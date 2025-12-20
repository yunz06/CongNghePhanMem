from flask import Blueprint, request, jsonify
# Giả sử bạn có hàm lấy kết nối DB từ file config hoặc app
# from config import get_db_connection 

assignment_bp = Blueprint('assignment_bp', __name__)

@assignment_bp.route('/api/assignments', methods=['POST'])
def assign_reviewer():
    """
    [TP4] API Gán bài review cho giảng viên
    Input: { "paper_id": 1, "user_id": 2 }
    """
    data = request.json
    paper_id = data.get('paper_id')
    user_id = data.get('user_id')

    if not paper_id or not user_id:
        return jsonify({"error": "Thiếu ID bài báo hoặc ID người chấm"}), 400

    try:
        # --- ĐOẠN NÀY KẾT NỐI DB (Code mẫu với psycopg2) ---
        # conn = get_db_connection()
        # cur = conn.cursor()
        # cur.execute("INSERT INTO assignments (paper_id, user_id) VALUES (%s, %s)", (paper_id, user_id))
        # conn.commit()
        # cur.close()
        # conn.close()
        # ---------------------------------------------------
        
        # Tạm thời trả về thành công giả lập để test Frontend
        print(f"Đã gán bài {paper_id} cho User {user_id}")
        return jsonify({"message": "Phân công thành công!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500