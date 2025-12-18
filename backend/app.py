from flask import Flask
from flask_cors import CORS

# Import cái file "assignment_routes" bạn vừa viết ở trên
from backend.routes.assignment_routes import assignment_bp

app = Flask(__name__)
CORS(app) # Cho phép Frontend gọi API thoải mái

# --- ĐĂNG KÝ BLUEPRINT (CẮM DÂY) ---
# Dòng này cực quan trọng, thiếu nó là API không chạy
app.register_blueprint(assignment_bp)

# Test thử xem Server sống không
@app.route('/')
def home():
    return "Hello! UTH-ConfMS Backend is running with AI Power!"

if __name__ == '__main__':
    # Chạy server ở cổng 5000
    app.run(debug=True, port=5000)