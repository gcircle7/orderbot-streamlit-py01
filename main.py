import os
import streamlit as st

from utils import print_messages, StreamHandler
from langchain_openai import ChatOpenAI
from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from langchain_community.chat_message_histories import ChatMessageHistory 
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Streamlit App", page_icon=":tada:")
st.title("Streamlit ChatGPT App")
# st.write("This is a simple Streamlit app.")

# 메시지 지속성을 위한 세션 생성
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 대화 기록 저장하는 store 세션 상태 변수 
if "store" not in st.session_state:
    st.session_state.store = dict()

with st.sidebar:
    session_id = st.text_input("Session ID", value="abc123")

    clear_button = st.button("Clear")
    if clear_button:
        st.session_state.messages = []
        # st.session_state.store = dict()
        st.rerun()

def get_session_history(session_ids: str) -> BaseChatMessageHistory:
    # print(f"session_ids: {session_ids}")
    if session_ids not in st.session_state.store:
        # 새로운 ChatMessageHistory 객체 생성하여 저장
        st.session_state.store[session_ids] = ChatMessageHistory()
    return st.session_state.store[session_ids]

# 이전 대화기록을 출력해 주는 코드
print_messages()

if user_input := st.chat_input("메시지를 입력해 주세요 : "):
    # 사용자 입력한 메시지 출력
    st.chat_message("user").write(f"{user_input}")
    st.session_state.messages.append(ChatMessage(role="user", content=user_input))

    # LLM을 사용하여 AI의 답변 생성

    # AI의 답변 출력
    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
            
        # 1. 모델 생성
        # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        llm = ChatOpenAI(streaming=True, callbacks=[stream_handler])

        # 2. 프롬프트 생성
        prompt = ChatPromptTemplate.from_messages([
            ("system", "질문에 대하여 간결하게 답변해 주세요."),
            # 대화 기록을 변수로 사용, history가 MessageHistory 의 key 가 됨
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),  
        ])
        # 3. 체인 생성  
        chain = prompt | llm 

        # 4. 메시지 기록관리 객체 생성
        chain_with_memory =  RunnableWithMessageHistory( # RunnableWithMessageHistory 메시지 기록관리 객체 생성
            chain, # 실행할 Runnable 객체
            get_session_history, # 세션 기록을 가져오는 함수
            input_messages_key="question", # 사용자 질문의 키
            history_messages_key="history", # 기록 메시지 키
        )

        # 5. 체인 실행
        response = chain_with_memory.invoke({"question": user_input},
                                            # 세션ID 설정
                                            config={"configurable": {"session_id": session_id}},
                                            )
        st.session_state.messages.append(ChatMessage(role="assistant", content=response.content ))


