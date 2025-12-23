"""
UTH-ConfMS - Authentication Routes
[TP1] Auth System

API Endpoints:
- POST /api/auth/register - Đăng ký tài khoản
- POST /api/auth/login - Đăng nhập
- POST /api/auth/logout - Đăng xuất
- GET /api/auth/me - Thông tin user hiện tại
"""

from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from utils.audit import log_action

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    API Register: Đăng ký tài khoản mới

    Request Body:
        {
            "email": "user@example.com",
            "password": "password123",
            "name": "Nguyễn Văn A"
        }

    Response:
        - 201: Đăng ký thành công
        - 400: Thiếu thông tin
        - 409: Email đã tồn tại
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Không có dữ liệu'}), 400

    # Lấy thông tin
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    name = data.get('name', '').strip()

    # Validate
    if not email:
        return jsonify({'error': 'Email là bắt buộc'}), 400

    if not password:
        return jsonify({'error': 'Password là bắt buộc'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Password phải ít nhất 6 ký tự'}), 400

    if not name:
        return jsonify({'error': 'Name là bắt buộc'}), 400

    # Check email đã tồn tại
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email đã được sử dụng'}), 409

    # Tạo user mới - Hash password bằng werkzeug.security
    new_user = User(
        email=email,
        password_hash=generate_password_hash(password),
        name=name,
        role='author'  # Default role = 'author'
    )

    try:
        db.session.add(new_user)
        db.session.commit()

        # Ghi audit log
        log_action(new_user.id, 'USER_REGISTERED')

        return jsonify({
            'message': 'Đăng ký thành công',
            'user': new_user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Đăng ký thất bại', 'details': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    API Login: Đăng nhập

    Request Body:
        {
            "email": "user@example.com",
            "password": "password123"
        }

    Response:
        - 200: { user: { id, email, name, role } }
        - 401: Sai email hoặc password
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Không có dữ liệu'}), 400

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email và password là bắt buộc'}), 400

    # Tìm user theo email
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'error': 'Email không tồn tại'}), 401

    # Kiểm tra password bằng werkzeug.security
    if not check_password_hash(user.password_hash, password):
        # Ghi audit log - đăng nhập thất bại
        log_action(user.id, 'LOGIN_FAILED')
        return jsonify({'error': 'Mật khẩu không đúng'}), 401

    # Lưu session
    session['user_id'] = user.id

    # Ghi audit log - đăng nhập thành công
    log_action(user.id, 'USER_LOGIN')

    # Trả về thông tin user + role
    return jsonify({
        'message': 'Đăng nhập thành công',
        'user': user.to_dict()
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    API Logout: Đăng xuất
    """
    user_id = session.get('user_id')

    if user_id:
        log_action(user_id, 'USER_LOGOUT')

    session.clear()

    return jsonify({'message': 'Đăng xuất thành công'}), 200


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """
    API: Lấy thông tin user đang đăng nhập
    """
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'Chưa đăng nhập'}), 401

    user = User.query.get(user_id)

    if not user:
        session.clear()
        return jsonify({'error': 'User không tồn tại'}), 404

    return jsonify({
        'user': user.to_dict()
    }), 200
