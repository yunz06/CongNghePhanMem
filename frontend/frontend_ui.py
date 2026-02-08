import streamlit as st
import requests
import time

# --- CẤU HÌNH ---
API_BASE = "http://127.0.0.1:5000/api/decision"
st.set_page_config(page_title="Cổng thông tin UTH", layout="wide", page_icon="🎓")

# --- CSS (Ẩn Sidebar khi chưa Login & Làm đẹp) ---
st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none; }
    %s
    .main-header { font-size: 28px; color: #003366; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .status-box { padding: 5px; border-radius: 5px; text-align: center; font-weight: bold; }
    .accepted { background-color: #d4edda; color: #155724; }
    .rejected { background-color: #f8d7da; color: #721c24; }
    .waiting { background-color: #fff3cd; color: #856404; }
</style>
""" % ("" if not st.session_state.get('logged_in') else "[data-testid='stSidebar'] { display: block !important; }"), unsafe_allow_html=True)

# --- QUẢN LÝ STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'role' not in st.session_state: st.session_state.role = "" 
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'user_pass' not in st.session_state: st.session_state.user_pass = ""

# ==========================================
# DASHBOARD CHO ADMIN
# ==========================================
def admin_dashboard():
    with st.sidebar:
        st.image("https://portal.ut.edu.vn/images/logo_full.png", width=200)
        st.info(f"Admin: {st.session_state.user_email}")
        
        if st.button("🚪 Đăng xuất"):
            st.session_state.logged_in = False
            st.rerun()
            
        st.divider()
        
        # NÚT XUẤT EXCEL
        st.write("### Công cụ")
        if st.button("📥 Xuất Kỷ Yếu (.xlsx)"):
            try:
                res = requests.get(f"{API_BASE}/export")
                if res.status_code == 200:
                    st.download_button(
                        label="Bấm vào đây để tải về máy",
                        data=res.content,
                        file_name="KyYeu_HoiNghi.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        type="primary"
                    )
                else:
                    st.error(f"Lỗi Server: {res.json().get('message', 'Không rõ')}")
            except Exception as e: st.error(f"Lỗi kết nối: {e}")

        if st.button("🔄 Reset Dữ liệu"):
            requests.post(f"{API_BASE}/reset")
            st.rerun()

    st.markdown('<div class="main-header">📋 HỘI ĐỒNG XÉT DUYỆT</div>', unsafe_allow_html=True)
    
    try:
        papers = requests.get(f"{API_BASE}/papers").json().get('data', [])
    except: papers = []

    # Thống kê (Đã fix thụt lề c2.metric)
    c1, c2, c3 = st.columns(3)
    c1.metric("Tổng hồ sơ", len(papers))
    c2.metric("Đã Duyệt", len([p for p in papers if p['status']=='ACCEPTED']))
    c3.metric("Chờ xử lý", len([p for p in papers if p['status']=='REVIEWED']))
    st.write("---")

    # Danh sách bài báo
    for p in papers:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1.5])
            
            with col1:
                st.subheader(p['title'])
                st.caption(f"Tác giả: {p['author']} | File: {p.get('filename','N/A')}")
                
                if p['status'] != 'REVIEWED':
                    with st.expander("📧 Gửi Email kết quả"):
                        email_to = st.text_input("Gửi tới:", value=p['author'], key=f"m_{p['id']}")
                        if st.button("Gửi ngay", key=f"s_{p['id']}"):
                            with st.spinner("Đang gửi..."):
                                res = requests.post(f"{API_BASE}/send-email", json={
                                    "id": p['id'], "email_to": email_to,
                                    "sender_email": st.session_state.user_email,
                                    "sender_pass": st.session_state.user_pass
                                })
                                if res.status_code == 200: st.toast("Đã gửi mail!", icon="✅")
                                else: st.error("Lỗi gửi mail!")

            with col2:
                if p['status']=='ACCEPTED': st.markdown('<div class="status-box accepted">Đã Duyệt</div>', unsafe_allow_html=True)
                elif p['status']=='REJECTED': st.markdown('<div class="status-box rejected">Đã Loại</div>', unsafe_allow_html=True)
                else: st.markdown('<div class="status-box waiting">Chờ duyệt</div>', unsafe_allow_html=True)

            with col3:
                if p['status']=='REVIEWED':
                    c_ok, c_no = st.columns(2)
                    if c_ok.button("✅", key=f"ok_{p['id']}"):
                        requests.post(f"{API_BASE}/make", json={"paper_id": p['id'], "decision": "ACCEPTED"})
                        st.rerun()
                    if c_no.button("❌", key=f"no_{p['id']}"):
                        requests.post(f"{API_BASE}/make", json={"paper_id": p['id'], "decision": "REJECTED"})
                        st.rerun()

# ==========================================
# DASHBOARD CHO SINH VIÊN
# ==========================================
def student_dashboard():
    with st.sidebar:
        st.image("https://portal.ut.edu.vn/images/logo_full.png", width=200)
        st.success(f"SV: {st.session_state.user_email}")
        if st.button("🚪 Đăng xuất"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown('<div class="main-header">📤 NỘP ĐỀ TÀI KHOA HỌC</div>', unsafe_allow_html=True)
    
    with st.form("submit_form", clear_on_submit=True):
        st.write("Điền thông tin đề tài:")
        # Fix thụt lề f_title
        f_title = st.text_input("Tên đề tài")
        f_abstract = st.text_area("Tóm tắt nội dung")
        f_file = st.file_uploader("File báo cáo", type=['pdf', 'docx'])
        
        if st.form_submit_button("🚀 Gửi hồ sơ", type="primary", use_container_width=True):
            if not f_title or not f_file: st.error("Thiếu thông tin!")
            else:
                files = {'file': (f_file.name, f_file.getvalue(), f_file.type)}
                data = {'title': f_title, 'abstract': f_abstract, 'author': st.session_state.user_email}
                requests.post(f"{API_BASE}/submit", data=data, files=files)
                st.success("Nộp thành công! Hãy đợi Admin duyệt.")

# ==========================================
# TRANG LOGIN / REGISTER
# ==========================================
def auth_page():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image("https://portal.ut.edu.vn/images/logo_full.png", use_container_width=True)
        st.markdown("<h3 style='text-align:center; color:#003366'>CỔNG THÔNG TIN ĐIỆN TỬ</h3>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🎓 SV Đăng Nhập", "📝 SV Đăng Ký", "🛡️ Admin Login"])

        with tab1:
            with st.form("sv_log"):
                e = st.text_input("Email SV")
                p = st.text_input("Mật khẩu", type="password")
                if st.form_submit_button("Đăng nhập", type="primary", use_container_width=True):
                    res = requests.post(f"{API_BASE}/student/login", json={"email":e, "password":p})
                    if res.status_code==200:
                        st.session_state.logged_in=True
                        st.session_state.role="student"
                        st.session_state.user_email=e
                        st.rerun()
                    else: st.error("Sai thông tin!")

        with tab2:
            with st.form("sv_reg"):
                re = st.text_input("Email")
                rp = st.text_input("Mật khẩu", type="password")
                r2 = st.text_input("Nhập lại mật khẩu", type="password")
                if st.form_submit_button("Đăng ký", use_container_width=True):
                    if rp!=r2: st.error("Mật khẩu không khớp")
                    else:
                        requests.post(f"{API_BASE}/student/register", json={"email":re, "password":rp})
                        st.success("Đăng ký thành công! Hãy đăng nhập.")

        with tab3:
            with st.form("ad_log"):
                ae = st.text_input("Gmail Admin")
                ap = st.text_input("App Password", type="password")
                if st.form_submit_button("Vào Hội Đồng", type="secondary", use_container_width=True):
                    # Fix thụt lề res ở đây
                    res = requests.post(f"{API_BASE}/admin/login", json={"email":ae, "password":ap})
                    if res.status_code==200:
                        st.session_state.logged_in=True
                        st.session_state.role="admin"
                        st.session_state.user_email=ae
                        st.session_state.user_pass=ap
                        st.rerun()
                    else: st.error("Sai thông tin Admin!")

# Điều hướng chính
if not st.session_state.logged_in:
    auth_page()
else:
    if st.session_state.role == "student": student_dashboard()
    else: admin_dashboard()