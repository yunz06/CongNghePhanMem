-- ============================================
-- UTH-ConfMS Database Schema
-- Member 1: Lâm Minh Phú - MSSV: 096206003648
-- ============================================

-- 1. Xóa bảng cũ nếu có (Để làm sạch)
DROP TABLE IF EXISTS audit_logs CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

-- 2. Tạo bảng Roles (Danh sách quyền hạn)
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL, -- admin, author, chair, reviewer
    description VARCHAR(255)
);

-- Thêm các quyền mặc định vào
INSERT INTO roles (name, description) VALUES
    ('admin', 'Quản trị viên hệ thống'),
    ('chair', 'Chủ tịch hội nghị'),
    ('reviewer', 'Người phản biện'),
    ('author', 'Tác giả (Mặc định)');

-- 3. Tạo bảng Users (Tài khoản người dùng)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL, -- Lưu chuỗi mã hóa
    fullname VARCHAR(255) NOT NULL,
    organization VARCHAR(255),
    role_id INTEGER REFERENCES roles(id) DEFAULT 4, -- Mặc định ID 4 là author
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tạo bảng Audit Logs (YÊU CẦU BẮT BUỘC CỦA BẠN)
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(255) NOT NULL, -- Lưu hành động: "Đăng nhập", "Đăng ký"...
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tạo 1 tài khoản Admin mẫu để test
-- Email: admin@uth.edu.vn
-- Pass: admin123 (Chuỗi bên dưới là hash của 'admin123' tạo bởi werkzeug)
INSERT INTO users (email, password_hash, fullname, role_id) VALUES 
('admin@uth.edu.vn', 'scrypt:32768:8:1$kPvQy9xS$a1b2c3d4e5f6...', 'System Admin', 1);