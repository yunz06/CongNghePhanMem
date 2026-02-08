from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# =====================
# USER & ROLE
# =====================

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    roles = db.relationship(
        "Role",
        secondary="user_roles",
        backref="users"
    )


class UserRole(db.Model):
    __tablename__ = "user_roles"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), primary_key=True)


# =====================
# PAPER
# =====================

class Paper(db.Model):
    __tablename__ = "papers"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    abstract = db.Column(db.Text)

    file_path = db.Column(db.String(255))        
    status = db.Column(db.String(50), default="SUBMITTED")

    author_id = db.Column(                     
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)



# =====================
# ASSIGNMENT & REVIEW
# =====================

class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey("papers.id"))
    reviewer_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    __table_args__ = (
        db.UniqueConstraint("paper_id", "reviewer_id", name="unique_assignment"),
    )


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey("papers.id"))
    reviewer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    score = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# =====================
# DECISION
# =====================

class Decision(db.Model):
    __tablename__ = "decisions"

    id = db.Column(db.Integer, primary_key=True)

    paper_id = db.Column(
        db.Integer,
        db.ForeignKey("papers.id"),
        nullable=False,
        unique=True          # 1 paper = 1 decision
    )

    score = db.Column(db.Float, default=0)        
    status = db.Column(
        db.String(50),
        default="PENDING"     # PENDING | ACCEPTED | REJECTED
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
