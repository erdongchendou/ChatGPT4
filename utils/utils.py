from pathlib import Path
from datetime import datetime
from .role_definition import role_definitions
from config.personal_info import introduction


def init_messages(st):
    if "messages" not in st.session_state:
        chat_mode = st.session_state.mode
        st.session_state["messages"] = []
        st.session_state["messages"].extend(role_definitions[chat_mode])


def set_title(st):
    st.title("ChatGPT4")
    st.caption("利用Python调用GPT4的开发接口, 模拟的ChatGPT。 作者陈雷雷")


def choose_mode(st):
    with st.sidebar:
        st.empty().markdown(introduction)
        st.session_state.mode = st.selectbox(
            "聊天模式",
            list(role_definitions.keys()),
            on_change=lambda: st.session_state.clear(),
        )

        if st.session_state.mode == "英语练习":
            st.session_state.number_of_choices = st.selectbox(
                "生成个数", list(range(1, 10))
            )
            st.session_state.voice = st.selectbox(
                "声音", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
            )


def show_messages(st):
    for msg in st.session_state.messages:
        if msg["role"] == "system":
            continue

        if "img" in msg["content"] and "https:" in msg["content"]:
            st.chat_message(msg["role"]).image(msg["content"])
        elif "mp3" in msg["content"]:
            st.chat_message(msg["role"]).audio(msg["content"])
        else:
            st.chat_message(msg["role"]).write(msg["content"])
    return msg


def show_stream_chat(st, ai_bot):
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

    for content in ai_bot.stream_chat(st):
        full_response += content
        message_placeholder.markdown(full_response + "▌")

    message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})


def generate_image(st, ai_bot, prompt):
    image_url = ai_bot.generate_image(prompt)
    st.chat_message("assistant").image(image_url)

    st.session_state.messages.append({"role": "assistant", "content": image_url})


def generate_audio(st, ai_bot, prompt):
    rspd_translation = ai_bot.chat(st)
    date = datetime.now().strftime("%Y%m%d")
    Path(date).mkdir(parents=True, exist_ok=True)

    for rspd in rspd_translation.choices:
        datetime_with_second = datetime.now().strftime("%Y%m%d_%H%M%S")
        speech_file_path = f"{date}/{datetime_with_second}.mp3"

        content = rspd.message.content
        rspd_with_num = f"{rspd.index + 1}.{content}\n\n"
        st.chat_message("assistant").empty().markdown(rspd_with_num)

        rspd_audio = ai_bot.generate_audio(st, content)
        rspd_audio.stream_to_file(speech_file_path)

        st.chat_message("assistant").audio(speech_file_path)
        st.session_state.messages.append({"role": "assistant", "content": content})
        st.session_state.messages.append(
            {"role": "assistant", "content": speech_file_path}
        )
