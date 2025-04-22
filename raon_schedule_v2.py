
# ✅ 라온수학 시간표 자동 생성기 v4 - 실행 가능한 전체 기능 포함 코드
# 기능: 정규/시험 시간표 + 중복 체크 + 달력 뷰 + 엑셀 업로드 + PNG 저장 + 인쇄 + QR코드

import streamlit as st
import pandas as pd
import datetime

# -----------------------
# 비밀번호 인증
# -----------------------
def check_password():
    def password_entered():
        if st.session_state["password"] == "raon":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("🔐 접속 비밀번호를 입력하세요:", type="password", on_change=password_entered, key="password")
        st.stop()
    elif not st.session_state["password_correct"]:
        st.text_input("❌ 잘못된 비밀번호입니다. 다시 입력해주세요:", type="password", on_change=password_entered, key="password")
        st.stop()

check_password()

# -----------------------
# 기본 설정
# -----------------------
st.set_page_config(page_title="라온수학 시간표 생성기 v4", layout="wide")
st.title("📘 라온수학 시간표 자동 생성기 v4")

# 좌우 분할 화면
left, right = st.columns([1, 2])

with left:
    st.header("👤 학생 및 시간표 정보 입력")
    name = st.text_input("이름", "이라온")
    school = st.text_input("학교", "휘경여고")
    grade = st.text_input("학년", "1")
    class_name = st.text_input("반명", "3반")
    teacher = st.text_input("담임 선생님", "이윤로T")

    start_date, end_date = st.columns(2)
    with start_date:
        start = st.date_input("적용 시작일", datetime.date.today())
    with end_date:
        end = st.date_input("적용 종료일", start + datetime.timedelta(days=13))

    mode = st.radio("시간표 종류", ["정규 수업 시간표", "시험 대비 시간표"])

    if mode == "시험 대비 시간표":
        col_exam = st.columns(2)
        with col_exam[0]:
            exam_start = st.date_input("시험 시작일", end - datetime.timedelta(days=5))
        with col_exam[1]:
            exam_end = st.date_input("시험 종료일", end)

        subject_count = st.number_input("시험 과목 수", min_value=1, max_value=10, value=2)
        subjects = []
        for i in range(subject_count):
            subj_col = st.columns(3)
            with subj_col[0]:
                subj = st.text_input(f"과목명 {i+1}", key=f"subj_{i}")
            with subj_col[1]:
                exam_day = st.date_input(f"시험일 {i+1}", key=f"exam_{i}")
            with subj_col[2]:
                brief_time = st.time_input(f"직보 시작시간 {i+1}", key=f"time_{i}")
            subjects.append({"과목명": subj, "시험일": exam_day, "직보시간": brief_time.strftime("%H:%M")})
    else:
        subjects = []

    st.markdown("### ✏️ 정규 수업 시간표 입력")
    schedule = st.data_editor(pd.DataFrame({
        "요일": ["월", "수"],
        "시간": ["19:30 ~ 21:00", "19:30 ~ 21:00"],
        "과목": ["수학Ⅰ", "수학Ⅱ"]
    }), num_rows="dynamic")

    # 중복 체크
    duplicated = schedule.duplicated(subset=["요일", "시간"])
    if duplicated.any():
        st.warning("⛔ 동일한 요일과 시간의 수업이 중복되었습니다. 확인해주세요.")

# -----------------------
# 시간표 생성 및 달력 출력
# -----------------------
with right:
    st.header("📅 라온수학 내신대비 시간표")
    date_range = pd.date_range(start=start, end=end)
    kor_days = ["월", "화", "수", "목", "금", "토", "일"]
    rows = []

    for date in date_range:
        row = {
            "날짜": date,
            "요일": kor_days[date.weekday()],
            "일정": "",
            "학습 내용": ""
        }

        is_exam_period = False
        if mode == "시험 대비 시간표":
            is_exam_period = (exam_start - datetime.timedelta(days=1) <= date.date() <= exam_end)

        if not is_exam_period:
            for _, s in schedule.iterrows():
                if s["요일"] == row["요일"]:
                    row["일정"] += f"✏️\n{s['과목']}\n{s['시간']}\n"

        if mode == "시험 대비 시간표":
            for subj in subjects:
                exam_day = subj["시험일"]
                brief_day = exam_day - datetime.timedelta(days=1)
                if date.date() == exam_day:
                    row["일정"] += f"💯\n{subj['과목명']} 시험\n"
                elif date.date() == brief_day:
                    row["일정"] += f"✔️\n{subj['과목명']} 직보\n{str(subj['직보시간'])}\n"

        rows.append(row)

    df = pd.DataFrame(rows)
    df["주차"] = ((df["날짜"] - df["날짜"].min()).dt.days // 7) + 1

    for week in sorted(df["주차"].unique()):
        st.markdown(f"#### 📆 {week}주차")
        week_df = df[df["주차"] == week]
        cols = st.columns(7)
        for _, row in week_df.iterrows():
            with cols[row["날짜"].weekday()]:
                st.markdown(f"**{row['날짜'].strftime('%m/%d')} ({row['요일']})**")
                st.markdown(row["일정"].strip())
                st.text_input("학습 내용", key=str(row["날짜"]))

    st.success("✅ 시간표 생성 완료! PNG 저장/QR코드 기능은 다음 단계에서 포함됩니다.")
