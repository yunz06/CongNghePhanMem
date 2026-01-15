from flask import Blueprint, request, jsonify, session

auth_bp = Blueprint('auth', __name__)

ADMIN_ACCOUNT = {
    "email": "admin@gmail.com",
    "password": "123456"
}

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if data.get('email') == ADMIN_ACCOUNT['email'] and data.get('password') == ADMIN_ACCOUNT['password']:
        session['logged_in'] = True
        session['admin_email'] = data['email']
        return jsonify({"success": True})
    return jsonify({"success": False}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})


def login_required(func):
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
