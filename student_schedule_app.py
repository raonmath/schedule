import streamlit as st
import pandas as pd
from collections import defaultdict
import io

st.set_page_config(page_title="학생별 시간표 생성기", layout="wide")
st.title("📚 학생별 주간 시간표 자동 생성기")
st.write("엑셀 파일을 업로드하면, 학생별로 자동으로 시간표를 생성해줍니다.")

# 🔐 간이 비밀번호 보호
password = st.text_input("🔒 비밀번호를 입력하세요", type="password")
if password != "raonmath":
    st.warning("비밀번호를 입력해야 사용 가능합니다.")
    st.stop()
else:
    st.success("접속 성공! 아래에서 파일을 업로드하세요.")

uploaded_file = st.file_uploader("📂 시간표 엑셀 파일 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    df = df.fillna(method='ffill')  # 선생님/반명 등이 비어있으면 이전 값 채움

    student_schedules = defaultdict(list)

    for _, row in df.iterrows():
        teacher = row['담당선생님']
        class_name = row['반명']
        day = row['수업요일'].strip()
        time = row['수업시간'].strip()

        if pd.notna(row['학생명']):
            students = [s.strip() for s in row['학생명'].split(',')]
            for student in students:
                student_schedules[student].append({
                    '요일': day,
                    '시간': time,
                    '반명': class_name
                })

    selected_student = st.selectbox("👤 학생 선택", sorted(student_schedules.keys()))

    if selected_student:
        schedule_df = pd.DataFrame(student_schedules[selected_student])
        schedule_df = schedule_df[['요일', '시간', '반명']]
        st.write(f"### 📅 {selected_student} 학생의 주간 시간표")
        st.dataframe(schedule_df, use_container_width=True)

        # 다운로드 기능
        towrite = io.BytesIO()
        with pd.ExcelWriter(towrite, engine='openpyxl') as writer:
            schedule_df.to_excel(writer, index=False, sheet_name=selected_student[:31])
        towrite.seek(0)

        st.download_button(
            label="📥 엑셀 파일 다운로드",
            data=towrite,
            file_name=f"{selected_student}_시간표.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
