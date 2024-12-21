import streamlit as st
from utils import print_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Streamlit App", page_icon=":tada:")
st.title("Streamlit ChatGPT App")
# st.write("This is a simple Streamlit app.")

# 메시지 지속성을 위한 세션 생성
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화기록을 출력해 주는 코드
print_messages()

if user_input := st.chat_input("메시지를 입력해 주세요 : "):
    # 사용자 입력한 메시지 출력
    st.chat_message("user").write(f"{user_input}")
    st.session_state.messages.append(ChatMessage(role="user", content=user_input))

    # LLM을 사용하여 AI의 답변 생성
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        """질문에 대하여 간결하게 답변해 주세요. 
        {question}
        """)
    chain = prompt | llm | StrOutputParser()     # 출력파서까지 체인에 연결하여 문자열 출력하게 함
    msg = chain.invoke({"question": user_input})
    # msg = response.content  

    # AI의 답변 출력
    with st.chat_message("assistant"):
        st.write(msg) 
        st.session_state.messages.append(ChatMessage(role="assistant", content=msg))


