# 🛡️ UTH-ConfMS: Backend Core System

**Sinh viên:** Lâm Minh Phú - 096206003648  
**Vai trò:** Leader & System Architect

## ✅ Nhiệm vụ TP1 đã làm

1. **Database:** Thiết kế bảng `users` (phân quyền) & `audit_logs`.
2. **Auth API:** Đăng ký/Đăng nhập (Password Hashing an toàn).
3. **Audit System:** Tự động ghi log mọi thay đổi quan trọng.
4. **Middleware:** Chặn quyền truy cập Admin (`@admin_required`).

## 📂 Cấu trúc dự án (Backend)

```text
backend/
├── app.py              # Khởi chạy App, cấu hình DB & JWT
├── models.py           # Định nghĩa bảng Users & AuditLogs
├── routes/             # Xử lý API
│   ├── auth.py         # API Đăng ký, Đăng nhập
│   └── admin.py        # API Quản lý User (dành cho Admin)
├── utils/              # Tiện ích hỗ trợ
│   ├── audit.py        # Hàm ghi log hệ thống (log_action)
│   └── decorators.py   # Middleware kiểm tra quyền Admin
└── requirements.txt    # Các thư viện cần thiết