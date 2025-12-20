from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from backend import decision_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.register_blueprint(decision_bp)

# --- MEMBER 7: CODE TẠO BẢNG LỖI (SYSTEM BUGS) ---
# Lưu ý: Dán đoạn này ở CUỐI file, bên dưới dòng db = SQLAlchemy(app)

class SystemBug(db.Model):
    __tablename__ = 'system_bugs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Open')
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Bug {self.id}: {self.status}>'

# Define User model to satisfy ForeignKey constraint
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
