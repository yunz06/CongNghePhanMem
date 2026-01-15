# TP7 - Xuất Kỷ Yếu & Bug Report
# Member 7 - Minh Hùng (đã chỉnh cho UTH-ConfMS)

import requests
import pandas as pd
from datetime import datetime

API_BASE = "http://127.0.0.1:5000/api/decision"

def export_tp7():
    print("⏳ Bắt đầu Tool TP7...")

    # ==============================
    # PHẦN 1: XUẤT KỶ YẾU (THẬT)
    # ==============================
    try:
        print("👉 Đang lấy danh sách bài báo từ Backend...")
        res = requests.get(f"{API_BASE}/papers")

        if res.status_code != 200:
            print("❌ Không lấy được dữ liệu bài báo")
            return

        papers = res.json()["data"]

        accepted = [
            {
                "Mã bài": p["id"],
                "Tên bài": p["title"],
                "Tác giả": p["author"],
                "Điểm": p["score"],
                "Trạng thái": p["status"]
            }
            for p in papers if p["status"] == "ACCEPTED"
        ]

        if not accepted:
            accepted.append({
                "Mã bài": "N/A",
                "Tên bài": "Chưa có bài được duyệt",
                "Tác giả": "",
                "Điểm": "",
                "Trạng thái": ""
            })

        df = pd.DataFrame(accepted)
        file_kyyeu = f"KyYeu_HoiNghi_{datetime.now().strftime('%Y%m%d')}.xlsx"
        df.to_excel(file_kyyeu, index=False)

        print(f"✅ Xuất kỷ yếu thành công: {file_kyyeu}")

    except Exception as e:
        print("❌ Lỗi xuất kỷ yếu:", e)

    # ==============================
    # PHẦN 2: BUG REPORT (MÔ PHỎNG)
    # ==============================
    try:
        print("👉 Tạo Bug Report mô phỏng...")

        bugs = [
            {"Bug ID": 1, "Mô tả": "Không đăng nhập được khi sai mật khẩu", "Trạng thái": "Fixed"},
            {"Bug ID": 2, "Mô tả": "Không gửi mail khi thiếu App Password", "Trạng thái": "Fixed"},
            {"Bug ID": 3, "Mô tả": "Reset bị chặn khi chưa login admin", "Trạng thái": "Known issue"}
        ]

        df_bug = pd.DataFrame(bugs)
        file_bug = "DanhSachBug_TP7.xlsx"
        df_bug.to_excel(file_bug, index=False)

        print(f"✅ Xuất Bug Report thành công: {file_bug}")

    except Exception as e:
        print("❌ Lỗi xuất bug:", e)

if __name__ == "__main__":
    export_tp7()
    print("\n🎯 Hoàn tất TP7 – kiểm tra file Excel trong thư mục.")