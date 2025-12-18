import sys
import os
import google.generativeai as genai # Nhớ cài thư viện: pip install google-generativeai

# Đoạn này giúp tìm thấy file config dù chạy ở đâu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import GEMINI_KEY

# Cấu hình AI
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def check_grammar(text):
    """(Cho Mem 3) Sửa lỗi ngữ pháp tiếng Anh"""
    try:
        response = model.generate_content(f"Correct English grammar: {text}")
        return response.text
    except:
        return "Lỗi AI check grammar"

def summarize_paper(text):
    """(Cho Mem 5) Tóm tắt bài báo"""
    try:
        response = model.generate_content(f"Summarize in 3 bullet points (Vietnamese): {text}")
        return response.text
    except:
        return "Lỗi AI tóm tắt"

def draft_decision_email(author_name, decision, reason):
    """(Cho Mem 6) Viết email thông báo"""
    try:
        response = model.generate_content(f"Write a {decision} email to {author_name}. Reason: {reason}.")
        return response.text
    except:
        return "Lỗi AI soạn mail"

def suggest_reviewer(abstract, reviewers_list):
    """(Cho Mem 4) Gợi ý người chấm"""
    try:
        response = model.generate_content(f"Match best reviewer for abstract '{abstract}' from list: {reviewers_list}")
        return response.text
    except:
        return "Lỗi AI gợi ý"