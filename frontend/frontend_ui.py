import streamlit as st
import requests

API = "http://127.0.0.1:5000/api/decision"
AUTH_API = "http://127.0.0.1:5000/api/auth/login"
LOGOUT_API = "http://127.0.0.1:5000/api/auth/logout"

st.set_page_config(page_title="Hệ thống Xét duyệt", layout="wide")

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "http" not in st.session_state:
    st.session_state.http = requests.Session()

# ---------- LOGIN ----------
if not st.session_state.logged_in:
    st.title("🔐 Admin Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = st.session_state.http.post(
            AUTH_API,
            json={"email": email, "password": password}
        )

        if res.status_code == 200:
            st.session_state.logged_in = True
            st.success("Đăng nhập thành công")
            st.rerun()
        else:
            st.error("Sai tài khoản hoặc mật khẩu")

    st.stop()

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("Admin Panel")

    if st.button("🚪 Logout"):
        st.session_state.http.post(LOGOUT_API)
        st.session_state.clear()
        st.rerun()

    st.divider()

    # ===== EXPORT =====
    if st.button("📥 Xuất file Excel"):
        res = st.session_state.http.get(f"{API}/export")
        if res.status_code == 200:
            st.download_button(
                label="Tải KyYeu.xlsx",
                data=res.content,
                file_name="KyYeu.xlsx"
            )
        else:
            st.error("Không xuất được file")

    # ===== RESET =====
    if st.button("🔄 Reset dữ liệu"):
        res = st.session_state.http.post(f"{API}/reset")
        if res.status_code == 200:
            st.success("Đã reset dữ liệu")
            st.rerun()
        else:
            st.error("Reset thất bại")

# ---------- MAIN ----------
st.title("📋 HỘI ĐỒNG XÉT DUYỆT")

res = st.session_state.http.get(f"{API}/papers")

if res.status_code != 200:
    st.error("Không lấy được dữ liệu")
    st.stop()

papers = res.json()["data"]

for p in papers:
    with st.container(border=True):
        st.subheader(p["title"])
        st.write(f"👤 Tác giả: {p['author']}")
        st.write(f"⭐ Điểm: {p['score']}")
        st.write(f"📌 Trạng thái: **{p['status']}**")

        if p["status"] == "REVIEWED":
            col1, col2 = st.columns(2)

            if col1.button("✅ Duyệt", key=f"ok_{p['id']}"):
                st.session_state.http.post(
                    f"{API}/make",
                    json={"paper_id": p["id"], "decision": "ACCEPTED"}
                )
                st.rerun()

            if col2.button("❌ Loại", key=f"no_{p['id']}"):
                st.session_state.http.post(
                    f"{API}/make",
                    json={"paper_id": p["id"], "decision": "REJECTED"}
                )
                st.rerun()
