from flask import Flask, Blueprint, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
import pandas as pd
import io
import copy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==============================
# KHỞI TẠO APP
# ==============================
app = Flask(__name__)
CORS(app)

decision_bp = Blueprint('decision', __name__)

# ==============================
# DỮ LIỆU MẪU
# ==============================
INITIAL_DATA = [
    {
        "id": "BB01",
        "title": "Nghiên cứu AI trong chẩn đoán Y tế",
        "author": "student1@gmail.com",
        "abstract": "Mô tả về AI...",
        "score": 8.5,
        "status": "REVIEWED",
        "date": "2025-01-10"
    },
    {
        "id": "BB02",
        "title": "Ứng dụng Blockchain",
        "author": "student2@gmail.com",
        "abstract": "Mô tả Blockchain...",
        "score": 9.5,
        "status": "REVIEWED",
        "date": "2025-01-11"
    },
]

mock_papers_db = copy.deepcopy(INITIAL_DATA)
ADMIN_DB = []
STUDENTS_DB = []

# ==============================
# AUTH API
# ==============================
@decision_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email, password)
        server.quit()
        return jsonify({"success": True, "role": "admin", "user": email})
    except:
        if any(u['email'] == email and u['password'] == password for u in ADMIN_DB):
            return jsonify({"success": True, "role": "admin", "user": email})
        return jsonify({"success": False, "message": "Sai thông tin Admin!"}), 401


@decision_bp.route('/student/register', methods=['POST'])
def student_register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if any(u['email'] == email for u in STUDENTS_DB):
        return jsonify({"success": False, "message": "Email đã tồn tại!"}), 400

    STUDENTS_DB.append({"email": email, "password": password})
    return jsonify({"success": True, "message": "Đăng ký thành công!"}), 201


@decision_bp.route('/student/login', methods=['POST'])
def student_login():
    data = request.json
    user = next(
        (u for u in STUDENTS_DB
         if u['email'] == data.get('email')
         and u['password'] == data.get('password')),
        None
    )
    if user:
        return jsonify({"success": True, "role": "student", "user": user['email']})
    return jsonify({"success": False, "message": "Sai thông tin sinh viên!"}), 401


# ==============================
# NỘP BÀI
# ==============================
@decision_bp.route('/submit', methods=['POST'])
def submit_paper():
    title = request.form.get('title')
    abstract = request.form.get('abstract')
    author = request.form.get('author')
    file = request.files.get('file')

    if not title or not author:
        return jsonify({"success": False, "message": "Thiếu thông tin"}), 400

    filename = file.filename if file else "No file"

    new_paper = {
        "id": f"BB{len(mock_papers_db) + 1:02d}",
        "title": title,
        "author": author,
        "abstract": abstract,
        "filename": filename,
        "score": 0.0,
        "status": "REVIEWED",
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    mock_papers_db.append(new_paper)
    return jsonify({"success": True, "message": "Nộp bài thành công!"}), 201


# ==============================
# LẤY DANH SÁCH BÀI
# ==============================
@decision_bp.route('/papers', methods=['GET'])
def get_papers():
    return jsonify({"success": True, "data": mock_papers_db})


# ==============================
# CẬP NHẬT ĐIỂM
# ==============================
@decision_bp.route('/update-score', methods=['POST'])
def update_score():
    data = request.json
    p_id = data.get('paper_id')
    new_score = data.get('score')

    for p in mock_papers_db:
        if p['id'] == p_id:
            p['score'] = float(new_score)
            return jsonify({"success": True, "message": "Đã lưu điểm!"})

    return jsonify({"success": False, "message": "Không tìm thấy bài!"}), 404


# ==============================
# QUYẾT ĐỊNH ACCEPT / REJECT
# ==============================
@decision_bp.route('/make', methods=['POST'])
def make_decision():
    data = request.json
    for p in mock_papers_db:
        if p['id'] == data.get('paper_id'):
            p['status'] = data.get('decision')
            return jsonify({"success": True})
    return jsonify({"success": False}), 404


# ==============================
# RESET DATA
# ==============================
@decision_bp.route('/reset', methods=['POST'])
def reset_data():
    global mock_papers_db
    mock_papers_db = copy.deepcopy(INITIAL_DATA)
    return jsonify({"success": True, "message": "Reset thành công!"})


# ==============================
# EXPORT EXCEL
# ==============================
@decision_bp.route('/export', methods=['GET'])
def export_excel():
    try:
        df = pd.DataFrame(mock_papers_db)
        if df.empty:
            return jsonify({"success": False, "message": "Chưa có dữ liệu!"}), 400

        df = df[['id', 'title', 'author', 'score', 'status', 'date']]
        df.rename(columns={
            'id': 'Mã HS',
            'title': 'Tên Đề Tài',
            'author': 'Tác Giả',
            'score': 'Điểm',
            'status': 'Trạng Thái',
            'date': 'Ngày Nộp'
        }, inplace=True)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='KyYeu')

        output.seek(0)
        return send_file(
            output,
            download_name=f"KyYeu_{datetime.now().strftime('%d%m%Y')}.xlsx",
            as_attachment=True
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ==============================
# GỬI EMAIL THÔNG BÁO
# ==============================
@decision_bp.route('/send-email', methods=['POST'])
def send_email_notification():
    data = request.json
    p_id = data.get('id')
    email_to = data.get('email_to')
    sender_email = data.get('sender_email')
    sender_pass = data.get('sender_pass')

    paper = next((p for p in mock_papers_db if p['id'] == p_id), None)
    if not paper:
        return jsonify({"success": False}), 404

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email_to

        if paper['status'] == 'ACCEPTED':
            msg['Subject'] = f"🎉 KẾT QUẢ: {paper['title']}"
            intro = "Chúc mừng! Bài báo của bạn đã được chấp nhận."
        else:
            msg['Subject'] = f"⚠️ KẾT QUẢ: {paper['title']}"
            intro = "Rất tiếc, bài báo của bạn chưa đạt yêu cầu."

        msg.attach(MIMEText(intro, 'plain'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_pass)
        server.send_message(msg)
        server.quit()

        return jsonify({"success": True, "message": "Đã gửi mail!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ==============================
# REGISTER BLUEPRINT
# ==============================
app.register_blueprint(decision_bp, url_prefix='/api/decision')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
