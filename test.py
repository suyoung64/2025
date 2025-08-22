import streamlit as st
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="퇴원 후 나홀로 집", page_icon="🏥")

# 제목
st.title("퇴원 후 나홀로 집: 나만의 퇴원 계획 짜기 🏥")
st.markdown("---")

# 세션 상태 초기화
if 'plan_created' not in st.session_state:
    st.session_state.plan_created = False
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'completed_tasks' not in st.session_state:
    st.session_state.completed_tasks = []

# 퇴원 유형별 할 일 목록
recovery_tasks = {
    "수술 후 회복": [
        "상처 소독하기 (하루 1-2회)",
        "처방된 진통제 복용하기",
        "가벼운 스트레칭 하기",
        "충분한 휴식 취하기",
        "수술 부위 감염 징후 확인하기"
    ],
    "만성 질환 관리": [
        "혈압/혈당 측정하기",
        "처방약 정시에 복용하기",
        "저염/저당 식단 유지하기",
        "가벼운 운동하기 (하루 30분)",
        "체중 기록하기"
    ],
    "골절 회복": [
        "처방된 진통제 복용하기",
        "깁스/부목 상태 확인하기",
        "처방된 재활 운동하기",
        "보조기구 올바르게 사용하기",
        "충분한 휴식 취하기"
    ],
    "산후 조리": [
        "회음부 관리하기",
        "모유수유/젖몸살 관리",
        "충분한 휴식 취하기",
        "산후 출혈량 확인하기",
        "골반 운동하기"
    ]
}

# 사이드바 - 사용자 정보 입력
with st.sidebar:
    st.header("내 정보 입력하기")
    
    if not st.session_state.plan_created:
        user_name = st.text_input("이름을 입력해주세요:")
        recovery_type = st.selectbox("퇴원 유형을 선택해주세요:", list(recovery_tasks.keys()))
        discharge_date = st.date_input("퇴원일을 선택해주세요:")
        
        if st.button("맞춤 계획 만들기"):
            st.session_state.user_name = user_name
            st.session_state.recovery_type = recovery_type
            st.session_state.discharge_date = discharge_date
            st.session_state.tasks = recovery_tasks[recovery_type].copy()
            st.session_state.completed_tasks = [False] * len(st.session_state.tasks)
            st.session_state.plan_created = True
            st.experimental_rerun()
    else:
        st.success(f"{st.session_state.user_name}님의 맞춤 계획이 생성되었습니다!")
        
        if st.button("새로운 계획 만들기"):
            st.session_state.plan_created = False
            st.session_state.tasks = []
            st.session_state.completed_tasks = []

# 메인 화면 - 퇴원 계획 보여주기
if st.session_state.plan_created:
    st.header(f"{st.session_state.user_name}님의 {st.session_state.recovery_type} 퇴원 계획")
    
    # 퇴원 후 경과일 계산
    today = datetime.now().date()
    discharge_date = st.session_state.discharge_date
    days_since = (today - discharge_date).days
    
    st.info(f"퇴원일: {discharge_date.strftime('%Y년 %m월 %d일')} (퇴원 후 {days_since}일 경과)")
    
    # 체크리스트 표시
    st.subheader("나의 회복 체크리스트")
    for i, task in enumerate(st.session_state.tasks):
        checked = st.checkbox(task, value=st.session_state.completed_tasks[i], key=f"task_{i}")
        st.session_state.completed_tasks[i] = checked
    
    # 진행률 표시
    if st.session_state.tasks:
        progress = sum(st.session_state.completed_tasks) / len(st.session_state.completed_tasks)
        st.progress(progress)
        st.write(f"오늘의 회복 진행률: {int(progress * 100)}%")
    
    # 메모 기능
    st.subheader("오늘의 건강 메모")
    memo = st.text_area("오늘 컨디션이나 특이사항을 기록해보세요:")
    if st.button("저장하기"):
        st.success("메모가 저장되었습니다!")
else:
    st.info("👈 왼쪽 사이드바에서 정보를 입력하고 '맞춤 계획 만들기'를 눌러주세요!")
    st.image("https://img.freepik.com/free-vector/flat-hand-drawn-hospital-reception-scene_52683-54613.jpg")
