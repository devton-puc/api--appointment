import os
from dotenv import load_dotenv


if not os.getenv("GEMINI_TOKEN"):
    load_dotenv()

OPENAI_TOKEN = os.getenv("GEMINI_TOKEN")
GEMINI_AI_URL = os.getenv("GEMINI_AI_URL")
