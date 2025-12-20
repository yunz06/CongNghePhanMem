import pandas as pd
from app import app, db, SystemBug 
# Nếu nhóm bạn có bảng 'Paper' thì thêm vào dòng trên: from app import Paper

def export_bugs_to_excel():
    with app.app_context():
        # 1. Lấy toàn bộ dữ liệu từ bảng Lỗi
        bugs = SystemBug.query.all()
        
        # 2. Chuyển đổi dữ liệu thành danh sách
        data = []
        for bug in bugs:
            data.append({
                'ID': bug.id,
                'Tiêu đề': bug.title,
                'Mô tả': bug.description,
                'Trạng thái': bug.status
            })
        
        # 3. Tạo file Excel bằng Pandas
        if data:
            df = pd.DataFrame(data)
            filename = "Danh_sach_Loi_He_thong.xlsx"
            df.to_excel(filename, index=False)
            print(f"--> Đã xuất thành công file: {filename}")
        else:
            print("--> Không có dữ liệu để xuất!")

if __name__ == "__main__":
    export_bugs_to_excel()