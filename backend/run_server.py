from flask import Flask
from flask_cors import CORS
from backend import decision_bp

app = Flask(__name__)
CORS(app) # Cho phép Frontend gọi API

app.register_blueprint(decision_bp, url_prefix='/api/decision')

if __name__ == '__main__':
    print("🚀 SERVER ĐANG CHẠY TẠI: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)