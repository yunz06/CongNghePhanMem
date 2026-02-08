from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Role, UserRole

auth_bp = Blueprint("auth", __name__)

# =====================
# REGISTER
# =====================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Thiếu email hoặc mật khẩu"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email đã tồn tại"}), 400

    user = User(
        email=email,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()

    # 🔹 Role mặc định là STUDENT
    role = Role.query.filter_by(name="student").first()
    if not role:
        role = Role(name="student")
        db.session.add(role)
        db.session.commit()

    db.session.add(UserRole(user_id=user.id, role_id=role.id))
    db.session.commit()

    return jsonify({"message": "Đăng ký sinh viên thành công"}), 201


# =====================
# LOGIN (LƯU SESSION)
# =====================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid credentials"}), 401

    roles = [role.name for role in user.roles]

    # 🔐 LƯU SESSION
    session["user_id"] = user.id
    session["roles"] = roles

    return jsonify({
        "message": "Login successful",
        "user_id": user.id,
        "roles": roles
    })


# =====================
# LOGOUT
# =====================
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logout successful"})