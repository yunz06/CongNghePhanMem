import streamlit as st
import pandas as pd
import time

# 1. CẤU HÌNH TRANG (Phải để đầu tiên)
st.set_page_config(layout="wide", page_title="Hệ thống xét duyệt", page_icon="🎓")
st.markdown("""
    <h1 style='text-align: center; color: #2E4053;'>HỆ THỐNG XÉT DUYỆT BÀI BÁO KHOA HỌC</h1>
    <p style='text-align: center; color: #555;'>Hội đồng khoa học – Trường Đại học Giao thông vận tải TP.HCM</p>
    <hr>
""", unsafe_allow_html=True)

# 2. KHỞI TẠO DỮ LIỆU (Tránh lỗi màn hình trắng)
if "papers" not in st.session_state:
    st.session_state.papers = [
        {"id": 101, "title": "AI trong chẩn đoán y tế", "author": "Nguyễn Văn A", "score": 8.5, "status": "REVIEWED"},
        {"id": 102, "title": "Blockchain và IoT", "author": "Trần Thị B", "score": 4.5, "status": "REVIEWED"},
        {"id": 103, "title": "An toàn thông tin 2025", "author": "Lê Văn C", "score": 7.0, "status": "REVIEWED"},
        {"id": 104, "title": "Big Data trong giáo dục", "author": "Phạm Văn D", "score": 9.0, "status": "ACCEPTED"},
        {"id": 105, "title": "Tối ưu giao thông thông minh", "author": "Võ Văn E", "score": 6.5, "status": "REVIEWED"},
    ]



# 4. GIAO DIỆN CHÍNH
col1, col2 = st.columns([1.5, 1.5], gap="large")

# --- CỘT TRÁI: DANH SÁCH ---
with col1:
    st.subheader("📋 Danh sách bài báo")
    df = pd.DataFrame(st.session_state.papers)
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- CỘT PHẢI: CHỨC NĂNG ---
with col2:
    st.subheader("⚙️ Xử lý hồ sơ")
    
    # Placeholder thông báo
    msg_box = st.empty()

    # Chọn bài
    all_ids = [p["id"] for p in st.session_state.papers]
    selected_id = st.selectbox("Chọn Mã bài báo (ID):", all_ids)
    
    # Tìm bài tương ứng
    paper = next(p for p in st.session_state.papers if p["id"] == selected_id)

    # Hiện thông tin
    st.info(f"**{paper['title']}**\nTác giả: {paper['author']} | Điểm: {paper['score']}")
    
    # Hiện trạng thái
    st.write(f"Trạng thái hiện tại: **{paper['status']}**")

    # Nút Duyệt/Loại
    c1, c2 = st.columns(2)
    if c1.button("✅ DUYỆT BÀI", use_container_width=True):
        paper["status"] = "ACCEPTED"
        msg_box.success("Đã Duyệt!")
        time.sleep(0.5)
        st.rerun()
        
    if c2.button("❌ TỪ CHỐI", use_container_width=True):
        paper["status"] = "REJECTED"
        msg_box.error("Đã Từ chối!")
        time.sleep(0.5)
        st.rerun()

    # NÚT GỬI EMAIL (NẰM Ở ĐÂY)
    st.markdown("---")
    st.warning("👇 Gửi Email thông báo")
    
    if st.button("📧 GỬI EMAIL NGAY", type="primary", use_container_width=True):
        if paper["status"] == "REVIEWED":
            msg_box.error("⚠️ Phải DUYỆT hoặc TỪ CHỐI trước khi gửi mail!")
        else:
            with st.spinner("Đang kết nối máy chủ mail..."):
                time.sleep(2)
            msg_box.success(f"✅ Đã gửi email thành công cho {paper['author']}!")
            st.balloons()