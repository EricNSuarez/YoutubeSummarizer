import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "o3-mini")
    MAX_INPUT_LENGTH = int(os.getenv("MAX_INPUT_LENGTH", 4096))
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-123")