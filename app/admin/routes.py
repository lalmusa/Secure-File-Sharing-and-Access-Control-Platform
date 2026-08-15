from flask import Blueprint, render_template
from flask_login import login_required
from app.auth.decorators import admin_required
from app.models import User, AuditLog

admin = Blueprint("admin", __name__)


@admin.route("/admin")
@login_required
@admin_required
def admin_home():

    users = User.query.all()

    logs = AuditLog.query.order_by(
        AuditLog.timestamp.desc()
    ).all()

    return render_template(
        "admin_dashboard.html",
        users=users,
        logs=logs
    )