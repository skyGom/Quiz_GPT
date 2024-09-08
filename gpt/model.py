from langchain.chat_models import ChatOpenAI
from langchain.callbacks import StreamingStdOutCallbackHandler

from gpt.functions import FUNCTION

import openai

def create_llm(key):
    return ChatOpenAI(
        temperature=0.1,
        model="gpt-4o-mini-2024-07-18",
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
        api_key=key,
    ).bind(
        function_call={
            "name":"create_quiz",
        },
        functions = [FUNCTION],
    )
    
def is_valid_openai_key(key):
    try:
        openai.api_key = key
        openai.Model.list()
        return True
    except Exception as e:
        return False