import streamlit as st
from utils.utils import (
    init_messages,
    set_title,
    choose_mode,
    show_messages,
    show_stream_chat,
    generate_image,
    generate_audio,
)
from utils.role_definition import role_definitions
from ai_bots.openai_bot import OpenAIBot

set_title(st)
choose_mode(st)
init_messages(st)
show_messages(st)
ai_bot = OpenAIBot()

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if st.session_state.mode == "聊天":
        show_stream_chat(st, ai_bot)

    elif st.session_state.mode == "画图":
        generate_image(st, ai_bot, prompt)

    elif st.session_state.mode == "英语练习":
        generate_audio(st, ai_bot, prompt)
