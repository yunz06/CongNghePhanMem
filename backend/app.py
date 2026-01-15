from flask import Flask, send_file, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import os

from auth import auth_bp
from decision import decision_bp

app = Flask(__name__)
app.secret_key = "uth-secret-key"

# ===== DATABASE =====
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///system.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

CORS(app, supports_credentials=True)

# ===== MODEL =====
class Decision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    result = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ===== REGISTER BLUEPRINT =====
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(decision_bp, url_prefix="/api/decision")
