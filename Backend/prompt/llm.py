# llm.py
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
from llama_index.llms.gemini import Gemini
from connection.config import GEMINI_API_KEY


# Initialize token counter and callback manager
token_counter = TokenCountingHandler(verbose=False)
callback_manager = CallbackManager([token_counter])

# Initialize LLM with callback manager
llm = Gemini(
    model="models/gemini-1.5-flash",
    api_key=GEMINI_API_KEY,
    callback_manager=callback_manager
)
