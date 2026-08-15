from flask import Blueprint, request, redirect, url_for, current_app, send_from_directory, abort, render_template
from flask_login import login_required, current_user
from app import db
from app.models import File, SharedFile, User
import os
from datetime import datetime
from app.audit import log_action

files = Blueprint("files", __name__)

@files.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    if request.method == "POST":

        uploaded_file = request.files["file"]

        if uploaded_file.filename == "":
            return "No file selected."

        # Create a unique filename
        filename = uploaded_file.filename

        # Path to the uploads directory
        upload_folder = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "uploads"
        )

        # Save the physical file
        uploaded_file.save(os.path.join(upload_folder, filename))

        # Get file size
        file_size = os.path.getsize(
            os.path.join(upload_folder, filename)
        )

        # Create database record
        new_file = File(
            filename=filename,
            owner_id=current_user.id,
            upload_date=datetime.now(),
            file_size=file_size
        )

        db.session.add(new_file)
        db.session.commit()

        log_action(
            current_user.id,
            f"File uploaded: {filename}"
        )

        return "File uploaded successfully."

    return render_template("upload.html")

@files.route("/download/<int:file_id>")
@login_required
def download_file(file_id):

    # Find the file in the database
    file = File.query.get_or_404(file_id)

    # Check if the current user owns the file
    is_owner = file.owner_id == current_user.id

    # Check if the file has been shared with the current user
    is_shared = SharedFile.query.filter_by(
        file_id=file.id,
        shared_with=current_user.id
    ).first() is not None

    # Only the owner or an authorized shared user can download
    if not is_owner and not is_shared:
        log_action(
            current_user.id,
            f"Unauthorized download attempt: {file.filename}"
        )
        abort(403)

    # Record the download
    log_action(
        current_user.id,
        f"File downloaded: {file.filename}"
    )

    # Get the upload directory
    upload_folder = current_app.config["UPLOAD_FOLDER"]

    # Send the file to the user
    return send_from_directory(
        upload_folder,
        file.filename,
        as_attachment=True
    )

@files.route("/delete/<int:file_id>", methods=["POST"])
@login_required
def delete_file(file_id):

    # Find the file in the database
    file = File.query.get_or_404(file_id)

    # Make sure the logged-in user owns the file
    if file.owner_id != current_user.id:
        abort(403)

    # Get the upload directory
    upload_folder = current_app.config["UPLOAD_FOLDER"]

    # Build the path to the physical file
    file_path = os.path.join(upload_folder, file.filename)

    # Delete the physical file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete any sharing records associated with the file
    SharedFile.query.filter_by(file_id=file.id).delete()

    # Delete the database record
    db.session.delete(file)
    db.session.commit()

    # Record the deletion
    log_action(
        current_user.id,
        f"File deleted: {file.filename}"
    )

    return redirect(url_for("auth.dashboard"))

@files.route("/share/<int:file_id>", methods=["POST"])
@login_required
def share_file(file_id):

    # Find the file
    file = File.query.get_or_404(file_id)

    # Only the owner can share the file
    if file.owner_id != current_user.id:
        abort(403)

    # Get the username entered in the form
    username = request.form["username"]

    # Find the user receiving the file
    user = User.query.filter_by(username=username).first()

    # Make sure the user exists
    if not user:
        return "User not found."

    # Prevent sharing a file with yourself
    if user.id == current_user.id:
        return "You cannot share a file with yourself."

    # Check whether the file has already been shared with this user
    existing_share = SharedFile.query.filter_by(
        file_id=file.id,
        shared_with=user.id
    ).first()

    if existing_share:
        return "File is already shared with this user."

    # Create the sharing record
    shared_file = SharedFile(
        file_id=file.id,
        shared_with=user.id
    )

    db.session.add(shared_file)
    db.session.commit()

    # Record the file sharing
    log_action(
        current_user.id,
        f"File shared: {file.filename} with user {user.username}"
    )

    return redirect(url_for("auth.dashboard"))