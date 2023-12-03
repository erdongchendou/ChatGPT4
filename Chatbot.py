import streamlit as st
from openai import OpenAI
from config.api_key import openai_api_key
from config.personal_info import introduction


st.title("ChatGPT4")
st.caption("利用Python调用GPT4的开发接口, 模拟ChatGPT的功能。 作者陈雷雷")

with st.sidebar:
    st.empty().markdown(introduction)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "我是GPT4，有什么可以帮您？"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

client = OpenAI(api_key=openai_api_key)
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

    for chunk in client.chat.completions.create(
        model="gpt-4-1106-preview", messages=st.session_state.messages, stream=True
    ):
        if chunk.choices[0].finish_reason != "stop":
            full_response += chunk.choices[0].delta.content
            message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
