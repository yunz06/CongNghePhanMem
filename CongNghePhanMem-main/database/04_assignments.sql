-- [TP4] TABLE ASSIGNMENTS
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    paper_id INT NOT NULL,
    user_id INT NOT NULL,
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',
    
    -- Khóa ngoại (Giả định bảng papers và users đã tồn tại)
    CONSTRAINT fk_assignment_paper FOREIGN KEY (paper_id) REFERENCES papers(id),
    CONSTRAINT fk_assignment_user FOREIGN KEY (user_id) REFERENCES users(id)
);