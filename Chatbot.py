import streamlit as st
from openai import OpenAI
from config.api_key import openai_api_key
from config.personal_info import introduction


st.title("ChatGPT4")
st.caption("利用Python调用GPT4的开发接口, 模拟的ChatGPT。 作者陈雷雷")

with st.sidebar:
    st.empty().markdown(introduction)
    option = st.selectbox("聊天模式", ["聊天", "画图"])

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "我是GPT4，有什么可以帮您？"}]

for msg in st.session_state.messages:
    if "img" in msg["content"] and "https:" in msg["content"]:
        st.image(msg["content"], caption="生成的图像")
    else:
        st.chat_message(msg["role"]).write(msg["content"])

client = OpenAI(api_key=openai_api_key)
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if option == "聊天":
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
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
    else:
        response = client.images.generate(
            model="dall-e-3", prompt=prompt, size="1024x1024", quality="standard", n=1
        )
        image_url = response.data[0].url
        st.image(image_url, caption="生成的图像")
        st.session_state.messages.append({"role": "assistant", "content": image_url})
