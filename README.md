# StudySpark

Een Flask-gebaseerde applicatie voor het beheren en analyseren van vectordata. Deze applicatie maakt gebruik van een vectorstore voor efficiënte gegevensopslag en -verwerking.

## Features

- Vector data opslag en beheer
- Flask web interface
- Real-time verwerking
- Debugger ondersteuning
- REST API endpoints

## Vereisten

- Python 3.x
- pip (Python package manager)
- Virtual environment

## Installatie

1. Clone deze repository:
```bash
git clone https://github.com/janssja/StudySpark.git
cd StudySpark
```

2. Maak een virtual environment aan en activeer deze:
```bash
python -m venv venv
source venv/bin/activate  # Voor Linux/Mac
# OF
venv\Scripts\activate     # Voor Windows
```

3. Installeer de benodigde packages:
```bash
pip install -r requirements.txt
```

## Configuratie

1. Controleer of het `config.py` bestand aanwezig is
2. Pas indien nodig de configuratie aan voor jouw omgeving

## Gebruik

1. Activeer de virtual environment (indien nog niet actief):
```bash
source venv/bin/activate  # Voor Linux/Mac
# OF
venv\Scripts\activate     # Voor Windows
```

2. Start de applicatie:
```bash
python run.py
```

De applicatie is nu beschikbaar op: `http://127.0.0.1:5000`

## Project Structuur

```
StudySpark/
├── __pycache__/
├── app/
├── catalogs/
│   └── cataloog_lezen.py
├── flask_session/
├── config.py
├── requirements.txt
├── run.py
├── setup_vectorstore.py
└── test_vectorstore.py
```

## Development

Voor ontwikkeling draait de server standaard in debug mode met de volgende features:
- Debug mode: Aan
- Automatisch herladen bij code wijzigingen
- Debugger PIN wordt gegenereerd bij opstarten

**Let op:** De development server is niet bedoeld voor productie. Gebruik een productie WSGI server voor deployment.

## Testing

Om de tests uit te voeren:
```bash
python test_vectorstore.py
```

## API Endpoints

De applicatie biedt verschillende API endpoints:
- GET / - Hoofdpagina
- GET /static/js/chat.js - Chat functionaliteit
- GET /static/css/main.css - Styling
- POST /api/chat - Chat API endpoint

## Bijdragen

1. Fork de repository
2. Maak een nieuwe branch (`git checkout -b feature/nieuwe-feature`)
3. Commit je wijzigingen (`git commit -am 'Voeg nieuwe feature toe'`)
4. Push naar de branch (`git push origin feature/nieuwe-feature`)
5. Maak een Pull Request aan
