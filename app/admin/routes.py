from flask import Blueprint
from flask_login import login_required
from app.auth.decorators import admin_required

admin = Blueprint("admin", __name__)


@admin.route("/admin")
@login_required
@admin_required
def admin_home():
    return "Admin Dashboard"