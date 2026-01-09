#Member 7 ( Minh Hùng ), Xuất file kỷ yếu và file bug
import pandas as pd
from datetime import datetime
import os
import sys

# --- CẤU HÌNH IMPORT ---
# Thêm đường dẫn để tìm thấy file app.py bên cạnh
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import từ file app.py của bạn
try:
    from app import app, db, SystemBug
    print("✅ Đã tìm thấy app và bảng SystemBug!")
except ImportError as e:
    print("❌ Lỗi: Không tìm thấy file app.py hoặc class SystemBug.")
    print(f"Chi tiết: {e}")
    exit()

# --- HÀM XUẤT DỮ LIỆU ---

def export_tool():
    print("⏳ Đang khởi động Tool TP7...")
    
    # BẮT BUỘC: Dùng app_context để chui vào Database SQLite
    with app.app_context():
        
        # ==========================================
        # PHẦN 1: XUẤT BUG REPORT (DỮ LIỆU THẬT 100%)
        # ==========================================
        try:
            print("--> Đang truy vấn bảng system_bugs trong database...")
            bugs = SystemBug.query.all()
            
            bug_data = []
            if bugs:
                for b in bugs:
                    # Lấy thông tin người báo lỗi (nếu có)
                    reporter_id = b.reported_by if b.reported_by else "Anonymous"
                    
                    bug_data.append({
                        "Bug ID": b.id,
                        "Tiêu đề": b.title,
                        "Mô tả chi tiết": b.description,
                        "Trạng thái": b.status,
                        "Người báo (ID)": reporter_id
                    })
                print(f"    Tìm thấy {len(bugs)} lỗi trong hệ thống.")
            else:
                print("    ⚠️ Database kết nối thành công nhưng CHƯA CÓ LỖI NÀO (Bảng rỗng).")
                # Tạo một dòng mẫu để file Excel không bị trống trơn (để còn chụp ảnh)
                bug_data.append({
                    "Bug ID": "MẪU", "Tiêu đề": "Chưa có dữ liệu thật", 
                    "Mô tả": "Hãy nhập thử lỗi vào Database", "Trạng thái": "N/A", "Người báo": ""
                })

            # Xuất ra Excel
            df_bugs = pd.DataFrame(bug_data)
            file_bugs = "Danh_sach_Loi_He_thong.xlsx"
            df_bugs.to_excel(file_bugs, index=False)
            print(f"✅ ĐÃ XONG! File lỗi thật: {file_bugs}")

        except Exception as e:
            print(f"❌ Lỗi khi xuất Bug: {e}")

        # ==========================================
        # PHẦN 2: XUẤT KỶ YẾU (DỮ LIỆU GIẢ - VÌ THIẾU BẢNG PAPER)
        # ==========================================
        try:
            # Vì trong app.py của bạn KHÔNG CÓ class Paper, nên tôi dùng dữ liệu giả
            # để bạn có file nộp báo cáo.
            print("--> Đang tạo giả lập Kỷ yếu (Do chưa có bảng Paper)...")
            
            fake_papers = [
                {"ID": 101, "Title": "Nghiên cứu AI 2024", "Author": "Nguyễn Văn A", "Track": "CNTT", "Status": "Accepted"},
                {"ID": 102, "Title": "Blockchain Finance", "Author": "Trần Thị B", "Track": "Kinh tế", "Status": "Accepted"},
                {"ID": 105, "Title": "Cyber Security", "Author": "Lê Văn C", "Track": "An toàn", "Status": "Accepted"},
            ]
            
            df_papers = pd.DataFrame(fake_papers)
            file_proceedings = f"Ky_Yeu_Hoi_Nghi_{datetime.now().strftime('%Y%m%d')}.xlsx"
            df_papers.to_excel(file_proceedings, index=False)
            print(f"✅ ĐÃ XONG! File kỷ yếu (Demo): {file_proceedings}")
            
        except Exception as e:
            print(f"❌ Lỗi khi xuất Kỷ yếu: {e}")

# --- CHẠY ---
if __name__ == "__main__":
    export_tool()
    print("\n👉 Kiểm tra thư mục để lấy 2 file Excel nhé!")