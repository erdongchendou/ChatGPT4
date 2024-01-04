from pathlib import Path
from datetime import datetime

import streamlit as st
from openai import OpenAI
from config.api_key import openai_api_key
from config.personal_info import introduction


role_definition = """
你是我的英语教练。
请将我的话改写成英文。
不需要逐字翻译。
请分析清楚我的内容，而后用英文重新逻辑清晰地组织它。
请使用地道的美式英语，纽约腔调。
请尽量使用日常词汇，尽量优先使用短语动词或者习惯用语。
每个句子最长不应该超过 20 个单词。
"""

st.title("ChatGPT4")
st.caption("利用Python调用GPT4的开发接口, 模拟的ChatGPT。 作者陈雷雷")


with st.sidebar:
    st.empty().markdown(introduction)
    option = st.selectbox(
        "聊天模式", ["英语练习", "聊天", "画图"], on_change=lambda: st.session_state.clear()
    )


if option == "聊天":
    number_of_choices = 1
else:
    number_of_choices = 2

if "messages" not in st.session_state:
    st.session_state["messages"] = []

    if option == "英语练习":
        st.session_state["messages"].extend(
            [
                {"role": "system", "content": role_definition},
                {"role": "assistant", "content": "我是你的英语学习助手, 请把你要学习的中文句子发给我"},
            ]
        )
    elif option == "聊天":
        st.session_state["messages"].extend(
            [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "assistant", "content": "我是GPT4, 有什么可以帮您"},
            ]
        )
    elif option == "画图":
        st.session_state["messages"].extend(
            [
                {"role": "assistant", "content": "我是Dalle3, 你想画什么图，请把对应的描述发给我"},
            ]
        )


for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue

    if "img" in msg["content"] and "https:" in msg["content"]:
        st.chat_message(msg["role"]).image(msg["content"])
    elif "mp3" in msg["content"]:
        st.chat_message(msg["role"]).audio(msg["content"])
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
    elif option == "画图":
        response = client.images.generate(
            model="dall-e-3", prompt=prompt, size="1024x1024", quality="standard", n=1
        )
        image_url = response.data[0].url
        st.chat_message(msg["role"]).image(image_url)
        st.session_state.messages.append({"role": "assistant", "content": image_url})
    elif option == "英语练习":
        rspd_translation = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=st.session_state.messages,
            n=number_of_choices,
        )

        voice_performer = "alloy"
        date = datetime.now().strftime("%Y%m%d")
        Path(date).mkdir(parents=True, exist_ok=True)

        for rspd in rspd_translation.choices:
            index = rspd.index + 1
            content = rspd.message.content
            rspd_with_num = f"{index}.{content}\n\n"
            st.chat_message("assistant").empty().markdown(rspd_with_num)

            # alloy, echo, fable, onyx, nova, and shimmer, the last two of which are femail voices.
            datetime_with_second = datetime.now().strftime("%Y%m%d_%H%M%S")
            speech_file_path = f"{date}/{datetime_with_second}.mp3"

            rspd_audio = client.audio.speech.create(
                model="tts-1",
                voice=voice_performer,
                input=content,
            )

            rspd_audio.stream_to_file(speech_file_path)
            st.chat_message("assistant").audio(speech_file_path)

            st.session_state.messages.append({"role": "assistant", "content": content})
            st.session_state.messages.append(
                {"role": "assistant", "content": speech_file_path}
            )
