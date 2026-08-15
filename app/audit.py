from datetime import datetime
from app import db
from app.models import AuditLog


def log_action(user_id, action):
    log = AuditLog(
        user_id=user_id,
        action=action,
        timestamp=datetime.now()
    )

    db.session.add(log)
    db.session.commit()