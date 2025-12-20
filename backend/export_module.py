
#  MEMBER 6 (Quan Tran)
# MÃ TASK: DEV-11 (TP7 - Export Proceedings to Excel)
# MÔ TẢ: Module xuất danh sách bài báo đạt yêu cầu ra file Excel


import pandas as pd
import os
from datetime import datetime

def export_accepted_papers_to_excel(paper_list):
    """
    Hàm lọc các bài đã được ACCEPTED và xuất ra file Excel
    """
    # 1. Lọc dữ liệu: Chỉ lấy bài có trạng thái ACCEPTED
    accepted_papers = [p for p in paper_list if p.get('status') == 'ACCEPTED' or p.get('Trạng thái') == 'ACCEPTED']
    
    if not accepted_papers:
        return {"success": False, "message": "Không có bài nào được duyệt để xuất file."}

    # 2. Tạo DataFrame (Bảng dữ liệu)
    df = pd.DataFrame(accepted_papers)
    
    # 3. Đặt tên file theo thời gian thực (để không bị trùng)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Ky_Yeu_Hoi_Nghi_{timestamp}.xlsx"
    
    # 4. Xuất file Excel
    try:
        # Yêu cầu cài thư viện: pip install openpyxl
        df.to_excel(filename, index=False, sheet_name='Accepted Papers')
        
        # Lấy đường dẫn tuyệt đối để báo cáo
        full_path = os.path.abspath(filename)
        print(f"--- LOG: Đã xuất file thành công tại: {full_path}")
        
        return {"success": True, "filename": filename, "path": full_path}
    except Exception as e:
        return {"success": False, "message": str(e)}

# --- TEST THỬ NGHIỆM (Unit Test) ---
if __name__ == "__main__":
    # Dữ liệu giả lập để test hàm
    mock_data = [
        {"id": 101, "title": "Bài báo A", "author": "Nguyen Van A", "status": "ACCEPTED"},
        {"id": 102, "title": "Bài báo B", "author": "Tran Thi B", "status": "REJECTED"},
        {"id": 104, "title": "Bài báo C", "author": "Pham Van D", "status": "ACCEPTED"}
    ]
    
    print("Đang chạy test xuất Excel...")
    result = export_accepted_papers_to_excel(mock_data)
    print("Kết quả:", result)