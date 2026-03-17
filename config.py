import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Configuration
API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
MODEL = "gpt-3.5-turbo"  # or "gpt-4" for better results
TEMPERATURE = 0.7

# Desktop App Configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
APP_TITLE = "Python AI Assistant"