from flask import Flask
from flask_cors import CORS

from models import db
import models   # QUAN TRỌNG: để load các bảng

# =====================
# APP INIT
# =====================
app = Flask(__name__)
app.secret_key = "uth-secret-key"

# =====================
# DATABASE CONFIG (PostgreSQL)
# =====================
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql://postgres:123456@localhost:5432/uth_confms"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# GẮN DB VỚI APP (ĐÚNG CÁCH)
db.init_app(app)

# =====================
# CORS
# =====================
CORS(app, supports_credentials=True)

# =====================
# BLUEPRINTS
# =====================
from auth import auth_bp
from decision import decision_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(decision_bp, url_prefix="/api/decision")

# =====================
# MAIN
# =====================
if __name__ == "__main__":
    print(">>> Flask app starting...")
    with app.app_context():
        db.create_all()   # tạo bảng
        print(">>> Database tables created")
    app.run(debug=True)
