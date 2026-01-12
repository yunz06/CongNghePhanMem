# MEMBER 7
# MÃ TASK: TP7 - Export Proceedings & Test Report
# MÔ TẢ: Module xuất Kỷ yếu (bài Accepted) và Báo cáo lỗi (System Bug) ra Excel

import pandas as pd
import os
from datetime import datetime

# --- HÀM 1: XUẤT DANH SÁCH LỖI (BUG) ---
def export_bugs_to_excel():
    print("\n[TASK 1] Đang thực hiện xuất Báo cáo lỗi...")
    
    # Import bên trong hàm để tránh lỗi vòng lặp (Circular Import)
    try:
        from app import app, SystemBug
    except ImportError:
        from app import app
        from models import SystemBug

    with app.app_context():
        bugs = SystemBug.query.all()
        
        data = []
        for bug in bugs:
            data.append({
                'Bug ID': bug.id,
                'Tiêu đề lỗi': bug.title,
                'Mô tả chi tiết': bug.description,
                'Trạng thái': bug.status,
                'Người phụ trách': bug.assigned_to
            })
        
        if data:
            df = pd.DataFrame(data)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Danh_sach_Loi_He_thong_{timestamp}.xlsx"
            
            df.to_excel(filename, index=False)
            full_path = os.path.abspath(filename)
            print(f"✅ THÀNH CÔNG: Đã xuất file lỗi tại: {full_path}")
        else:
            print("⚠️ THÔNG BÁO: Database hiện không có lỗi nào để xuất.")

# --- HÀM 2: XUẤT KỶ YẾU (BÀI BÁO ACCEPTED) ---
def export_proceedings_to_excel():
    print("\n[TASK 2] Đang thực hiện xuất Kỷ yếu Hội nghị...")

    try:
        from app import app, Paper
    except ImportError:
        from app import app
        try:
            from models import Paper
        except ImportError:
            print("❌ LỖI: Không tìm thấy model 'Paper'.")
            return

    with app.app_context():
        # Lọc bài có trạng thái ACCEPTED
        papers = Paper.query.filter(
            (Paper.status == 'accepted') | (Paper.status == 'ACCEPTED')
        ).all()
        
        data = []
        for p in papers:
            author_info = getattr(p, 'author_name', getattr(p, 'author_id', 'Unknown'))
            file_url = getattr(p, 'file_url', 'N/A')
            
            data.append({
                'Mã bài': p.id,
                'Tên bài báo': p.title,
                'Tác giả': author_info,
                'Trạng thái': p.status,
                'File bài': file_url
            })
            
        if data:
            df = pd.DataFrame(data)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Ky_Yeu_Hoi_Nghi_{timestamp}.xlsx"
            
            df.to_excel(filename, index=False)
            full_path = os.path.abspath(filename)
            print(f"✅ THÀNH CÔNG: Đã xuất Kỷ yếu tại: {full_path}")
        else:
            print("⚠️ THÔNG BÁO: Chưa có bài báo nào được Duyệt (Accepted).")

# --- CHẠY CHƯƠNG TRÌNH ---
if __name__ == "__main__":
    export_bugs_to_excel()
    print("-" * 30)
    export_proceedings_to_excel()