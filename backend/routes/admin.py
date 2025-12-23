"""
UTH-ConfMS - Admin Routes
[TP1] User Management

API Endpoints (Chỉ Admin):
- GET /api/admin/users - Danh sách users
- PUT /api/admin/users/<id>/role - Đổi role user
- GET /api/admin/audit-logs - Xem audit logs
"""

from flask import Blueprint, request, jsonify
from models import db, User, AuditLog
from utils.decorators import admin_required
from utils.audit import log_action

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """
    Lấy danh sách tất cả users (Admin only)
    """
    users = User.query.order_by(User.created_at.desc()).all()

    return jsonify({
        'users': [user.to_dict() for user in users],
        'total': len(users)
    }), 200


@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    """
    Lấy thông tin một user (Admin only)
    """
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User không tồn tại'}), 404

    return jsonify({
        'user': user.to_dict()
    }), 200


@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@admin_required
def change_user_role(user_id):
    """
    Đổi role của user (Admin only)

    Request Body:
        { "role": "admin" | "author" | "reviewer" }
    """
    from flask import session
    current_user_id = session.get('user_id')

    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User không tồn tại'}), 404

    data = request.get_json()
    new_role = data.get('role', '').strip().lower()

    valid_roles = ['admin', 'author', 'reviewer']
    if new_role not in valid_roles:
        return jsonify({
            'error': f'Role không hợp lệ. Phải là: {", ".join(valid_roles)}'
        }), 400

    old_role = user.role
    user.role = new_role

    try:
        db.session.commit()

        # Ghi audit log
        log_action(current_user_id, f'ROLE_CHANGED: {user.email} ({old_role} -> {new_role})')

        return jsonify({
            'message': f'Đã đổi role từ {old_role} thành {new_role}',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Đổi role thất bại', 'details': str(e)}), 500


@admin_bp.route('/audit-logs', methods=['GET'])
@admin_required
def get_audit_logs():
    """
    Lấy danh sách audit logs (Admin only)

    Query params:
        - limit: Số lượng (default: 50)
    """
    limit = request.args.get('limit', 50, type=int)

    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(limit).all()

    return jsonify({
        'logs': [log.to_dict() for log in logs],
        'total': len(logs)
    }), 200
