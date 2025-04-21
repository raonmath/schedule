
import streamlit as st
import pandas as pd
import datetime

# 앱 기본 설정
st.set_page_config(page_title="시험 대비 시간표 달력 뷰", layout="wide")
st.title("📘 시험 대비 시간표 (달력 뷰 + 인쇄용 카드)")

# 기본 정보 입력
with st.sidebar:
    st.header("👤 학생 정보")
    student_name = st.text_input("이름", "이라온")
    class_name = st.text_input("반명", "3반")
    teacher_name = st.text_input("담임 선생님", "이윤로T")

    st.markdown("---")
    st.subheader("📅 기간 설정")
    start_date = st.date_input("적용 시작일", value=datetime.date.today())
    end_date = st.date_input("적용 종료일", value=start_date + datetime.timedelta(days=13))

    exam_start = st.date_input("시험 시작일", value=end_date - datetime.timedelta(days=5))
    exam_end = st.date_input("시험 종료일", value=end_date)

    st.markdown("---")
    st.subheader("📚 시험 과목 입력")
    num_subjects = st.number_input("시험 과목 수", min_value=1, max_value=10, value=3, step=1)

    subjects = []
    for i in range(num_subjects):
        st.markdown(f"**과목 {i+1}**")
        subj = st.text_input(f"과목명 {i+1}", key=f"subj_{i}")
        exam_day = st.date_input(f"시험일 {i+1}", value=exam_start + datetime.timedelta(days=i), key=f"exam_{i}")
        brief_time = st.text_input(f"직보 시간 {i+1}", "18:30 ~ 21:00", key=f"time_{i}")
        subjects.append({"과목명": subj, "시험일": exam_day, "직보시간": brief_time})

# 날짜 생성
date_range = pd.date_range(start=start_date, end=end_date)
rows = []

# 일정 채우기
for date in date_range:
    day_str = date.strftime("%Y-%m-%d")
    weekday = date.strftime("%A")
    entry = {
        "날짜": day_str,
        "요일": weekday,
        "일정": "",
        "학습 내용": ""
    }

    # 과목별 직보/시험 자동 삽입
    for subj in subjects:
        exam_day = subj["시험일"]
        briefing_day = exam_day - datetime.timedelta(days=1)
        if date.date() == exam_day:
            entry["일정"] += f"{subj['과목명']} 시험 🧾\n"
        elif date.date() == briefing_day:
            entry["일정"] += f"{subj['과목명']} 직보 📝 ({subj['직보시간']})\n"

    # 수업 제외 조건
    if not (exam_start - datetime.timedelta(days=1) <= date.date() <= exam_end):
        entry["일정"] += "정규 수업\n"

    rows.append(entry)

# 달력 형식으로 변환
df = pd.DataFrame(rows)
df["날짜"] = pd.to_datetime(df["날짜"])
df["주"] = df["날짜"].dt.isocalendar().week
weeks = df["주"].unique()

st.markdown("## 🗓️ 달력 형식 시간표")

for week in weeks:
    st.markdown(f"### 📅 Week {week}")
    week_df = df[df["주"] == week]
    week_df = week_df.sort_values("날짜")

    cols = st.columns(7)
    for i, (_, row) in enumerate(week_df.iterrows()):
        with cols[row["날짜"].weekday()]:
            st.markdown(f"**{row['날짜'].strftime('%m/%d')} ({row['요일'][0]})**")
            st.markdown(f"`{row['일정'].strip()}`")
            st.text_input("학습 내용", key=str(row["날짜"]))

st.success("✅ 시간표가 달력 형식으로 출력되었습니다. 인쇄는 브라우저 인쇄(ctrl+P) 또는 PDF로 저장을 활용하세요.")
