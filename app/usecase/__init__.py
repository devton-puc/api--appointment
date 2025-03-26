import os
from dotenv import load_dotenv


if not os.getenv("OPENAI_TOKEN"):
    load_dotenv()

OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
