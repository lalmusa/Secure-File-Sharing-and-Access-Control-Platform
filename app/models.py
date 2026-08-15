from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    # Generates new IDs for each user
    id = db.Column(db.Integer, primary_key=True)

    # Usernames must be no more than 80 characters, cannot be empty, and must be unique
    username = db.Column(db.String(80), unique=True, nullable=False)

    # We will not store passwords directly; instead, store a hash of the password
    password_hash = db.Column(db.String(255), nullable=False)

    # Only two roles are planned: user and admin
    role = db.Column(db.String(20), default="user")

    # Relationship between users and their files
    files = db.relationship("File", backref="owner", lazy=True)


class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)
    file_size = db.Column(db.Integer, nullable=False)

class SharedFile(db.Model):
    __tablename__ = "shared_files"

    id = db.Column(db.Integer, primary_key=True)

    file_id = db.Column(
        db.Integer,
        db.ForeignKey("files.id"),
        nullable=False
    )

    shared_with = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    action = db.Column(
        db.String(255),
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False
    )

    user = db.relationship("User", backref="audit_logs")