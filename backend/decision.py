from flask import Blueprint, request, jsonify, send_file, Flask
from flask_cors import CORS
from datetime import datetime
import pandas as pd
import io
import copy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Khởi tạo App
app = Flask(__name__)
CORS(app) 

decision_bp = Blueprint('decision', __name__)

# --- DỮ LIỆU MẪU (Lưu trên RAM) ---
INITIAL_DATA = [
    {"id": "BB01", "title": "Nghiên cứu AI trong chẩn đoán Y tế", "author": "student1@gmail.com", "abstract": "Mô tả về AI...", "score": 8.5, "status": "REVIEWED", "date": "2025-01-10"},
    {"id": "BB02", "title": "Ứng dụng Blockchain", "author": "student2@gmail.com", "abstract": "Mô tả Blockchain...", "score": 9.5, "status": "REVIEWED", "date": "2025-01-11"},
]
# Copy dữ liệu mẫu vào biến làm việc
mock_papers_db = copy.deepcopy(INITIAL_DATA)

# Lưu tài khoản tạm thời
ADMIN_DB = []
STUDENTS_DB = []

# ==========================================
# 1. API AUTH (Đăng nhập / Đăng ký)
# ==========================================

@decision_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # Cách 1: Thử đăng nhập bằng Gmail thật (SMTP)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email, password)
        server.quit()
        return jsonify({"success": True, "role": "admin", "user": email})
    except:
        # Cách 2: Nếu không phải Gmail thật, thử tìm trong DB nội bộ
        if any(u['email'] == email and u['password'] == password for u in ADMIN_DB):
            return jsonify({"success": True, "role": "admin", "user": email})
        return jsonify({"success": False, "message": "Sai thông tin Admin hoặc App Password!"}), 401

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
    user = next((u for u in STUDENTS_DB if u['email'] == data.get('email') and u['password'] == data.get('password')), None)
    if user: 
        return jsonify({"success": True, "role": "student", "user": user['email']})
    return jsonify({"success": False, "message": "Sai thông tin sinh viên!"}), 401

# ==========================================
# 2. API CHỨC NĂNG CHÍNH
# ==========================================

@decision_bp.route('/submit', methods=['POST'])
def submit_paper():
    # Nhận dữ liệu từ form nộp bài
    title = request.form.get('title')
    abstract = request.form.get('abstract')
    author = request.form.get('author')
    file = request.files.get('file')
    filename = file.filename if file else "No file"

    if not title or not author: 
        return jsonify({"success": False, "message": "Thiếu thông tin"}), 400

    # Tạo ID mới
    new_id = f"BB{len(mock_papers_db) + 1:02d}"
    
    new_paper = {
        "id": new_id,
        "title": title, "author": author, "abstract": abstract,
        "filename": filename, "score": 0, "status": "REVIEWED",
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    mock_papers_db.append(new_paper)
    return jsonify({"success": True, "message": "Nộp bài thành công!"}), 201

@decision_bp.route('/papers', methods=['GET'])
def get_papers():
    return jsonify({"success": True, "data": mock_papers_db})

@decision_bp.route('/reset', methods=['POST'])
def reset_data():
    global mock_papers_db
    mock_papers_db = copy.deepcopy(INITIAL_DATA)
    return jsonify({"success": True, "message": "Reset thành công!"})

@decision_bp.route('/make', methods=['POST'])
def make_decision():
    data = request.json
    for p in mock_papers_db:
        if p['id'] == data.get('paper_id'):
            p['status'] = data.get('decision')
            return jsonify({"success": True})
    return jsonify({"success": False}), 404

# --- API XUẤT EXCEL (ĐÃ FIX LỖI) ---
@decision_bp.route('/export', methods=['GET'])
def export_excel():
    try:
        # 1. Tạo DataFrame từ dữ liệu hiện có
        df = pd.DataFrame(mock_papers_db)
        
        # 2. Kiểm tra nếu chưa có dữ liệu
        if df.empty:
            return jsonify({"success": False, "message": "Chưa có dữ liệu!"}), 400

        # 3. Chọn lọc cột để xuất (Tránh lỗi thừa cột)
        cols_to_keep = ['id', 'title', 'author', 'score', 'status', 'date']
        existing_cols = [c for c in cols_to_keep if c in df.columns]
        df = df[existing_cols]
        
        # 4. Đổi tên cột sang tiếng Việt
        df.rename(columns={
            'id': 'Mã HS', 'title': 'Tên Đề Tài', 'author': 'Tác Giả',
            'score': 'Điểm', 'status': 'Trạng Thái', 'date': 'Ngày Nộp'
        }, inplace=True)

        # 5. Ghi file vào bộ nhớ RAM (BytesIO)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='KyYeu')
            
            # Tự động chỉnh độ rộng cột cho đẹp
            worksheet = writer.sheets['KyYeu']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except: pass
                worksheet.column_dimensions[column_letter].width = (max_length + 2)

        # 6. Đặt con trỏ về đầu file (QUAN TRỌNG ĐỂ KHÔNG BỊ LỖI FILE HỎNG)
        output.seek(0)
        
        # 7. Gửi file về trình duyệt
        return send_file(
            output, 
            download_name=f"KyYeu_HoiNghi_{datetime.now().strftime('%d%m%Y')}.xlsx", 
            as_attachment=True, 
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        print(f"Lỗi Export: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@decision_bp.route('/send-email', methods=['POST'])
def send_email_notification():
    data = request.json
    p_id = data.get('id')
    email_to = data.get('email_to')
    sender_email = data.get('sender_email')
    sender_pass = data.get('sender_pass')
    
    paper = next((p for p in mock_papers_db if p['id'] == p_id), None)
    if paper:
        try:
            msg = MIMEMultipart()
            msg['From'] = f"Hội đồng Xét duyệt UTH <{sender_email}>"
            msg['To'] = email_to
            
            if paper['status'] == 'ACCEPTED':
                msg['Subject'] = f"🎉 KẾT QUẢ: {paper['title']}"
                status_color = "#28a745"
                status_text = "ĐƯỢC CHẤP NHẬN (ACCEPTED)"
                bg_header = "#0056b3"
                icon = "🎉"
                intro = "Chúc mừng! Bài báo của bạn đã đạt yêu cầu."
            elif paper['status'] == 'REJECTED':
                msg['Subject'] = f"⚠️ KẾT QUẢ: {paper['title']}"
                status_color = "#dc3545"
                status_text = "TỪ CHỐI (REJECTED)"
                bg_header = "#6c757d"
                icon = "⚠️"
                intro = "Rất tiếc, bài báo chưa đạt yêu cầu."
            else: 
                return jsonify({"success": False, "message": "Trạng thái không hợp lệ"}), 400

            html_content = f"""
            <div style="font-family: Arial; max-width: 600px; border: 1px solid #ddd; margin: auto;">
                <div style="background:{bg_header}; color:white; padding:20px; text-align:center">
                    <h2 style="margin:0">HỘI ĐỒNG KHOA HỌC - UTH</h2>
                </div>
                <div style="padding:20px">
                    <p>Chào <strong>{paper['author']}</strong>,</p>
                    <p>{intro}</p>
                    <div style="background:#2d2d2d; color:white; padding:15px; border-left:5px solid {status_color}; margin:20px 0;">
                        <h3 style="color:{status_color}; margin:0 0 10px 0;">{icon} KẾT QUẢ ĐÁNH GIÁ</h3>
                        <p style="margin:5px 0">Bài: {paper['title']}</p>
                        <p style="margin:5px 0">Trạng thái: <strong>{status_text}</strong></p>
                    </div>
                    <p>Trân trọng,<br>Ban Thư Ký.</p>
                </div>
            </div>
            """
            msg.attach(MIMEText(html_content, 'html'))
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_email, sender_pass)
            server.send_message(msg)
            server.quit()
            return jsonify({"success": True, "message": "Đã gửi mail!"})
        except Exception as e: 
            return jsonify({"success": False, "message": str(e)}), 500
    return jsonify({"success": False}), 404

# Đăng ký Blueprint
app.register_blueprint(decision_bp, url_prefix='/api/decision')

if __name__ == '__main__':
    app.run(debug=True, port=5000)