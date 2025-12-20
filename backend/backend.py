from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
import pandas as pd
import io
import copy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

decision_bp = Blueprint('decision', __name__)

# --- DỮ LIỆU MẪU ---
INITIAL_DATA = [
    {"id": "BB01", "title": "Nghiên cứu AI trong chẩn đoán Y tế", "author": "Dương Ngọc Yến Nhi", "score": 8.5, "status": "REVIEWED", "date": "2025-01-10"},
    {"id": "BB02", "title": "Ứng dụng Blockchain trong Logistic", "author": "Trần Minh Quân", "score": 9.5, "status": "REVIEWED", "date": "2025-01-11"},
    {"id": "BB03", "title": "Giải pháp An toàn thông tin Cloud", "author": "Lê Văn Cường", "score": 7.0, "status": "REVIEWED", "date": "2025-01-12"},
    {"id": "BB04", "title": "Phân tích Dữ liệu lớn trong Giáo dục", "author": "Phạm Văn Dũng", "score": 9.2, "status": "REVIEWED", "date": "2025-01-09"},
    {"id": "BB05", "title": "Hệ thống Giao thông thông minh IoT", "author": "Võ Văn Em", "score": 6.0, "status": "REVIEWED", "date": "2025-01-13"}
]

mock_papers_db = copy.deepcopy(INITIAL_DATA)

#  CÁC API KHÁC GIỮ NGUYÊN 
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
    p_id = data.get('paper_id')
    decision = data.get('decision')
    for p in mock_papers_db:
        if p['id'] == p_id:
            p['status'] = decision
            p['final_date'] = datetime.now().strftime("%Y-%m-%d")
            return jsonify({"success": True, "message": "Đã cập nhật!"})
    return jsonify({"success": False}), 404

@decision_bp.route('/export', methods=['GET'])
def export_excel():
    try:
        df = pd.DataFrame(mock_papers_db)
        df.rename(columns={'id':'Mã', 'title':'Tên Bài', 'author':'Tác Giả', 'score':'Điểm', 'status':'Trạng Thái'}, inplace=True)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='KyYeu')
            ws = writer.sheets['KyYeu']
            for col in ws.columns:
                max_len = 0
                col_let = col[0].column_letter
                for cell in col:
                    try: 
                        if len(str(cell.value)) > max_len: max_len = len(str(cell.value))
                    except: pass
                ws.column_dimensions[col_let].width = max_len + 2
        output.seek(0)
        return send_file(output, download_name="KyYeu_2025.xlsx", as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@decision_bp.route('/send-email', methods=['POST'])
def send_email_notification():
    data = request.json
    p_id = data.get('id')
    email_to = data.get('email_to')
    
    # Lấy tài khoản gửi từ Frontend
    sender_email = data.get('sender_email')
    sender_pass = data.get('sender_pass')
    
    if not sender_email or not sender_pass:
        return jsonify({"success": False, "message": "Chưa nhập thông tin Admin!"}), 400

    paper = next((p for p in mock_papers_db if p['id'] == p_id), None)
    
    if paper:
        try:
            msg = MIMEMultipart()
            
           
            msg['From'] = f"Hội đồng Xét duyệt - Trường ĐH GTVT TP.HCM <{sender_email}>"
            
            msg['To'] = email_to
            
            # Cấu hình nội dung (Như cũ)
            if paper['status'] == 'ACCEPTED':
                msg['Subject'] = f"🎉 [THÔNG BÁO] KẾT QUẢ XÉT DUYỆT: {paper['title']}"
                status_color = "#28a745"
                status_text = "ĐƯỢC CHẤP NHẬN (ACCEPTED)"
                icon = "🎉"
                intro = "Hội đồng khoa học trân trọng thông báo bài báo của bạn đã ĐẠT YÊU CẦU."
                bg_header = "#0056b3"
            elif paper['status'] == 'REJECTED':
                msg['Subject'] = f"⚠️ [THÔNG BÁO] KẾT QUẢ XÉT DUYỆT: {paper['title']}"
                status_color = "#dc3545"
                status_text = "TỪ CHỐI (REJECTED)"
                icon = "⚠️"
                intro = "Hội đồng khoa học rất tiếc thông báo bài báo chưa đạt yêu cầu."
                bg_header = "#6c757d"
            else:
                msg['Subject'] = f"⏳ [THÔNG BÁO] Đang xử lý hồ sơ {paper['id']}"
                status_color = "#ffc107"
                status_text = "ĐANG CHỜ"
                icon = "⏳"
                intro = "Hồ sơ đang được xem xét."
                bg_header = "#17a2b8"

            # HTML Content (Giữ nguyên giao diện đẹp)
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                <div style="max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                    <div style="background-color: {bg_header}; color: #ffffff; padding: 30px 20px; text-align: center;">
                        <h1 style="margin: 0; font-size: 22px; text-transform: uppercase;">HỘI ĐỒNG KHOA HỌC - UTH</h1>
                        <p style="margin: 5px 0 0; font-size: 14px;">Trường Đại học Giao thông vận tải TP.HCM</p>
                    </div>
                    <div style="padding: 30px;">
                        <p>Kính gửi tác giả <strong>{paper['author']}</strong>,</p>
                        <p>{intro}</p>
                        <div style="background-color: #f8f9fa; border-left: 6px solid {status_color}; padding: 20px; margin: 25px 0;">
                            <h3 style="margin-top: 0; color: {status_color}; font-size: 18px;">{icon} KẾT QUẢ ĐÁNH GIÁ</h3>
                            <p><strong>Bài báo:</strong> {paper['title']}</p>
                            <p><strong>Điểm số:</strong> {paper['score']}/10</p>
                            <p><strong>Trạng thái:</strong> <span style="color: {status_color}; font-weight: bold;">{status_text}</span></p>
                        </div>
                        <p>Trân trọng,<br><strong>Ban Thư Ký Hội Đồng</strong></p>
                    </div>
                </div>
            </body>
            </html>
            """
            msg.attach(MIMEText(html_content, 'html'))

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_email, sender_pass)
            server.send_message(msg)
            server.quit()

            return jsonify({"success": True, "message": f"Đã gửi tới {email_to}"})

        except Exception as e:
            return jsonify({"success": False, "message": f"Lỗi: {str(e)}"}), 500
    
    return jsonify({"success": False, "message": "Không tìm thấy dữ liệu"}), 404
