import os
import psycopg2
import google.generativeai as genai

# 1. DATABASE CLOUD
DB_CONNECTION_STRING = "postgresql://neondb_owner:npg_iLfSh7mtsF1I@ep-delicate-moon-a1yhrfrd-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# 2. AI KEY (Dùng chung)
GEMINI_KEY = "AIzaSyDyC8dfjGw32DhkOgHjpnFk49eZOeGhqtw"

# Hàm kết nối DB chuẩn (Chỉ cần gọi là chạy)
def get_db_connection():
    try:
        return psycopg2.connect(DB_CONNECTION_STRING)
    except Exception as e:
        print("❌ Lỗi kết nối Cloud DB:", e)
        return None

# Hàm lấy Model AI
def get_ai_model():
    genai.configure(api_key=GEMINI_KEY)
    return genai.GenerativeModel('gemini-1.5-flash')