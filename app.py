import streamlit as st
import json
import time

# [설정] 페이지 기본 설정
st.set_page_config(
    page_title="동화 만들기 마법사", 
    page_icon="https://github.com/maychrissj-ging/fairy-tale/blob/main/logo.png?raw=true", 
    layout="centered"
)

# [CSS] 파트너님의 귀여운 폰트와 스타일 적용
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&family=Nanum+Pen+Script&family=Black+Han+Sans&display=swap');
    
    * { font-family: 'Jua', sans-serif; }
    .stApp { background-color: #fef9f0; }
    h1 { color: #764ba2; text-align: center; font-family: 'Black Han Sans', sans-serif; font-size: 2.5rem; text-shadow: 2px 2px #f093fb; }
    .story-box { background: white; padding: 20px; border-radius: 20px; border: 3px solid #c9b8f8; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .story-text { font-family: 'Nanum Pen Script', cursive; font-size: 1.5rem; color: #2c2c54; line-height: 1.8; }
    .ai-label { color: #ff6b6b; font-size: 0.9rem; margin-bottom: 5px; }
    .user-label { color: #4ecdc4; font-size: 0.9rem; margin-bottom: 5px; text-align: right; }
    .ai-bubble { background: #fff0f5; padding: 15px; border-radius: 15px; margin-bottom: 10px; border-left: 4px solid #ffb347; }
    .user-bubble { background: #f0f4ff; padding: 15px; border-radius: 15px; margin-bottom: 10px; border-right: 4px solid #4ecdc4; text-align: right; }
</style>
""", unsafe_allow_html=True)

# [상태 관리] 기승전결 단계 및 데이터 저장소 초기화
STAGES = ['기', '승', '전', '결']
STAGE_NAMES = {'기': '시작', '승': '전개', '전': '위기', '결': '마무리'}
STAGE_ICONS = {'기': '🌱', '승': '🚀', '전': '⚡', '결': '🌈'}

if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 0
if 'story_segments' not in st.session_state:
    st.session_state.story_segments = [] # [{'role': 'ai', 'text': '...', 'stage': '기'}, ...]
if 'ai_question' not in st.session_state:
    st.session_state.ai_question = "오늘의 동화 주인공은 누구인가요? 이름과 어떤 친구인지 알려주세요! 🐰"
if 'ai_suggestions' not in st.session_state:
    st.session_state.ai_suggestions = ["토끼 소녀 달이", "용감한 소년 하늘이", "작은 마법사 별이"]

# [API 함수] 실제 서비스 시 이 부분에 Anthropic API 코드를 활성화합니다.
def get_ai_response(user_text, next_stage):
    # 실제 API 호출 코드가 들어갈 자리입니다. 
    # 지금은 파트너님의 테스트를 위해 Fallback(임시) 데이터를 반환하도록 설정했습니다.
    time.sleep(1) # API 대기 시간 흉내
    fallbacks = {
        '승': {'story': f"주인공은 {user_text}에서 신나는 모험을 시작했어요!", 'q': '이제 신나는 일이 일어났어요! 어떤 일이 생겼을까요?', 's': ['무서운 괴물이 나타났어요', '보물 지도를 발견했어요', '새 친구를 만났어요']},
        '전': {'story': f"그러던 중, 갑자기 놀라운 일이 벌어졌답니다.", 'q': '앗, 갑자기 큰일이 생겼어요! 어떤 위기였나요?', 's': ['친구가 위험에 빠졌어요', '보물이 사라졌어요', '길을 잃어버렸어요']},
        '결': {'story': f"정말 큰 위기였지만, 포기하지 않았어요.", 'q': '마지막으로 어떻게 문제를 해결했나요?', 's': ['모두 힘을 합쳐 해결했어요', '마법의 힘으로 이겼어요', '용기를 내서 해냈어요']},
        '완성': {'story': f"그렇게 모두 행복하게 살았답니다!", 'q': '', 's': []}
    }
    return fallbacks.get(next_stage, fallbacks['완성'])

# [UI 구현] 메인 화면
st.markdown("<h1>✨ 동화 만들기 마법사 ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>함께 신나는 이야기를 만들어 보아요! 🎉</p>", unsafe_allow_html=True)

# 1. 진행률 바 (Progress Bar)
progress_val = int(((st.session_state.current_stage) / 4) * 100)
st.progress(progress_val)

# 2. 동화책 본문 영역
if st.session_state.story_segments:
    st.markdown('<div class="story-box">', unsafe_allow_html=True)
    for seg in st.session_state.story_segments:
        if seg['role'] == 'ai':
            st.markdown(f"""
            <div class="ai-bubble">
                <div class="ai-label">🧚 마법사가 이어쓴 이야기 [{seg['stage']}]</div>
                <div class="story-text">{seg['text']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="user-bubble">
                <div class="user-label">👦 내가 쓴 이야기 [{seg['stage']}]</div>
                <div class="story-text">{seg['text']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("📚 아직 빈 책이에요. 이야기를 시작해 보세요!")

# 3. 입력 및 진행 로직 (기승전결 진행 중일 때)
if st.session_state.current_stage < 4:
    stage_key = STAGES[st.session_state.current_stage]
    
    # AI 질문 카드
    st.warning(f"🧚 마법사가 묻는다!\n\n**{st.session_state.ai_question}**")
    
    # 추천 선택지 버튼들 (가로로 배치)
    cols = st.columns(len(st.session_state.ai_suggestions))
    selected_suggestion = None
    for i, col in enumerate(cols):
        if col.button(st.session_state.ai_suggestions[i], use_container_width=True):
            selected_suggestion = st.session_state.ai_suggestions[i]
            
    # 사용자 입력창
    user_input = st.chat_input(placeholder="여기에 이야기를 써 주세요... ✏️")
    
    # 입력 처리 (버튼 클릭 또는 텍스트 입력 시)
    final_input = selected_suggestion if selected_suggestion else user_input
    
    if final_input:
        # 사용자가 쓴 내용 저장
        st.session_state.story_segments.append({'role': 'user', 'text': final_input, 'stage': stage_key})
        
        # 다음 단계 계산
        next_index = st.session_state.current_stage + 1
        next_stage_key = STAGES[next_index] if next_index < 4 else '완성'
        
        # AI 응답 가져오기
        with st.spinner("✨ 마법을 부리는 중..."):
            ai_data = get_ai_response(final_input, next_stage_key)
            
            # AI가 이어 쓴 내용 저장
            st.session_state.story_segments.append({'role': 'ai', 'text': ai_data['story'], 'stage': next_stage_key})
            
            # 다음 질문 세팅
            st.session_state.ai_question = ai_data['q']
            st.session_state.ai_suggestions = ai_data['s']
            
            # 단계 넘어가기
            st.session_state.current_stage += 1
            st.rerun()

# 4. 완성 화면 (결 단계까지 모두 마쳤을 때)
if st.session_state.current_stage >= 4:
    st.success("🎉 짜잔! 우리만의 동화책이 완성되었어요!")
    st.balloons() # 스트림릿의 내장 풍선 애니메이션 효과!
    
    if st.button("🔄 새 이야기 만들기", use_container_width=True):
        st.session_state.clear()

        st.rerun()


