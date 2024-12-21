from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import ChatOpenAI

chat_model = ChatOpenAI()

# content = "코딩"

# response = chat_model.predict(content)

# print(response)

import streamlit as st

st.title("코딩 챗봇")

content = st.text_input("코딩 챗봇에게 물어보세요.")

if content:
    response = chat_model.predict(content)
    st.text_area("챗봇의 답변", value=response)

