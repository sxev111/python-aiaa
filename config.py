import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Configuration
API_KEY = os.getenv("OPENAI_API_KEY", "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")
MODEL = "gpt-3.5-turbo"  # or "gpt-4" for better results
TEMPERATURE = 0.7

# Desktop App Configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
APP_TITLE = "Python AI Assistant"
