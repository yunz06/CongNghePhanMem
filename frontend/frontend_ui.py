import streamlit as st
import requests
import time

# --- CẤU HÌNH ---
API = "http://127.0.0.1:5000/api/decision"
st.set_page_config(page_title="Hệ thống Xét duyệt", layout="wide")

# --- CSS (Giữ nguyên cho đẹp) ---
st.markdown("""
<style>
    [data-testid="stSidebar"] h1 { font-size: 30px !important; color: #0d47a1 !important; text-transform: uppercase; }
    .info-box { text-align: left !important; color: #546e7a !important; font-weight: bold; }
    [data-testid="stSidebar"] button { background-color: #007bff !important; color: white !important; }
    .stButton button[kind="primary"] { background-color: #28a745 !important; color: white !important; }
    .stButton button[kind="secondary"] { color: #dc3545 !important; border: 1px solid #dc3545 !important; background-color: white !important; }
    .status-box { padding: 5px; border-radius: 5px; text-align: center; font-weight: bold; font-size: 14px; }
    .accepted { background-color: #E6F4EA; color: #1E8E3E; }
    .rejected { background-color: #FCE8E6; color: #D93025; }
    .waiting { background-color: #F3F4F6; color: #5F6368; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: NƠI NHẬP TÀI KHOẢN ADMIN ---
with st.sidebar:
    st.image("https://portal.ut.edu.vn/images/logo_full.png", width=250)
    st.title("Admin Portal")
    st.markdown('<div class="info-box">TP6 - Decision Support</div>', unsafe_allow_html=True)
    st.divider()

    # --- KHU VỰC CẤU HÌNH EMAIL ---
    st.markdown("### Nhập tài khoảng Admin")
    
    
    # Ô nhập Email Admin
    admin_email = st.text_input("Gmail của bạn:", placeholder="admin@gmail.com")
    # Ô nhập Pass Admin (ẩn ký tự bằng type='password')
    admin_pass = st.text_input("Mật khẩu ứng dụng:", type="password", help="Mã 16 ký tự Google cấp")
    
    st.divider()
    
    st.subheader("Báo cáo (TP7)")
    if st.button("📥 Xuất Kỷ Yếu (.xlsx)", type="primary"):
        try:
            res = requests.get(f"{API}/export")
            if res.status_code == 200:
                st.download_button("Tải file về", res.content, "KyYeu.xlsx")
        except: st.error("Lỗi Server!")

    st.write(""); st.write("")
    if st.button("🔄 Reset Dữ liệu"):
        requests.post(f"{API}/reset")
        st.rerun()

# --- MAIN PAGE ---
st.title("HỘI ĐỒNG XÉT DUYỆT")

try:
    res = requests.get(f"{API}/papers")
    papers = res.json()['data'] if res.status_code == 200 else []
except: papers = []

if not papers:
    st.error("⚠️ Hãy chạy Backend: python run_server.py")
else:
    c1, c2, c3 = st.columns(3)
    c1.metric("Tổng hồ sơ", len(papers))
    c2.metric("Đã Duyệt", len([p for p in papers if p['status']=='ACCEPTED']))
    c3.metric("Chờ xử lý", len([p for p in papers if p['status']=='REVIEWED']))
    st.divider()

    for p in papers:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1.5])
            with col1:
                st.subheader(p['title'])
                st.text(f"TG: {p['author']} | Điểm: {p['score']}")
                
                # --- GỬI MAIL LINH HOẠT ---
                if p['status'] != 'REVIEWED':
                    with st.expander(f"📧 Gửi Email thông báo"):
                        # Ô nhập người nhận (Người dùng tự nhập)
                        email_to = st.text_input("Người nhận:", value="", key=f"mail_{p['id']}", placeholder="nhap_email_nguoi_nhan@gmail.com")
                        
                        if st.button("📤 Gửi ngay", key=f"btn_{p['id']}"):
                            # 1. Kiểm tra đã nhập tài khoản Admin chưa
                            if not admin_email or not admin_pass:
                                st.error("❌ Vui lòng nhập Gmail & Mật khẩu ứng dụng ở thanh bên trái (Sidebar) trước!")
                            # 2. Kiểm tra đã nhập người nhận chưa
                            elif not email_to:
                                st.warning("Vui lòng nhập email người nhận!")
                            else:
                                with st.spinner("Đang đăng nhập và gửi..."):
                                    # Gửi tất cả thông tin xuống Backend
                                    payload = {
                                        "id": p['id'],
                                        "email_to": email_to,       # Gửi cho ai
                                        "sender_email": admin_email, # Gửi bằng tài khoản nào
                                        "sender_pass": admin_pass    # Mật khẩu là gì
                                    }
                                    api = requests.post(f"{API}/send-email", json=payload)
                                    
                                    if api.status_code == 200:
                                        st.success(f"✅ Đã gửi thành công tới {email_to}")
                                    else:
                                        st.error(f"Lỗi: {api.json().get('message')}")

            with col2:
                if p['status'] == 'ACCEPTED': st.markdown('<div class="status-box accepted">Đã Duyệt</div>', unsafe_allow_html=True)
                elif p['status'] == 'REJECTED': st.markdown('<div class="status-box rejected">Đã Loại</div>', unsafe_allow_html=True)
                else: st.markdown('<div class="status-box waiting">Đang chờ</div>', unsafe_allow_html=True)

            with col3:
                if p['status'] == 'REVIEWED':
                    c1, c2 = st.columns(2)
                    if c1.button("Duyệt", key=f"ok_{p['id']}", type="primary"):
                        requests.post(f"{API}/make", json={"paper_id": p['id'], "decision": "ACCEPTED"})
                        st.rerun()
                    if c2.button("Loại", key=f"no_{p['id']}", type="secondary"):
                        requests.post(f"{API}/make", json={"paper_id": p['id'], "decision": "REJECTED"})
                        st.rerun()