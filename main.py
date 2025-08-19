import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Streamlit 앱의 전반적인 스타일을 위한 이모지 잔치! 💖
st.set_page_config(page_title="💖MBTI 찐사랑 궁합 찰떡 웹앱!💖", page_icon="💘", layout="centered")

st.title("💫✨ 내 운명의 상대를 찾아라! MBTI 찐사랑 궁합 테스트! ✨💫")
st.write("솔로 탈출 기원! 커플들은 더욱 꽁냥꽁냥! 🤫💕")
st.image("https://images.unsplash.com/photo-1549442084-2a6d4ee2714f?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", caption="운명의 데스티니! 🤩", use_column_width=True)


# 사이드바에도 화려함 한 스푼 추가! 🌈
st.sidebar.header("✨ 내 MBTI는 뭐게? ✨")
user_mbti = st.sidebar.selectbox(
    "👉🏻 나의 심장을 뛰게 할 MBTI 선택하기!",
    ["INFP", "ENFP", "INFJ", "ENFJ", "INTJ", "ENTJ", "INTP", "ENTP", 
     "ISFP", "ESFP", "ISTP", "ESTP", "ISFJ", "ESFJ", "ISTJ", "ESTJ"],
    key='user_mbti_select' # 키 추가
)

st.sidebar.header("💕 그럼 상대방 MBTI는? 💕")
partner_mbti = st.sidebar.selectbox(
    "👉🏻 그/그녀의 MBTI는 무엇인가요?",
    ["INFP", "ENFP", "INFJ", "ENFJ", "INTJ", "ENTJ", "INTP", "ENTP", 
     "ISFP", "ESFP", "ISTP", "ESTP", "ISFJ", "ESFJ", "ISTJ", "ESTJ"],
    key='partner_mbti_select' # 키 추가
)

# 🔥 찐 궁합 데이터 (이모지 듬뿍 넣어봄! 더 채워 넣으면 대박남! 🎉)
compatibility_data = {
    "INFP": {
        "ENFJ": "💖 황금 궁합! 찐사랑 바이브 통하는 영혼의 단짝! ✨ 서로를 완벽하게 이해해요!",
        "ENTJ": "🤯 오잉? 흥미로운 조합! 티키타카 환상의 케미! 서로 다른 매력에 퐁당~!",
        "INFP": "🤝 완벽한 거울! 우리 닮았나요? 동족 상봉 너낌~ 공감 능력 만렙! 🥹",
        "ESTJ": "😱 극과 극은 통한다?! 스파크 튀는 의외의 조합! 서로에게 새로운 세상을 선물해 줄 거예요! 💫",
        "ISTP": "🤔 서로의 영역 존중! 적당한 거리감으로 편안함을 유지하는 관계! 자유로운 영혼들!"
        # 나머지 MBTI와의 궁합 정보 추가
    },
    "ENFP": {
        "INFJ": "💞 천생연분! 불꽃 케미! 에너지 폭발하는 최고의 파트너! 이 관계 유죄! 💯",
        "INTJ": "🧠 신기방기 조합! ENFP의 자유로움과 INTJ의 깊은 통찰력의 만남! 브레인 커플각! 📚",
        "ISFJ": "😌 편안함 그 자체! 따뜻함과 배려로 가득한 관계! 지친 일상에 쉼표가 되어줄 거예요! 🌿"
    },
    "INFJ": {
        "ENFP": "💞 천생연분! 불꽃 케미! 에너지 폭발하는 최고의 파트너! 이 관계 유죄! 💯",
        "ENTP": "🧐 지적인 대화가 넘치는 관계! 서로에게 영감을 주는 뮤즈 같은 존재! 💡",
        "ISFP": "🎨 감성 충만! 예술적인 영혼들의 만남! 조용히 서로를 응원하며 성장하는 관계! 🤫"
    },
    "ENFJ": {
        "INFP": "💖 황금 궁합! 찐사랑 바이브 통하는 영혼의 단짝! ✨ 서로를 완벽하게 이해해요!",
        "ISTP": "🏃‍♀️🕺 에너지 넘치는 ENFJ와 시크한 ISTP! 겉은 달라 보여도 서로에게 끌리는 신기한 조합! 💥"
    },
    "INTJ": {
        "ENFP": "🧠 신기방기 조합! ENFP의 자유로움과 INTJ의 깊은 통찰력의 만남! 브레인 커플각! 📚",
        "ENTP": "🗣️ 토론 배틀? 지적 자극 뿜뿜! 끝없는 대화로 서로의 지식 레벨을 올리는 스마트 커플! 🤓"
    },
    "ENTJ": {
        "INFP": "🤯 오잉? 흥미로운 조합! 티키타카 환상의 케미! 서로 다른 매력에 퐁당~!",
        "INTP": "🤖 계획형 ENTJ와 자유로운 INTP! 서로의 부족한 점을 채워주는 보완재 관계! 시너지가 장난 아냐! ✨"
    },
    "INTP": {
        "ENTJ": "🤖 계획형 ENTJ와 자유로운 INTP! 서로의 부족한 점을 채워주는 보완재 관계! 시너지가 장난 아냐! ✨",
        "ENTP": "🤯 자유로운 영혼들의 만남! 아이디어 샘솟는 창의력 뿜뿜 커플! 예측 불가능한 매력이 넘쳐요! 🎢"
    },
    "ENTP": {
        "INFJ": "🧐 지적인 대화가 넘치는 관계! 서로에게 영감을 주는 뮤즈 같은 존재! 💡",
        "INTJ": "🗣️ 토론 배틀? 지적 자극 뿜뿜! 끝없는 대화로 서로의 지식 레벨을 올리는 스마트 커플! 🤓",
        "INTP": "🤯 자유로운 영혼들의 만남! 아이디어 샘솟는 창의력 뿜뿜 커플! 예측 불가능한 매력이 넘쳐요! 🎢"
    },
    "ISFP": {
        "INFJ": "🎨 감성 충만! 예술적인 영혼들의 만남! 조용히 서로를 응원하며 성장하는 관계! 🤫",
        "ESTP": "🤸‍♀️ 흥부자 ISFP와 ESTP! 같이 있으면 웃음이 끊이지 않는 비타민 커플! 🥳"
    },
    "ESFP": {
        "ISTJ": "🤷‍♀️ 극과 극의 끌림! 즉흥적인 ESFP와 계획적인 ISTJ! 서로에게 새로운 경험을 선물해 줄 거예요! 🎁",
        "ISFJ": "🤝 밝고 유쾌한 ESFP와 따뜻한 ISFJ! 서로에게 힘이 되어주는 든든한 응원군! 💪"
    },
    "ISTP": {
        "INFP": "🤔 서로의 영역 존중! 적당한 거리감으로 편안함을 유지하는 관계! 자유로운 영혼들!",
        "ENFJ": "🏃‍♀️🕺 에너지 넘치는 ENFJ와 시크한 ISTP! 겉은 달라 보여도 서로에게 끌리는 신기한 조합! 💥",
        "ESTP": "😎 시크 도도! 쿨내 진동! 비슷한 성향으로 서로를 잘 이해하는 관계! 같이 있으면 핵인싸! 😎"
    },
    "ESTP": {
        "ISFP": "🤸‍♀️ 흥부자 ISFP와 ESTP! 같이 있으면 웃음이 끊이지 않는 비타민 커플! 🥳",
        "ISTP": "😎 시크 도도! 쿨내 진동! 비슷한 성향으로 서로를 잘 이해하는 관계! 같이 있으면 핵인싸! 😎"
    },
    "ISFJ": {
        "ENFP": "😌 편안함 그 자체! 따뜻함과 배려로 가득한 관계! 지친 일상에 쉼표가 되어줄 거예요! 🌿",
        "ESFP": "🤝 밝고 유쾌한 ESFP와 따뜻한 ISFJ! 서로에게 힘이 되어주는 든든한 응원군! 💪"
    },
    "ESFJ": {
        "ISTJ": "🏡 안정적인 관계! 서로에게 믿음과 의지를 주는 든든한 커플! 미래를 함께 그려나갈 수 있어요! 🌳"
    },
    "ISTJ": {
        "ESFP": "🤷‍♀️ 극과 극의 끌림! 즉흥적인 ESFP와 계획적인 ISTJ! 서로에게 새로운 경험을 선물해 줄 거예요! 🎁",
        "ESFJ": "🏡 안정적인 관계! 서로에게 믿음과 의지를 주는 든든한 커플! 미래를 함께 그려나갈 수 있어요! 🌳"
    },
    "ESTJ": {
        "INFP": "😱 극과 극은 통한다?! 스파크 튀는 의외의 조합! 서로에게 새로운 세상을 선물해 줄 거예요! 💫"
    }
}


# 메인 화면에 결과 팡팡! 🎆
st.header(f"❤️‍🔥 {user_mbti}님과 {partner_mbti}님의 찐 궁합 결과는? ❤️‍🔥")

# 궁합 정보 가져오기 시도! ✨
try:
    compatibility = compatibility_data.get(user_mbti, {}).get(partner_mbti)
    if compatibility:
        st.balloons() # 풍선 파티!
        st.success(f"🎉 두구두구... 결과는?! \n\n {user_mbti}와 {partner_mbti}는 바로... \n\n **{compatibility}**")
        
        st.subheader("🕵️‍♀️ MBTI 전문가 제이미의 추가 꿀팁! 🍯")
        st.write(f"두 분의 관계는 이렇게 발전할 수 있어요! 🚀")
        st.markdown(f"""
        - **{user_mbti}님은**: {partner_mbti}님과의 관계에서 ✨새로운 경험✨을 얻을 수 있을 거예요.
        - **{partner_mbti}님은**: {user_mbti}님과 함께라면 💖정서적 안정감💖을 느낄 수 있답니다.
        """)
        
        # 📊 궁합 점수 차트로 시각화 (눈 돌아가는 화려함! 💖)
        st.subheader("📈 우리의 케미 지수는 몇 점? 📈")
        
        # 예시 데이터 (실제 궁합에 맞게 조절해야 더 찰떡! )
        categories = ['대화 점수 💬', '이해도 점수 🤔', '갈등해결력 💪', '꽁냥 지수 💑', '장기지속력 ♾️']
        # 랜덤 점수지만, 좀 더 드라마틱하게!
        values = np.random.randint(40, 100, 5) # 40-100 사이의 랜덤값으로 흥미롭게
        
        # 점수별 멘트 추가 (넘 화려한가? ㅋㅋㅋ)
        if values.mean() >= 80:
            st.success("💖 우와! 거의 완벽한 궁합이에요! 앞으로도 쭉 꽃길만 걸으세요! 🌸")
        elif values.mean() >= 60:
            st.info("👍 이 정도면 굿 조합! 서로 노력하면 더 빛나는 관계가 될 수 있어요! ✨")
        else:
            st.warning("⚠️ 조금 더 노력해봐야 할지도? 하지만 사랑은 노력하는 만큼 빛나는 법! 🌟")

        fig, ax = plt.subplots(figsize=(10, 6)) # 차트 크기 키워서 시원하게!
        
        # 이모지에 맞게 색상도 핑크핑크~ 보라보라~ 💜💖
        colors = ['#FFC0CB', '#DA70D6', '#BA55D3', '#9370DB', '#9932CC'] 
        ax.bar(categories, values, color=colors, alpha=0.8)
        
        ax.set_ylim(0, 100)
        ax.set_ylabel('✨ 반짝이는 점수 ✨', fontsize=14, color='purple')
        ax.set_title(f'🚀 {user_mbti}와 {partner_mbti}의 ✨환상적인✨ 관계 분석! 🚀', fontsize=16, color='deeppink')
        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='y', labelsize=12)
        plt.xticks(rotation=15) # 글자 겹치지 않게 살짝 돌리기
        plt.grid(axis='y', linestyle='--', alpha=0.7) # 그리드도 좀 더 밝게
        plt.tight_layout() # 여백 조절

        st.pyplot(fig)
        
    else:
        st.info("🤷‍♀️ 앗! 아직 이 조합의 찐 궁합 데이터는 준비중이에요! 😭 다른 조합을 픽해보시겠어요? 💖")

except KeyError:
    st.error("🚨 헉! 궁합 데이터를 불러오다가 에러가 났어요! 😅 다시 시도해주시겠어요? 😥")

st.markdown("---") # 줄 하나 넣어주고

# 추가 기능: 모든 MBTI와의 궁합 순위 보기 👑
if st.button("내 MBTI와 찰떡인 유형 순위 보기! 👑", help="가장 잘 맞는 MBTI 유형들을 알려드려요!"):
    st.subheader(f"💯 {user_mbti}님과 찐으로 잘 맞는 MBTI 순위는?! 💯")
    # 여기에 실제 MBTI 궁합 순위 로직과 데이터를 넣으면 대박!
    st.write("""
    1.  **ENFJ**: ✨ 영혼의 단짝! 환상적인 시너지! 🚀
    2.  **ENTJ**: 💡 지적인 자극! 함께라면 세상 정복 가능! 🌍
    3.  **INFJ**: 💖 깊은 이해! 서로를 알아주는 진정한 친구! 🥹
    4.  (나머지는 데이터 채워야겠죠?ㅋㅋㅋ)
    """)
    st.info("✨ 이 순위는 예시예요! 실제 데이터로 채워주세요! ✨")

st.markdown("---")
st.success("💖 당신의 아름다운 사랑을 응원해요! 💖")
st.write("궁금한 거 있으면 또 물어봐! 제이미가 다 알려줄게! 😎")
st.image("https://images.unsplash.com/photo-1517748831835-f0927e1f4095?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", caption="러블리 러블리 🎈", use_column_width=True)
