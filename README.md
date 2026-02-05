# UTH-ConfMS - Hệ thống quản lý hội nghị khoa học

**Đề tài**: Hệ thống quản lý hội nghị khoa học (UTH-ConfMS)  
**Giảng viên hướng dẫn**: Nguyễn Văn Chiến  
**Ngôn ngữ lập trình**: 100% Python  
**Link repo**: https://github.com/yunz06/CongNghePhanMem  

## Giới thiệu dự án (Chapter 1)

### 1.1. Project Context
Trong môi trường học thuật hiện đại, việc tổ chức hội nghị khoa học là nhiệm vụ phức tạp bao gồm quản lý hàng trăm bài báo nghiên cứu, phối hợp với nhiều reviewer và giao tiếp với tác giả. **Đại học Giao thông Vận tải TP.HCM (UTH)** thường xuyên tổ chức các sự kiện học thuật này để thúc đẩy nghiên cứu và hợp tác.

Tuy nhiên, khối lượng công việc hành chính cho Ban Tổ chức và Program Committee thường quá tải. Các nhiệm vụ chính như theo dõi bài nộp, phân công reviewer, tổng hợp điểm và thông báo cho tác giả thường được xử lý thủ công. Để giải quyết, nhóm đã phát triển **UTH-ConfMS** – hệ thống giúp số hóa và tự động hóa các quy trình quyết định và báo cáo quan trọng của hội nghị khoa học.

### 1.2. Problem Statement
- Quản lý dữ liệu thủ công (Excel, giấy tờ) → dễ lỗi, phân mảnh dữ liệu.
- Gửi email thông báo thủ công → chậm trễ, không đồng nhất.
- Thiếu dashboard tập trung để Program Chair xem điểm tổng hợp và quyết định.
- Xuất kỷ yếu hội nghị thủ công → tốn thời gian, dễ lỗi định dạng.
- Không có cơ chế theo dõi bug hệ thống.

### 1.3. Project Objectives
#### General Objectives
- Giảm thiểu công việc thủ công.
- Đảm bảo độ chính xác dữ liệu.
- Chuyên nghiệp hóa giao tiếp với tác giả.

#### Specific Technical Objectives
- TP6: Decision Making (Accept/Reject bài báo).
- TP7: Automated Email Notification & Export Proceedings (Excel).
- TP4: Reviewer Assignment.
- Bug Tracking.

### 1.4. Project Scope
- Backend: Flask + Blueprints.
- Frontend Dashboard: Streamlit.
- Database: SQLite + SQLAlchemy.
- Target users: Admin & Program Chair.

### 1.5. Technology Stack
- Python 3.x
- Flask
- Streamlit
- SQLAlchemy + SQLite
- Pandas + OpenPyXL
- smtplib (email)

### 1.6. Business Process (BPMN)
Quy trình gồm 6 bước chính: Initialization → Submission → Review → Decision (TP6) → Notification (TP7) → Publication.

## Phân công thành viên (khớp chính xác báo cáo)

| Chương | Nội dung phụ trách                          | Thành viên thực hiện                  | Ghi chú                                      |
|--------|---------------------------------------------|---------------------------------------|----------------------------------------------|
| I      | Project Introduction                        | Lâm Minh Phú (Leader)                 | Overview, Objectives, Scope                  |
| II     | Project Management                          | Nguyễn Văn Hiếu                       | Planning, Sprints, Tools                     |
| III    | Software Requirements                       | Lê Văn Đạt                            | Use Cases, Functional Requirements (SRS)     |
| IV (Part 1) | System Design (Database & Architecture) | Nguyễn Tiến Phát Đạt                  | Database Design (ERD), System Architecture   |
| IV (Part 2) | System Design (Class, Sequence, API)    | Đỗ Vũ Khang<br>Quách Vĩnh Viễn        | Class Diagram, Sequence, API                 |
| Extra  | Authentication (Login/Logout)               | Quách Vĩnh Tiến                       | Authentication Flow, Login/Logout Interface, Security |
| V      | Software Testing                            | Trần Minh Quân                        | Test Plan, Test Cases                        |
| VI     | Release & User Guide                        | Ngô Phú Minh Hùng                     | Proceedings Export, Bug Reports, User Guide   |

## Quy trình làm việc (Scrum – 4 Sprint)
- **Sprint 1** (Week 1-2): Initialization & Setup.
- **Sprint 2** (Week 3-4): Submission & Review.
- **Sprint 3** (Week 5-6): Decision & Notification (TP6 focus).
- **Sprint 4** (Week 7-8): Publication & Export (TP7 focus).

Công cụ: Jira, GitHub, Risk Management table (xem báo cáo chi tiết).



