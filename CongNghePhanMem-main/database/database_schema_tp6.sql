-- 
-- PROJECT: UTH-ConfMS (Conference Management System)
-- MODULE: TP6 - Decision Making (Ra Quyết Định)
-- TÁC GIẢ: Member 6 (Quan Tran)
-- TASK ID: DEV-8
-- 

-- 1. Bảng Bài Báo (Papers)
-- Cập nhật trạng thái bài báo để phục vụ quy trình xét duyệt
CREATE TABLE papers (
    paper_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    author_name VARCHAR(100),
    abstract TEXT,
    -- Trạng thái: SUBMITTED (Mới nộp) -> REVIEWED (Đã chấm) -> ACCEPTED/REJECTED (Đã duyệt/Loại)
    status ENUM('SUBMITTED', 'REVIEWED', 'ACCEPTED', 'REJECTED') DEFAULT 'SUBMITTED',
    average_score DECIMAL(4, 2), -- Điểm trung bình từ Reviewer
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Bảng Quyết Định (Decisions)
-- Lưu lại lịch sử ai là người duyệt bài vào thời gian nào
CREATE TABLE decisions (
    decision_id INT PRIMARY KEY AUTO_INCREMENT,
    paper_id INT NOT NULL,
    decision_maker VARCHAR(100) NOT NULL, -- Tên người duyệt (Program Chair)
    result ENUM('ACCEPTED', 'REJECTED') NOT NULL,
    comments TEXT, -- Nhận xét gửi kèm email
    decision_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
);
