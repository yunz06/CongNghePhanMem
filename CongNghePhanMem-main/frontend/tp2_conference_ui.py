import streamlit as st
import requests

API = "http://127.0.0.1:5000/api"

st.title("TP2 – Conference & CFP Management")

menu = st.sidebar.selectbox(
    "Chọn chức năng",
    ["Tạo Conference", "Danh sách Conference", "Quản lý Track"]
)

# ======================
# CREATE CONFERENCE
# ======================
if menu == "Tạo Conference":
    st.header("Tạo hội nghị mới")

    name = st.text_input("Tên hội nghị")
    desc = st.text_area("Mô tả")
    start = st.date_input("Ngày bắt đầu")
    end = st.date_input("Ngày kết thúc")
    deadline = st.date_input("Deadline nộp bài")

    if st.button("Tạo hội nghị"):
        data = {
            "name": name,
            "description": desc,
            "start_date": str(start),
            "end_date": str(end),
            "submission_deadline": str(deadline)
        }

        res = requests.post(f"{API}/conferences", json=data)

        if res.status_code == 201:
            st.success("Tạo hội nghị thành công!")
        else:
            st.error("Lỗi khi tạo hội nghị")


# ======================
# LIST CONFERENCE
# ======================
if menu == "Danh sách Conference":
    st.header("Danh sách hội nghị")

    res = requests.get(f"{API}/conferences")
    data = res.json()

    for c in data:
        st.write(f"📌 {c['id']} - {c['name']} (Deadline: {c['submission_deadline']})")


# ======================
# TRACK MANAGEMENT
# ======================
if menu == "Quản lý Track":
    st.header("Thêm Track cho hội nghị")

    cid = st.number_input("ID Conference", step=1)
    track_name = st.text_input("Tên Track")

    if st.button("Thêm Track"):
        data = {"name": track_name}
        res = requests.post(f"{API}/conferences/{cid}/tracks", json=data)

        if res.status_code == 201:
            st.success("Thêm track thành công!")
        else:
            st.error("Không thêm được track")
