# 🎓 UTH-ConfMS - Hệ thống Quản lý Hội nghị Khoa học

[![Status](https://img.shields.io/badge/Status-Completed-brightgreen)]()
[![Role](https://img.shields.io/badge/Role-Member%201%20(Leader)-orange)]()
[![Tech](https://img.shields.io/badge/Stack-React%20%7C%20Flask%20%7C%20PostgreSQL-blue)]()

---

## 👤 Thông tin sinh viên
- **Họ và tên:** Lâm Minh Phú
- **MSSV:** 096206003648
- **Vai trò:** Member 1 (Leader) & System Architect
- **Nhiệm vụ:**
  - Xây dựng **Authentication System** (Đăng ký/Đăng nhập bảo mật).
  - Thiết kế **Database nền tảng** (Users, Roles).
  - Phát triển **Audit System** (Ghi nhật ký hoạt động hệ thống).

---

## 🏗️ Cấu trúc bài nộp

```text
UTH-ConfMS/
├── 📁 database/                # SQL Scripts
│   └── create_users_table.sql  # Tạo bảng Users & Audit Logs
│
├── 📁 backend/                 # Flask API
│   ├── app.py                  # API Logic (Auth + Audit)
│   └── requirements.txt        # Thư viện (Flask, Werkzeug...)
│
├── 📁 frontend/                # React App
│   └── src/
│       ├── pages/              # (NEW) Thư mục chứa các trang
│       │   ├── LoginPage.js    # Giao diện Đăng nhập
│       │   ├── LoginPage.css   # Style cho trang đăng nhập
│       │   ├── RegisterPage.js # Giao diện Đăng ký
│       │   └── RegisterPage.css# Style cho trang đăng ký
│       │
│       ├── App.js              # Điều hướng (Router)
│       ├── index.js            # Entry point (Khởi chạy App)
│       └── App.css             # Style toàn cục
│
├── 📁 docs/                    # Tài liệu
│   ├── SRS_Login_Register.md   # Đặc tả yêu cầu
│   └── UseCase_Login_Register.html # Sơ đồ Use Case
│
└── 📄 README.md                # File giới thiệu này

# Đồ án Công Nghệ Phần Mềm

## 🔗 Link Tài Nguyên Quan Trọng (Nhóm Zalo)
* **GitHub Repository:** https://github.com/yunz06/CongNghePhanMem
* **Quản lý dự án (Jira):** https://nhomcnpm.atlassian.net
* **Cơ sở dữ liệu (Neon DB):** https://console.neon.tech/app/projects/young-meadow-72778146