from flask import Blueprint, render_template, request, redirect, url_for
from app import db, bcrypt
from app.models import User, File, SharedFile
from flask_login import login_user, logout_user, login_required, current_user
from app.audit import log_action

auth = Blueprint("auth", __name__)

@auth.route("/dashboard")
@login_required
def dashboard():

    # Files owned by the current user
    owned_files = File.query.filter_by(
        owner_id=current_user.id
    ).all()

    # Files shared with the current user
    shared_files = (
        File.query
        .join(SharedFile, File.id == SharedFile.file_id)
        .filter(SharedFile.shared_with == current_user.id)
        .all()
    )

    # Combine owned and shared files
    files = owned_files + shared_files

    return render_template(
        "dashboard.html",
        files=files
    )

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Passwords do not match."

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "Username already exists."

        # Hash the password
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(
            username=username,
            password_hash=password_hash
        )

        db.session.add(new_user)
        db.session.commit()

        log_action(new_user.id, "User registered")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        # Check password hash
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)

            log_action(user.id, "User logged in")

            return redirect(url_for("auth.dashboard"))
        return "Invalid username or password."

    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():

    log_action(current_user.id, "User logged out")

    logout_user()

    return redirect(url_for("auth.login"))