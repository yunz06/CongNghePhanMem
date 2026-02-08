import os
import uuid
from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
from models import db, Paper, Decision   # ✅ thêm Decision

paper_bp = Blueprint("paper", __name__, url_prefix="/api/papers")

# =========================
# CONFIG
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"pdf", "docx"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# UTILS
# =========================
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# =========================
# ROUTES
# =========================
@paper_bp.route("/submit", methods=["POST"])
def submit_paper():
    if "user_id" not in session:
        return jsonify({"message": "Chưa đăng nhập"}), 401

    title = request.form.get("title")
    abstract = request.form.get("abstract", "")
    file = request.files.get("file")

    if not title:
        return jsonify({"message": "Thiếu tiêu đề bài báo"}), 400

    if not file or file.filename == "":
        return jsonify({"message": "Chưa upload file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"message": "Chỉ chấp nhận PDF hoặc DOCX"}), 400

    # Lưu file
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = secure_filename(f"{uuid.uuid4().hex}.{ext}")
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # =========================
    # TẠO PAPER
    # =========================
    paper = Paper(
        title=title,
        abstract=abstract,
        file_path=file_path,
        status="SUBMITTED",
        author_id=session["user_id"]
    )

    db.session.add(paper)
    db.session.commit()

    # =========================
    # AUTO TẠO DECISION
    # =========================
    decision = Decision(
        paper_id=paper.id,
        score=0,
        status="PENDING"
    )

    db.session.add(decision)
    db.session.commit()

    return jsonify({
        "message": "Nộp bài thành công",
        "paper_id": paper.id
    }), 201


@paper_bp.route("/<int:paper_id>", methods=["DELETE"])
def delete_paper(paper_id):
    if "user_id" not in session:
        return jsonify({"message": "Chưa đăng nhập"}), 401

    paper = Paper.query.get(paper_id)
    if not paper:
        return jsonify({"message": "Bài báo không tồn tại"}), 404

    if paper.author_id != session["user_id"]:
        return jsonify({"message": "Không có quyền xoá bài này"}), 403

    if paper.status in ("ACCEPTED", "REJECTED"):
        return jsonify({"message": "Bài đã được duyệt, không thể xoá"}), 400

    if paper.file_path and os.path.exists(paper.file_path):
        os.remove(paper.file_path)

    Decision.query.filter_by(paper_id=paper.id).delete()
    db.session.delete(paper)
    db.session.commit()

    return jsonify({"message": "Đã xoá bài báo"}), 200


# =========================
# ADMIN – CHẤM ĐIỂM & DUYỆT
# =========================
@paper_bp.route("/<int:paper_id>/decision", methods=["POST"])
def decide_paper(paper_id):
    if "user_id" not in session:
        return jsonify({"message": "Chưa đăng nhập"}), 401

    # TODO: check role ADMIN ở đây
    data = request.json
    score = data.get("score")
    status = data.get("status")  # ACCEPTED | REJECTED

    if status not in ("ACCEPTED", "REJECTED"):
        return jsonify({"message": "Trạng thái không hợp lệ"}), 400

    paper = Paper.query.get(paper_id)
    if not paper:
        return jsonify({"message": "Bài báo không tồn tại"}), 404

    decision = Decision.query.filter_by(paper_id=paper.id).first()
    if not decision:
        return jsonify({"message": "Decision không tồn tại"}), 404

    decision.score = score
    decision.status = status
    paper.status = status   # đồng bộ trạng thái

    db.session.commit()

    return jsonify({"message": "Đã chấm điểm & duyệt bài"}), 200


# =========================
# ADMIN – XEM DANH SÁCH BÀI
# =========================
@paper_bp.route("", methods=["GET"])
def list_papers():
    if "user_id" not in session:
        return jsonify({"message": "Chưa đăng nhập"}), 401

    papers = (
        db.session.query(Paper, Decision)
        .join(Decision, Paper.id == Decision.paper_id)
        .order_by(Paper.created_at.desc())
        .all()
    )

    result = []
    for paper, decision in papers:
        result.append({
            "id": paper.id,
            "title": paper.title,
            "status": paper.status,
            "score": decision.score,
            "decision_status": decision.status,
            "created_at": paper.created_at.strftime("%Y-%m-%d")
        })

    return jsonify(result), 200
