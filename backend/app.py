import sys
import os

# 1. Thêm dòng này để Python tìm thấy thư mục gốc
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from flask_cors import CORS

# 2. Sửa các dòng import: Thêm 'backend.' vào trước
from backend.config import get_db_connection
from backend.routes.assignment_routes import assignment_bp

app = Flask(__name__)
CORS(app)  # Cho phép Frontend kết nối

# Đăng ký các routes
app.register_blueprint(assignment_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=5000)