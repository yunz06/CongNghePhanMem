# Software Requirements Specification (SRS)
# Module: Authentication (Login & Register)
## UTH-ConfMS - Hệ thống Quản lý Hội nghị

---

## 1. Giới thiệu

### 1.1 Mục đích
Tài liệu này mô tả các yêu cầu chức năng và phi chức năng cho module Xác thực người dùng (Authentication) của hệ thống UTH-ConfMS.

### 1.2 Phạm vi
Module này bao gồm:
- Đăng ký tài khoản mới (Register)
- Đăng nhập hệ thống (Login)
- Quản lý phiên đăng nhập (Session)

### 1.3 Đối tượng sử dụng
- Author (Tác giả nộp bài)
- Reviewer (Người phản biện)
- Chair (Chủ tịch hội nghị)
- Admin (Quản trị viên)

---

## 2. Mô tả tổng quan

### 2.1 Actors (Tác nhân)
| Actor | Mô tả |
|-------|-------|
| Guest | Người dùng chưa đăng nhập, có thể đăng ký hoặc đăng nhập |
| User | Người dùng đã đăng nhập với vai trò cụ thể |

### 2.2 Use Cases

#### UC-01: Đăng ký tài khoản (Register)
- **Mô tả**: Cho phép Guest tạo tài khoản mới trong hệ thống
- **Actor**: Guest
- **Precondition**: Guest chưa có tài khoản
- **Postcondition**: Tài khoản được tạo, Guest trở thành User

**Luồng chính:**
1. Guest truy cập trang đăng ký
2. Guest nhập thông tin: Email, Mật khẩu, Họ tên, Đơn vị
3. Hệ thống validate thông tin
4. Hệ thống tạo tài khoản mới với role mặc định "Author"
5. Hệ thống hiển thị thông báo thành công
6. Chuyển hướng đến trang đăng nhập

**Luồng ngoại lệ:**
- 3a. Email đã tồn tại → Hiển thị lỗi "Email đã được sử dụng"
- 3b. Mật khẩu không đủ mạnh → Hiển thị yêu cầu mật khẩu
- 3c. Thông tin không hợp lệ → Hiển thị lỗi cụ thể

#### UC-02: Đăng nhập (Login)
- **Mô tả**: Cho phép Guest xác thực và truy cập hệ thống
- **Actor**: Guest
- **Precondition**: Guest có tài khoản hợp lệ
- **Postcondition**: Guest trở thành User với session hợp lệ

**Luồng chính:**
1. Guest truy cập trang đăng nhập
2. Guest nhập Email và Mật khẩu
3. Hệ thống xác thực thông tin
4. Hệ thống tạo session/token
5. Chuyển hướng đến Dashboard theo role

**Luồng ngoại lệ:**
- 3a. Email không tồn tại → Hiển thị lỗi "Thông tin đăng nhập không đúng"
- 3b. Mật khẩu sai → Hiển thị lỗi "Thông tin đăng nhập không đúng"
- 3c. Tài khoản bị khóa → Hiển thị lỗi "Tài khoản đã bị khóa"

---

## 3. Yêu cầu chức năng

### FR-01: Đăng ký
| ID | Yêu cầu | Độ ưu tiên |
|----|---------|------------|
| FR-01.1 | Hệ thống phải cho phép đăng ký với email, password, fullname, organization | Cao |
| FR-01.2 | Email phải là duy nhất trong hệ thống | Cao |
| FR-01.3 | Password phải có ít nhất 6 ký tự | Cao |
| FR-01.4 | Hệ thống tự gán role "author" cho user mới | Cao |

### FR-02: Đăng nhập
| ID | Yêu cầu | Độ ưu tiên |
|----|---------|------------|
| FR-02.1 | Hệ thống phải xác thực bằng email và password | Cao |
| FR-02.2 | Hệ thống phải tạo JWT token khi đăng nhập thành công | Cao |
| FR-02.3 | Token phải hết hạn sau 24 giờ | Trung bình |

---

## 4. Yêu cầu phi chức năng

| ID | Yêu cầu | Mô tả |
|----|---------|-------|
| NFR-01 | Bảo mật | Password phải được hash bằng bcrypt |
| NFR-02 | Hiệu năng | API phải phản hồi trong 2 giây |
| NFR-03 | Khả dụng | Hệ thống hoạt động 99% thời gian |

---

## 5. API Endpoints

| Method | Endpoint | Mô tả | Request Body | Response |
|--------|----------|-------|--------------|----------|
| POST | /api/register | Đăng ký | {email, password, fullname, organization} | {message, user_id} |
| POST | /api/login | Đăng nhập | {email, password} | {token, user} |

---

## 6. Database Schema

### Bảng: users
| Column | Type | Constraint | Description |
|--------|------|------------|-------------|
| id | SERIAL | PRIMARY KEY | ID người dùng |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email đăng nhập |
| password_hash | VARCHAR(255) | NOT NULL | Mật khẩu đã hash |
| fullname | VARCHAR(255) | NOT NULL | Họ và tên |
| organization | VARCHAR(255) | | Đơn vị/Trường |
| role | VARCHAR(50) | DEFAULT 'author' | Vai trò |
| created_at | TIMESTAMP | DEFAULT NOW() | Thời gian tạo |
| is_active | BOOLEAN | DEFAULT TRUE | Trạng thái |

---

**Người viết:** Lâm Minh Phú - MSSV: 096206003648
**Ngày tạo:** [Ngày hiện tại]
**Phiên bản:** 1.0
