try:
    from entext.settings import OPENAI_KEY, SYSTEM_PROMPT
except ImportError:
    from settings import OPENAI_KEY, SYSTEM_PROMPT

import openai


class OpenAI:
    def __init__(self):
        ...

    @staticmethod
    def parse(text) -> str:
        """
        Parse the text using OpenAI's GPT-3 API.
        :param text: the text to parse
        :return: None
        """
        openai.api_key = OPENAI_KEY
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ]

        chat = openai.chat.completions.create(model="gpt-4", messages=messages)

        reply = chat.choices[0].message.content

        return reply
