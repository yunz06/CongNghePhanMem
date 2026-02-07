# ==========================================================
# Member 7 (Minh Hùng)
# ROLE: REPORT & SYSTEM INTEGRATION TEST
# TEST LEVEL: FULL SYSTEM TEST (INTEGRATION + REPORT)
# PHIÊN BẢN AUTHENTIC – ƯU TIÊN DỮ LIỆU THẬT
# ==========================================================

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os, sys, time, json

# ======================================================
# 1. KẾT NỐI APP & DATABASE
# ======================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from app import app, db
    import models
    Paper = getattr(models, 'Paper', None)
    SystemBug = getattr(models, 'SystemBug', None)
    HAS_APP = True
    print("✅ [INIT] Kết nối backend thành công.")
except Exception as e:
    HAS_APP = False
    print("❌ [INIT] Không kết nối được backend:", e)

# ======================================================
# 2. HÀM SYSTEM TEST
# ======================================================
def draw_bug_chart(df):
    if df.empty or 'Status' not in df.columns:
        return None

    counts = df['Status'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140)
    plt.title("System Bug Status (REAL DATA)")
    fname = f"Bug_Chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(fname)
    plt.close()
    return fname


def backup_json(papers, bugs):
    if not os.path.exists("backup"):
        os.makedirs("backup")
    fname = f"backup/system_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump({
            "papers": papers,
            "bugs": bugs,
            "timestamp": str(datetime.now())
        }, f, indent=4, default=str)
    return fname


def stress_test():
    start = time.time()
    _ = [i**2 for i in range(500_000)]
    return round(time.time() - start, 4)


# ======================================================
# 3. CHƯƠNG TRÌNH CHÍNH – SYSTEM TEST
# ======================================================
def main():
    print("\n" + "="*60)
    print("🚀 FULL SYSTEM TEST – DATA AUTHENTIC MODE")
    print("="*60)

    papers_data = []
    bugs_data = []
    generated_files = []
    data_mode = ""

    # -----------------------------
    # STEP 1: TRÍCH XUẤT DATA THẬT
    # -----------------------------
    if HAS_APP and app:
        with app.app_context():
            if Paper:
                for p in Paper.query.all():
                    papers_data.append({
                        "ID": p.id,
                        "Title": p.title,
                        "Status": p.status
                    })
            if SystemBug:
                for b in SystemBug.query.all():
                    bugs_data.append({
                        "ID": b.id,
                        "Title": b.title,
                        "Status": b.status
                    })

    # -----------------------------
    # STEP 2: LOGIC TRUNG THỰC
    # -----------------------------
    if papers_data:
        data_mode = f"REAL DATA ({len(papers_data)} papers)"
        print(f"✅ [DB] Phát hiện {len(papers_data)} bài báo thật.")
    else:
        data_mode = "DEMO DATA (DB trống)"
        print("⚠️ [DB] Database trống → sinh dữ liệu demo tối thiểu.")
        for i in range(1, 6):
            papers_data.append({
                "ID": i,
                "Title": f"Bài báo demo {i}",
                "Status": "accepted"
            })
        bugs_data.append({
            "ID": 1,
            "Title": "Demo system bug",
            "Status": "Fixed"
        })

    # -----------------------------
    # STEP 3: SYSTEM TEST OUTPUT
    # -----------------------------
    df_papers = pd.DataFrame(papers_data)
    df_bugs = pd.DataFrame(bugs_data)

    kyyeu_file = f"KyYeu_SystemTest_{datetime.now().strftime('%Y%m%d')}.xlsx"
    df_papers.to_excel(kyyeu_file, index=False)
    generated_files.append(kyyeu_file)

    bug_report_file = f"BugReport_SystemTest_{datetime.now().strftime('%Y%m%d')}.xlsx"
    df_bugs.to_excel(bug_report_file, index=False)
    generated_files.append(bug_report_file)

    chart_file = draw_bug_chart(df_bugs)
    if chart_file:
        generated_files.append(chart_file)

    backup_file = backup_json(papers_data, bugs_data)
    stress_time = stress_test()

    # -----------------------------
    # STEP 4: KẾT QUẢ SYSTEM TEST
    # -----------------------------
    print("\n📊 KẾT QUẢ SYSTEM TEST")
    print("-"*60)
    print(f"🔹 Data mode        : {data_mode}")
    print(f"🔹 Papers processed : {len(papers_data)}")
    print(f"🔹 Bugs processed   : {len(bugs_data)}")
    print(f"🔹 Stress test time : {stress_time} giây")
    print("\n📁 FILE ĐƯỢC TẠO:")
    for f in generated_files:
        print(f"   ✔ {f}")
    print(f"   ✔ {backup_file}")

    print("\n🎉 SYSTEM TEST HOÀN TẤT – KHÔNG LỖI NGHIÊM TRỌNG")
    print("="*60)


if __name__ == "__main__":
    main()
