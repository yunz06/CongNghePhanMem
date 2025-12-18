from flask import Blueprint, request, jsonify
# Import hàm kết nối DB và hàm AI từ các file bạn đã làm
from backend.config import get_db_connection
from backend.services.ai_service import suggest_reviewer

# Tạo một "nhánh" API riêng cho phần phân công
assignment_bp = Blueprint('assignment_bp', __name__)

# --- API 1: LẤY DANH SÁCH REVIEWER (Ticket TP4-01) ---
# Logic: Lấy danh sách Reviewer NHƯNG loại bỏ tác giả bài báo (Tránh vừa đá bóng vừa thổi còi)
@assignment_bp.route('/api/reviewers-available/<int:paper_id>', methods=['GET'])
def get_available_reviewers(paper_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Lỗi kết nối Database"}), 500
    
    cur = conn.cursor()
    try:
        # 1. Tìm xem ai là tác giả của bài báo này?
        cur.execute("SELECT author_id FROM papers WHERE id = %s", (paper_id,))
        paper = cur.fetchone()
        if not paper:
            return jsonify({"error": "Không tìm thấy bài báo"}), 404
        author_id = paper[0]

        # 2. Lấy danh sách Reviewer, TRỪ ông tác giả ra
        query = """
            SELECT id, full_name, email 
            FROM users 
            WHERE role = 'reviewer' AND id != %s
        """
        cur.execute(query, (author_id,))
        reviewers = cur.fetchall()
        
        # 3. Trả về kết quả JSON gọn gàng
        result = [{"id": r[0], "name": r[1], "email": r[2]} for r in reviewers]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# --- API 2: GỢI Ý PHÂN CÔNG BẰNG AI (Ticket TP4-02) ---
# Logic: Gửi Abstract + DS Reviewer lên Google Gemini để nó chọn người giỏi nhất
@assignment_bp.route('/api/auto-assign', methods=['POST'])
def auto_assign():
    data = request.json
    paper_id = data.get('paper_id')

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # 1. Lấy Abstract (Tóm tắt) của bài báo
        cur.execute("SELECT title, abstract, author_id FROM papers WHERE id = %s", (paper_id,))
        paper_data = cur.fetchone()
        if not paper_data: 
            return jsonify({"error": "Không tìm thấy bài báo"}), 404
        
        paper_title = paper_data[0]
        abstract = paper_data[1]
        author_id = paper_data[2]

        # 2. Lấy danh sách Reviewer khả dụng (để gửi cho AI chọn)
        cur.execute("SELECT id, full_name FROM users WHERE role = 'reviewer' AND id != %s", (author_id,))
        reviewers = cur.fetchall()
        
        if not reviewers:
            return jsonify({"error": "Không có Reviewer nào rảnh!"}), 400

        # Biến đổi danh sách thành chuỗi văn bản cho AI đọc
        # Ví dụ: "ID 1: Nguyen Van A, ID 5: Tran Thi B..."
        reviewers_list_str = ", ".join([f"ID {r[0]}: {r[1]}" for r in reviewers])

        # 3. GỌI THẦN CHÚ AI (Hàm này bạn đã viết trong ai_service.py)
        ai_suggestion = suggest_reviewer(abstract, reviewers_list_str)

        # 4. Trả kết quả về cho Admin xem
        return jsonify({
            "paper_title": paper_title,
            "ai_suggestion": ai_suggestion, # AI sẽ bảo: "Nên chọn ông A vì..."
            "available_reviewers": reviewers_list_str
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# --- API 3: LƯU PHÂN CÔNG (Ticket TP4-03) ---
# Logic: Sau khi Admin chốt người, lưu vào Database
@assignment_bp.route('/api/assign', methods=['POST'])
def save_assignment():
    data = request.json
    paper_id = data.get('paper_id')
    reviewer_id = data.get('reviewer_id')

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Insert vào bảng assignments
        # Cờ is_auto=TRUE để đánh dấu là có dùng AI hỗ trợ (Lấy điểm cộng)
        cur.execute("""
            INSERT INTO assignments (paper_id, reviewer_id, assigned_date)
            VALUES (%s, %s, CURRENT_TIMESTAMP)
        """, (paper_id, reviewer_id))
        
        conn.commit()
        return jsonify({"message": "Phân công thành công!"}), 201
    except Exception as e:
        conn.rollback()
        # Lỗi thường gặp: Gán 1 bài cho 1 người 2 lần
        return jsonify({"error": "Lỗi: Có thể bài này đã được gán cho người này rồi!"}), 400
    finally:
        cur.close()
        conn.close()