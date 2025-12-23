"""
UTH-ConfMS - Audit System
[TP1] Audit Logs

Hàm log_action() để ghi lại mọi thay đổi dữ liệu vào bảng audit_logs
"""

from models import db, AuditLog


def log_action(user_id, action):
    """
    Ghi lại hành động vào bảng audit_logs.

    Sử dụng: Gọi hàm này mỗi khi có thay đổi dữ liệu trong hệ thống.

    Args:
        user_id (int): ID của user thực hiện hành động
        action (str): Mô tả hành động
            VD: "USER_LOGIN", "USER_REGISTERED", "PAPER_SUBMITTED"

    Returns:
        AuditLog: Object đã tạo, hoặc None nếu lỗi

    Example:
        log_action(user_id=1, action="USER_LOGIN")
        log_action(user_id=2, action="PAPER_SUBMITTED")
    """
    try:
        # INSERT INTO audit_logs (user_id, action, timestamp) VALUES (?, ?, NOW())
        log = AuditLog(
            user_id=user_id,
            action=action
        )
        db.session.add(log)
        db.session.commit()

        # Log to console
        print(f"[AUDIT] User {user_id}: {action}")

        return log

    except Exception as e:
        print(f"[AUDIT ERROR] Failed to log action: {str(e)}")
        db.session.rollback()
        return None
