import pandas as pd
from datetime import datetime

print("⏳ Đang tiến hành tạo dữ liệu giả lập...")

# --- PHẦN 1: TẠO FILE KỶ YẾU (Proceedings) ---
data_ky_yeu = [
    {"Paper ID": "P-101", "Title": "Ứng dụng AI trong quản lý giao thông đô thị", "Authors": "Nguyễn Văn A, Trần Thị B", "Track": "Smart City", "Status": "Accepted"},
    {"Paper ID": "P-105", "Title": "Nghiên cứu Blockchain trong Logistics", "Authors": "Lê Văn C", "Track": "Logistics", "Status": "Accepted"},
    {"Paper ID": "P-112", "Title": "Tối ưu hóa năng lượng tái tạo", "Authors": "Phạm Minh D, Vũ E", "Track": "Green Energy", "Status": "Accepted"},
    {"Paper ID": "P-120", "Title": "Xây dựng Chatbot hỗ trợ sinh viên UTH", "Authors": "Nhóm SV K21", "Track": "Software Eng", "Status": "Accepted"},
    {"Paper ID": "P-125", "Title": "Phân tích dữ liệu lớn trong Y tế", "Authors": "Hoàng Y", "Track": "Big Data", "Status": "Accepted"},
]

df_ky_yeu = pd.DataFrame(data_ky_yeu)
file_ky_yeu = f"Ky_Yeu_Hoi_Nghi_Official_{datetime.now().strftime('%d%m%Y')}.xlsx"
df_ky_yeu.to_excel(file_ky_yeu, index=False, sheet_name="Accepted Papers")
print(f"✅ Đã tạo xong Kỷ yếu: {file_ky_yeu}")

# --- PHẦN 2: TẠO FILE BÁO CÁO LỖI (Bug Report) ---
data_loi = [
    {"Bug ID": "BUG-001", "Mô tả": "Lỗi đăng nhập sai Pass", "Mức độ": "High", "Trạng thái": "Fixed", "Assignee": "Dev 1"},
    {"Bug ID": "BUG-002", "Mô tả": "Nút Submit bị lệch trên Mobile", "Mức độ": "Medium", "Trạng thái": "Open", "Assignee": "Dev 2"},
    {"Bug ID": "BUG-003", "Mô tả": "Lỗi font chữ khi xuất PDF", "Mức độ": "Low", "Trạng thái": "Pending", "Assignee": "Leader"},
]

df_loi = pd.DataFrame(data_loi)
file_loi = f"Danh_sach_Loi_System_{datetime.now().strftime('%d%m%Y')}.xlsx"
df_loi.to_excel(file_loi, index=False, sheet_name="Bug Report")
print(f"✅ Đã tạo xong Báo cáo lỗi: {file_loi}")

print("\n👉 XONG! Bạn hãy mở thư mục backend và chụp ảnh 2 file Excel này nhé!")