# test.py
from config import Config

# Test de configuratie
Config.validate()
print("OpenAI API Key:", Config.OPENAI_API_KEY[:8] + "..." if Config.OPENAI_API_KEY else "Not found")