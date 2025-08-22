# 퇴원 후 나홀로 집: 나만의 퇴원 계획 짜기 웹앱
# 제작: 수영
# 날짜: 2025.08.22

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import json
import os

# -------------- 1. 설정 및 초기화 함수 --------------

def initialize_app():
    """
    앱의 기본 설정과 세션 상태를 초기화하는 함수
    """
    # 페이지 설정
    st.set_page_config(
        page_title="퇴원 후 나홀로 집: 나만의 퇴원 계획 짜기",
        page_icon="🏥",
        layout="wide"
    )
    
    # CSS 스타일 적용
    load_css()
    
    # 세션 상태 초기화
    initialize_session_state()

def load_css():
    """
    앱의 스타일을 정의하는 CSS를 로드하는 함수
    """
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #3498DB;
            text-align: center;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.8rem;
            color: #2C3E50;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }
        .card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border-left: 5px solid #3498DB;
        }
        .success-card {
            background-color: #d4edda;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 5px solid #28a745;
        }
        .warning-card {
            background-color: #fff3cd;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 5px solid #ffc107;
        }
        .progress-container {
            margin-bottom: 1.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """
    세션 상태 변수들을 초기화하는 함수
    """
    # 기본 사용자 정보
    if 'plan_created' not in st.session_state:
        st.session_state.plan_created = False
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    if 'recovery_type' not in st.session_state:
        st.session_state.recovery_type = ""
    if 'discharge_date' not in st.session_state:
        st.session_state.discharge_date = datetime.now()
        
    # 할 일 및 약물 정보
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
    if 'completed_tasks' not in st.session_state:
        st.session_state.completed_tasks = []
    if 'medications' not in st.session_state:
        st.session_state.medications = []
        
    # 일일 기록
    if 'daily_notes' not in st.session_state:
        st.session_state.daily_notes = {}
    if 'progress_data' not in st.session_state:
        st.session_state.progress_data = []

# -------------- 2. 데이터 관련 함수 --------------

def load_recovery_tasks():
    """
    퇴원 유형별 권장 할 일 목록 데이터를 반환하는 함수
    """
    return {
        "수술 후 회복": [
            "상처 소독하기 (하루 1-2회)",
            "처방된 진통제 복용하기",
            "가벼운 스트레칭 하기",
            "충분한 휴식 취하기",
            "수술 부위 감염 징후 확인하기",
            "영양가 있는 식사하기",
            "충분한 수분 섭취하기",
            "주치의 추적 방문 일정 잡기"
        ],
        "만성 질환 관리": [
            "혈압/혈당 측정하기",
            "처방약 정시에 복용하기",
            "저염/저당 식단 유지하기",
            "가벼운 운동하기 (하루 30분)",
            "체중 기록하기",
            "증상 일지 작성하기",
            "스트레스 관리하기",
            "정기 검진 일정 잡기"
        ],
        "골절 회복": [
            "처방된 진통제 복용하기",
            "깁스/부목 상태 확인하기",
            "처방된 재활 운동하기",
            "보조기구 올바르게 사용하기",
            "충분한 휴식 취하기",
            "칼슘이 풍부한 음식 섭취하기",
            "부종 확인하기",
            "주치의 추적 방문 일정 잡기"
        ],
        "산후 조리": [
            "회음부 관리하기",
            "모유수유/젖몸살 관리",
            "충분한 휴식 취하기",
            "산후 출혈량 확인하기",
            "골반 운동하기",
            "영양가 있는 식사하기",
            "아기 케어 일정 관리하기",
            "산후 검진 일정 잡기"
        ]
    }

def save_data():
    """
    현재 사용자 데이터를 저장하는 함수 (확장성을 위해 준비)
    """
    # 실제 구현 시 파일이나 데이터베이스에 저장하는 코드 추가
    pass

def load_data():
    """
    사용자 데이터를 불러오는 함수 (확장성을 위해 준비)
    """
    # 실제 구현 시 파일이나 데이터베이스에서 불러오는 코드 추가
    pass

# -------------- 3. UI 컴포넌트 함수 --------------

def render_sidebar():
    """
    사이드바 UI를 렌더링하는 함수
    """
    with st.sidebar:
        st.markdown("### 내 정보 입력하기")
        
        if not st.session_state.plan_created:
            # 새 계획 생성 폼
            user_name = st.text_input("이름을 입력해주세요:", value=st.session_state.user_name)
            
            recovery_types = list(load_recovery_tasks().keys())
            recovery_type = st.selectbox(
                "
