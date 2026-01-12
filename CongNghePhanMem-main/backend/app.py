"""
UTH-ConfMS - Main Flask Application
[TP1] Auth System, Audit Logs, User Management

Author: Member 1 - Leader & System
"""

from flask import Flask
from flask_cors import CORS
from models import db, User
from werkzeug.security import generate_password_hash

# Import routes
from routes.auth import auth_bp
from routes.admin import admin_bp


def create_app():
    app = Flask(__name__)

    # Cấu hình
    app.config['SECRET_KEY'] = 'uth-confms-secret-key-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uth_confms.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    CORS(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    # Tạo database và admin mặc định
    with app.app_context():
        db.create_all()

        # Tạo admin user nếu chưa có
        admin = User.query.filter_by(email='admin@uth.edu.vn').first()
        if not admin:
            admin = User(
                email='admin@uth.edu.vn',
                password_hash=generate_password_hash('admin123'),
                name='Administrator',
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print('✅ Đã tạo tài khoản admin: admin@uth.edu.vn / admin123')

    # Health check
    @app.route('/api/health')
    def health():
        return {'status': 'OK', 'service': 'UTH-ConfMS Backend'}

    return app


# Chạy server
if __name__ == '__main__':
    app = create_app()
    print('🚀 UTH-ConfMS Backend đang chạy tại http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)
