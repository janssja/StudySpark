# config.py
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    SESSION_TYPE = 'filesystem'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    @classmethod
    def validate(cls):
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY niet gevonden in environment variables. "
                           "Zorg ervoor dat je .env file een OPENAI_API_KEY bevat.")