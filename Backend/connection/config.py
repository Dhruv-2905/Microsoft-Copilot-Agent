# config.py
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import Settings
import os
from dotenv import load_dotenv

load_dotenv()

host=os.getenv("HOST")
port=os.getenv("PORT")
user=os.getenv("USER")
password=os.getenv("PASSWORD")
database=os.getenv("DATABASE")

GEMINI_API_KEY=os.getenv("GOOGLE_API_KEY") 
embed_model = GeminiEmbedding(model_name="models/embedding-001", api_key=GEMINI_API_KEY)
Settings.embed_model = embed_model


DB_CONFIG = {
    "HOST": host,
    "PORT": port,
    "USER": user,
    "PASSWORD": password,
    "DATABASE": database
}

TABLES_VIEWS = os.getenv("TABLES_VIEWS", "").split(",")

