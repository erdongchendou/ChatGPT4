from openai import OpenAI
from config.api_key import openai_api_key


class OpenAIBot:
    def __init__(self):
        self.client = OpenAI(api_key=openai_api_key)
        self.chat_model = "gpt-4-1106-preview"
        self.draw_model = "dall-e-2"
        self.tts_model = "tts-1"

    def stream_chat(self, st):
        for chunk in self.client.chat.completions.create(
            model=self.chat_model, messages=st.session_state.messages, stream=True
        ):
            if chunk.choices[0].finish_reason != "stop":
                yield chunk.choices[0].delta.content

    def generate_image(self, st):
        response = self.client.images.generate(
            model=self.draw_model,
            prompt=st.session_state.messages[-1]["content"],
            size=st.session_state.image_size,
            quality=st.session_state.image_quality,
            n=st.session_state.number_of_choices,
        )
        return response

    def chat(self, st):
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=st.session_state.messages,
            n=st.session_state.number_of_choices,
        )
        return response

    def generate_audio(self, st):
        response = self.client.audio.speech.create(
            model=self.tts_model,
            voice=st.session_state.voice,
            input=st.session_state.messages[-1]["content"],
        )
        return response
