"""
UTH-ConfMS Backend API
# Contact email: phulm3648@ut.edu.vn
Module: Authentication & System (Member 1)
Student: Lâm Minh Phú
MSSV: 096206003648
Description: 
 - Xử lý Đăng ký/Đăng nhập (Hash password bằng werkzeug)
 - Phân quyền (Admin Middleware)
 - Ghi Nhật ký hệ thống (Audit Logs)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from functools import wraps

app = Flask(__name__)
CORS(app)

# ============================================
# CẤU HÌNH (CONFIG)
# ============================================
app.config['SECRET_KEY'] = 'uth-confms-secret-key-2025'

# Cấu hình kết nối Database PostgreSQL
# Lưu ý: Thay 'password' bằng mật khẩu PostgreSQL của máy bạn
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/uth_confms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ============================================
# MODELS (Phải khớp với file SQL)
# ============================================
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    users = db.relationship('User', backref='role_obj', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    fullname = db.Column(db.String(255))
    organization = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=4)
    is_active = db.Column(db.Boolean, default=True)

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# ============================================
# CORE FUNCTIONS (Nhiệm vụ Member 1)
# ============================================

# 1. Hàm ghi Audit Log (Bắt buộc)
def log_action(user_id, action):
    try:
        new_log = AuditLog(user_id=user_id, action=action)
        db.session.add(new_log)
        db.session.commit()
        print(f"[AUDIT] User {user_id}: {action}")
    except Exception as e:
        print(f"[AUDIT ERROR] {e}")
        db.session.rollback()

# 2. Middleware xác thực Token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Thiếu Token xác thực!'}), 401
        try:
            if token.startswith('Bearer '): token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            if not current_user: raise Exception
        except:
            return jsonify({'message': 'Token không hợp lệ!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# 3. Middleware Admin (Chỉ Admin mới được qua)
def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(current_user, *args, **kwargs):
        if current_user.role_obj.name != 'admin':
            return jsonify({'message': 'Truy cập bị từ chối! Yêu cầu quyền Admin.'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# ============================================
# API ENDPOINTS
# ============================================

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': 'Email đã tồn tại!'}), 409

    # Hash Password bằng Werkzeug (Yêu cầu PDF)
    hashed_pw = generate_password_hash(data.get('password'))
    
    # Tạo User mới (Mặc định Role ID 4 = Author)
    new_user = User(
        email=email,
        password_hash=hashed_pw,
        fullname=data.get('fullname'),
        organization=data.get('organization'),
        role_id=4 
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        
        # Ghi log ngay khi đăng ký thành công
        log_action(new_user.id, "Đăng ký tài khoản mới")
        
        return jsonify({'success': True, 'message': 'Đăng ký thành công!'}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()

    # Kiểm tra mật khẩu (Werkzeug)
    if user and check_password_hash(user.password_hash, data.get('password')):
        if not user.is_active: 
            return jsonify({'success': False, 'message': 'Tài khoản đã bị khóa!'}), 403
            
        role_name = user.role_obj.name
        
        # Tạo JWT Token
        token = jwt.encode({
            'user_id': user.id,
            'role': role_name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        # Ghi log đăng nhập
        log_action(user.id, "Đăng nhập hệ thống")

        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'fullname': user.fullname, 
                'role': role_name,
                'email': user.email
            }
        })
        
    return jsonify({'success': False, 'message': 'Sai email hoặc mật khẩu!'}), 401

# API Admin để xem Log (Dùng để test tính năng Phân quyền & Audit)
@app.route('/api/admin/logs', methods=['GET'])
@admin_required
def get_audit_logs(current_user):
    # Lấy 20 log mới nhất
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(20).all()
    
    return jsonify({
        'success': True,
        'logs': [{
            'user_id': l.user_id,
            'action': l.action,
            'time': l.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        } for l in logs]
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Đảm bảo bảng đã được tạo
    app.run(debug=True, port=5000)
