import streamlit as st
import requests

# =====================
# API CONFIG (DÙNG MOCK)
# =====================
API_BASE = "http://127.0.0.1:5000/api"
API_AUTH_LOGIN = f"{API_BASE}/auth/login"
API_AUTH_LOGOUT = f"{API_BASE}/auth/logout"
API_AUTH_REGISTER = f"{API_BASE}/auth/register"

API_PAPER_SUBMIT = f"{API_BASE}/papers/submit"      # sinh viên nộp
API_DECISION_PAPERS = f"{API_BASE}/decision/papers" # admin xem (MOCK)
API_DECISION_MAKE = f"{API_BASE}/decision/make"
API_DECISION_EXPORT = f"{API_BASE}/decision/export"
API_DECISION_RESET = f"{API_BASE}/decision/reset"
API_MAIL = f"{API_BASE}/decision/send-email"

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="UTH-ConfMS",
    page_icon="📄",
    layout="wide"
)

# =====================
# SESSION INIT
# =====================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "roles" not in st.session_state:
    st.session_state.roles = []

if "http" not in st.session_state:
    st.session_state.http = requests.Session()

# =====================
# SIDEBAR - AUTH
# =====================
st.sidebar.title("🔑 TÀI KHOẢN")

if not st.session_state.logged_in:
    auth_mode = st.sidebar.radio(
        "Chọn chức năng",
        ["Đăng nhập", "Đăng ký sinh viên"]
    )
else:
    auth_mode = None

# ======================================================
# REGISTER - SINH VIÊN
# ======================================================
if auth_mode == "Đăng ký sinh viên":
    st.header("📝 ĐĂNG KÝ SINH VIÊN")

    email = st.text_input("📧 Email sinh viên")
    password = st.text_input("🔑 Mật khẩu", type="password")

    if st.button("✅ Đăng ký"):
        res = requests.post(
            API_AUTH_REGISTER,
            json={"email": email, "password": password}
        )

        if res.status_code == 201:
            st.success("🎉 Đăng ký thành công")
        else:
            st.error(res.json().get("message", "Lỗi đăng ký"))

    st.stop()

# ======================================================
# LOGIN
# ======================================================
if auth_mode == "Đăng nhập":
    st.header("🔐 ĐĂNG NHẬP")

    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Mật khẩu", type="password")

    if st.button("🚀 Đăng nhập"):
        res = st.session_state.http.post(
            API_AUTH_LOGIN,
            json={"email": email, "password": password}
        )

        if res.status_code == 200:
            data = res.json()
            st.session_state.logged_in = True
            st.session_state.roles = data.get("roles", [])
            st.success("✅ Đăng nhập thành công")
            st.rerun()
        else:
            st.error("❌ Sai email hoặc mật khẩu")

    st.stop()

# ======================================================
# SIDEBAR - SAU LOGIN
# ======================================================
with st.sidebar:
    st.write(f"👤 **Roles:** {', '.join(st.session_state.roles)}")

    if st.button("🚪 Logout"):
        st.session_state.http.post(API_AUTH_LOGOUT)
        st.session_state.clear()
        st.rerun()

# ======================================================
# SIDEBAR - ADMIN PANEL
# ======================================================
sender_email = ""
sender_pass = ""

if "admin" in st.session_state.roles:
    with st.sidebar:
        st.divider()
        st.title("⚙️ ADMIN PANEL")

        st.subheader("📧 Cấu hình Email")
        sender_email = st.text_input("Gmail Admin")
        sender_pass = st.text_input("App Password", type="password")

        st.divider()

        if st.button("📥 Xuất file Excel"):
            res = st.session_state.http.get(API_DECISION_EXPORT)
            if res.status_code == 200:
                st.download_button(
                    "⬇️ Tải KyYeu.xlsx",
                    data=res.content,
                    file_name="KyYeu.xlsx"
                )
            else:
                st.error("❌ Không xuất được file")

        if st.button("🔄 Reset dữ liệu"):
            res = st.session_state.http.post(API_DECISION_RESET)
            if res.status_code == 200:
                st.success("✅ Đã reset dữ liệu")
                st.rerun()
            else:
                st.error("❌ Reset thất bại")

# ======================================================
# MAIN CONTENT
# ======================================================
st.markdown(
    "<h1 style='text-align:center'>📋 HỆ THỐNG XÉT DUYỆT HỘI NGHỊ</h1>",
    unsafe_allow_html=True
)

# =====================
# SINH VIÊN NỘP BÀI
# =====================
if "student" in st.session_state.roles:
    st.subheader("📄 NỘP BÀI BÁO (SINH VIÊN)")

    with st.form("submit_paper"):
        title = st.text_input("📝 Tiêu đề bài báo")
        abstract = st.text_area("📌 Tóm tắt nội dung")
        file = st.file_uploader("📎 Upload file", type=["pdf", "docx"])
        submit = st.form_submit_button("📤 Nộp bài")

    if submit:
        if not file:
            st.error("❌ Chưa upload file")
        else:
            files = {"file": (file.name, file.getvalue())}
            data = {"title": title, "abstract": abstract}

            res = st.session_state.http.post(
                API_PAPER_SUBMIT,
                data=data,
                files=files
            )

            if res.status_code == 201:
                st.success("✅ Nộp bài thành công")
            else:
                st.error(res.json().get("message", "❌ Lỗi nộp bài"))

# =====================
# ADMIN DUYỆT BÀI (MOCK)
# =====================
if "admin" in st.session_state.roles:
    st.divider()
    st.subheader("📑 DANH SÁCH BÀI BÁO (ADMIN)")

    res = st.session_state.http.get(API_DECISION_PAPERS)
    papers = res.json().get("data", [])

    for p in papers:
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.subheader(p["title"])
                st.write(f"👤 **Tác giả:** {p['author']}")
                st.write(f"⭐ **Điểm:** {p['score']}")

            with col2:
                if p["status"] == "ACCEPTED":
                    st.success("Đã duyệt")
                elif p["status"] == "REJECTED":
                    st.error("Bị loại")
                else:
                    st.warning("Chờ duyệt")

            if p["status"] == "REVIEWED":
                c1, c2 = st.columns(2)

                if c1.button("✅ Duyệt", key=f"ok_{p['id']}"):
                    st.session_state.http.post(
                        API_DECISION_MAKE,
                        json={"paper_id": p["id"], "decision": "ACCEPTED"}
                    )
                    st.rerun()

                if c2.button("❌ Loại", key=f"no_{p['id']}"):
                    st.session_state.http.post(
                        API_DECISION_MAKE,
                        json={"paper_id": p["id"], "decision": "REJECTED"}
                    )
                    st.rerun()

            if p["status"] == "ACCEPTED":
                with st.expander("📧 Gửi Email"):
                    email_to = st.text_input("Email tác giả", key=f"mail_{p['id']}")

                    if st.button("Gửi", key=f"send_{p['id']}"):
                        res = st.session_state.http.post(
                            API_MAIL,
                            json={
                                "id": p["id"],
                                "email_to": email_to,
                                "sender_email": sender_email,
                                "sender_pass": sender_pass
                            }
                        )

                        if res.status_code == 200:
                            st.success("✅ Đã gửi email")
                        else:
                            st.error("❌ Gửi email thất bại")
