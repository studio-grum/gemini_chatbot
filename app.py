import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="Gemini 챗봇", page_icon="💬")

# API 키 설정
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 모델 설정
model = genai.GenerativeModel('gemini-1.5-flash')

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 제목 표시
st.title("💬 Gemini 챗봇")

# 채팅 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요"):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini 응답 생성
    with st.chat_message("assistant"):
        # 이전 대화 내용을 컨텍스트로 포함
        chat = model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]}
            for m in st.session_state.messages[:-1]
        ])
        
        response = chat.send_message(prompt)
        st.markdown(response.text)
        
        # 어시스턴트 응답 저장
        st.session_state.messages.append({"role": "assistant", "content": response.text})
