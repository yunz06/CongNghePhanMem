from app import app, db, SystemBug

def create_fake_bugs():
    with app.app_context():
        # Tạo 3 cái lỗi giả
        bug1 = SystemBug(title="Lỗi đăng nhập", description="Không đăng nhập được bằng Gmail", status="Open")
        bug2 = SystemBug(title="Lỗi font chữ", description="Font chữ bị lỗi ở trang chủ", status="Fixed")
        bug3 = SystemBug(title="Nút bấm bị liệt", description="Nút Submit không bấm được", status="Open")

        # Lưu vào Database
        db.session.add(bug1)
        db.session.add(bug2)
        db.session.add(bug3)
        db.session.commit()
        
        print("--> Đã thêm thành công 3 lỗi giả vào Database!")

if __name__ == "__main__":
    create_fake_bugs()