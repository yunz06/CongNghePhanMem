"""
UTH-ConfMS - Middleware Decorators
[TP1] User Management

Middleware để chặn API admin nếu user không có role='admin'
"""

from functools import wraps
from flask import jsonify, session
from models import User


def admin_required(f):
    """
    Middleware: Chặn các API admin nếu user không có role='admin'

    Sử dụng:
        @app.route('/api/admin/users')
        @admin_required
        def get_all_users():
            # Chỉ admin mới vào được đây
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Lấy user_id từ session
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({
                'error': 'Chưa đăng nhập',
                'code': 'UNAUTHORIZED'
            }), 401

        # Tìm user trong database
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'error': 'User không tồn tại',
                'code': 'USER_NOT_FOUND'
            }), 404

        # Kiểm tra role
        if user.role != 'admin':
            return jsonify({
                'error': 'Không có quyền truy cập',
                'code': 'FORBIDDEN',
                'message': 'Chức năng này yêu cầu role: admin',
                'your_role': user.role
            }), 403

        return f(*args, **kwargs)

    return decorated_function


def login_required(f):
    """
    Middleware: Yêu cầu user phải đăng nhập
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({
                'error': 'Chưa đăng nhập',
                'code': 'UNAUTHORIZED'
            }), 401

        return f(*args, **kwargs)

    return decorated_function


def get_current_user():
    """
    Helper: Lấy user hiện tại từ session

    Returns:
        User object hoặc None
    """
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None
