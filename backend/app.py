from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from models import db
import models   # load bảng

# =====================
# APP INIT
# =====================
app = Flask(__name__)
app.secret_key = "uth-secret-key"

# =====================
# DATABASE CONFIG
# =====================
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql://postgres:123456@localhost:5432/uth_confms"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# =====================
# MIGRATE
# =====================
migrate = Migrate(app, db)

# =====================
# CORS
# =====================
CORS(app, supports_credentials=True)

# =====================
# BLUEPRINTS
# =====================
from auth import auth_bp
from decision import decision_bp
from paper import paper_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(decision_bp, url_prefix="/api/decision")

# ✅ QUAN TRỌNG: PHẢI CÓ DÒNG NÀY
# paper.py đã có url_prefix="/api/papers"
app.register_blueprint(paper_bp)

# =====================
# MAIN
# =====================
if __name__ == "__main__":
    print(">>> Flask app starting...")
    app.run(debug=True)
