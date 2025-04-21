
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="라온 스케줄 작성앱 v2.0", layout="wide")
st.title("📘 라온 스케줄 작성앱 v2.0")

# 선생님 리스트
teacher_list = ["이윤로T", "정주빈T", "김서진T", "조하현T", "류승연T", "임인섭T"]

# 수업과정 리스트 (2단계 구조)
course_category = {
    "초등부": ["초1-1", "초1-2", "초2-1", "초2-2", "초3-1", "초3-2", "초4-1", "초4-2", "초5-1", "초5-2", "초6-1", "초6-2"],
    "중등부": ["중1-1", "중1-2", "중2-1", "중2-2", "중3-1", "중3-2"],
    "고등부": ["공통수학1", "공통수학2", "대수", "미적분1", "미적분2", "확률과 통계", "기하", "수학1", "수학2", "미적분"]
}

# 워터마크 (웹 전용, 인쇄 시 제외)
st.markdown(
    '''
    <style>
    .watermark {
        position: fixed;
        bottom: 5%;
        right: 5%;
        z-index: -1;
        opacity: 0.08;
    }
    </style>
    <img class="watermark" src="https://raon-schedule.streamlit.app/raon_logo.png" width="300">
    ''',
    unsafe_allow_html=True
)

# 시간표 유형 선택
type_option = st.radio("🗂️ 시간표 유형을 선택하세요", ["정규 시간표", "시험대비 시간표"])

# 학생 정보 입력
with st.expander("👤 학생 기본 정보 입력"):
    col1, col2, col3 = st.columns(3)
    with col1:
        student_name = st.text_input("학생명")
    with col2:
        school = st.text_input("학교명")
    with col3:
        grade = st.text_input("학년")

    col4, col5 = st.columns(2)
    with col4:
        class_name = st.text_input("반명")
    with col5:
        teacher_name = st.selectbox("담임선생님", teacher_list)

# 기간 설정
with st.expander("📆 적용 기간 설정"):
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("시작일", value=datetime.date.today())
    with col2:
        end_date = st.date_input("종료일", value=datetime.date.today() + datetime.timedelta(days=30))

# 수업 정보 (정규 시간표용)
if type_option == "정규 시간표":
    with st.expander("📘 수업 정보 입력"):
        category = st.selectbox("과정 카테고리 선택", list(course_category.keys()))
        selected_courses = st.multiselect("수업과정명 선택 (복수 선택 가능)", course_category[category])
        textbook = st.text_input("교재명 (예: 쎈 수학)")

# 시험대비 정보 입력
if type_option == "시험대비 시간표":
    with st.expander("📝 시험 정보 입력"):
        col1, col2, col3 = st.columns(3)
        with col1:
            exam_start = st.date_input("시험 시작일")
        with col2:
            exam_end = st.date_input("시험 종료일")
        with col3:
            math_exam_date = st.date_input("수학 시험일")

# 시간표 직접 입력
with st.expander("📋 시간표 직접 입력"):
    st.write("요일, 시간, 과목 정보를 직접 입력하세요.")
    time_table = st.data_editor(pd.DataFrame({
        "요일": ["월", "수"],
        "시간": ["19:30 ~ 21:00", "19:30 ~ 21:00"],
        "과목": ["수학Ⅰ", "수학Ⅱ"]
    }), num_rows="dynamic")

# 파일 업로드
with st.expander("📤 엑셀 파일로 시간표 불러오기"):
    uploaded_file = st.file_uploader("엑셀 또는 CSV 파일을 업로드하세요", type=["xlsx", "csv"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith("csv"):
                uploaded_df = pd.read_csv(uploaded_file)
            else:
                uploaded_df = pd.read_excel(uploaded_file)
            st.success("✅ 파일 업로드 성공!")
            st.dataframe(uploaded_df)
        except Exception as e:
            st.error(f"❌ 파일을 읽는 중 오류 발생: {e}")

# 미리보기
with st.expander("👀 미리보기"):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"### 🧾 {student_name} 학생 ({school} {grade}) - {class_name}반 / 담임: {teacher_name}")
        st.markdown(f"**적용 기간:** {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")
        if type_option == "정규 시간표" and selected_courses:
            st.markdown(f"**과정:** {', '.join(selected_courses)} / **교재:** {textbook}")
        elif type_option == "시험대비 시간표" and 'exam_start' in locals():
            st.markdown(f"**시험기간:** {exam_start.strftime('%Y-%m-%d')} ~ {exam_end.strftime('%Y-%m-%d')} / 수학시험일: {math_exam_date.strftime('%Y-%m-%d')}")
    with col2:
        st.image("raon_logo.png", width=100)

    st.write("---")
    st.dataframe(time_table, use_container_width=True)
