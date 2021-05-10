from dotenv import load_dotenv
import os

load_dotenv()

class ENV:
    API_KEY = os.getenv("API_KEY")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_ADDRESS = os.getenv("MAIL_ADDRESS")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
