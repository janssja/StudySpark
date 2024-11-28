# app/advisor.py
from datetime import datetime
import json
from config import Config
from openai import OpenAI
from app.vectorstore.query_engine import QueryEngine

# Initialize OpenAI client after Config import
client = OpenAI(api_key=Config.OPENAI_API_KEY)

class StudyAdvisor:
    def __init__(self):
        self.conversation_history = []
        self.current_stage = "introduction"
        self.stages = [
            "introduction",
            "interests",
            "skills",
            "learning_style",
            "future_goals",
            "constraints",
            "summary",
            "recommendations"
        ]
        self.student_profile = {
            "interests": [],
            "skills": [],
            "learning_style": "",
            "future_goals": [],
            "constraints": []
        }
        # Initialize the query engine
        self.query_engine = QueryEngine()

    def process_message(self, message):  # This is the main entry point
        """Process incoming message and generate response"""
        # Add user message to history
        self.add_to_history("user", message)

        # Generate response using OpenAI
        response = self.generate_response(message)

        # Add response to history
        self.add_to_history("assistant", response)

        return {
            "response": response,
            "stage": self.current_stage
        }
    
    def get_relevant_program_info(self, query):
        """Get relevant program information from the vectorstore"""
        try:
            results = self.query_engine.query_catalog(query, k=3)
            if results:
                # Combine the content from all results
                return "\n\n".join([doc.page_content for doc in results])
            return ""
        except Exception as e:
            print(f"Error querying vectorstore: {str(e)}")
            return ""

    def generate_response(self, user_message):
        # Bouw de systeem prompt op basis van de huidige fase
        system_prompt = self.get_system_prompt()

        # Get relevant program information based on the current stage and message
        if self.current_stage in ["interests", "recommendations"]:
            # Construct search query based on user message and profile
            search_query = user_message
            if self.student_profile["interests"]:
                search_query += " " + " ".join(self.student_profile["interests"])
            
            program_info = self.get_relevant_program_info(search_query)
            if program_info:
                system_prompt += f"\n\nRelevante opleidingsinformatie uit de PXL catalogus:\n{program_info}"

        # Bereid de messages voor
        messages = [
            {"role": "system", "content": system_prompt},
        ]

        # Voeg relevante geschiedenis toe
        for msg in self.conversation_history[-4:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        try:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )

            response = completion.choices[0].message.content

            # Update student profile als we nuttige informatie hebben
            self.update_student_profile(user_message, response)

            # Ga naar volgende fase indien nodig
            self.advance_stage_if_needed(response)

            return response

        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return "Er is een fout opgetreden. Kun je je vraag opnieuw stellen?"

    def get_system_prompt(self):
        base_prompt = """
    Jij bent StudySpark, de AI-studiekeuzeadviseur van Hogeschool PXL. Je bent vriendelijk, behulpzaam en persoonlijk in je communicatie.

    Je belangrijkste taken zijn:
    1. Het leren kennen van de student en hun voorkeuren
    2. Het matchen van hun profiel met geschikte PXL-opleidingen
    3. Het geven van accurate informatie over opleidingen op basis van de officiële PXL-studiegids

    Richtlijnen voor je communicatie:
    - Gebruik een informele, persoonlijke toon
    - Spreek de student aan met 'je' en 'jij'
    - Stel gerichte vragen om meer te weten te komen
    - Verwijs naar specifieke aspecten uit de studiegids wanneer relevant
    - Wees eerlijk over voor- en nadelen van opleidingen

    Als je informatie geeft over opleidingen:
    1. Baseer je ALLEEN op de informatie uit de PXL-studiegids die je krijgt
    2. Als je iets niet zeker weet, verwijs dan naar de PXL-website of studieadviseurs
    3. Gebruik concrete voorbeelden en details uit het studieprogramma
    4. Leg uit waarom bepaalde aspecten wel of niet bij de student passen

    Voor elke opleiding, overweeg:
    1. De match tussen het programma en de interesses van de student
    2. De aansluiting bij de leerstijl en vaardigheden
    3. De haalbaarheid gezien de vooropleiding en context
    4. De toekomstperspectieven en carrièremogelijkheden
    """

        stage_prompts = {
            "introduction": """
    Stel jezelf voor en begin het gesprek op een vriendelijke manier. 
    Vraag naar de naam van de student en gebruik deze in je antwoorden.
    Vraag naar hun huidige situatie en eerste gedachten over studiekeuze.
    """,

            "interests": """
    Analyseer de genoemde interesses en vraag door naar specifieke voorkeuren.
    Als er interesses worden genoemd die aansluiten bij PXL-opleidingen, gebruik dan de specifieke informatie uit de studiegids om hierop in te gaan.
    Focus op:
    - Concrete voorbeelden van wat de student interessant vindt
    - Waarom bepaalde onderwerpen hen aanspreken
    - Praktische vs theoretische interesses
    """,

            "skills": """
    Vraag naar concrete voorbeelden van vaardigheden en prestaties.
    Let vooral op:
    - Schoolprestaties in relevante vakken
    - Praktische vaardigheden en ervaring
    - Soft skills zoals communicatie en samenwerking
    - Technische of specifieke vaardigheden die aansluiten bij PXL-opleidingen
    """,

            "learning_style": """
    Onderzoek hun ideale leeromgeving en -methode:
    - Praktisch vs. theoretisch leren
    - Individueel vs. groepswerk
    - Projectmatig vs. traditioneel onderwijs
    - Voorkeur voor bepaalde werkvormen
    Relateer hun voorkeuren aan de onderwijsmethoden bij PXL.
    """,

            "future_goals": """
    Verken hun toekomstambities:
    - Gewenste beroepen of sectoren
    - Belangrijke waarden in werk
    - Ambities op korte en lange termijn
    Koppel deze aan concrete opleidingen en beroepsperspectieven bij PXL.
    """,

            "constraints": """
    Bespreek praktische overwegingen:
    - Reistijd en bereikbaarheid
    - Studieduur en studielast
    - Specifieke vereisten of voorkennis
    - Financiële aspecten
    Geef concrete informatie over deze aspecten bij PXL.
    """,

            "summary": f"""
    Vat het gesprek samen met focus op:
    - Kerninteresses: {', '.join(self.student_profile['interests'])}
    - Belangrijkste vaardigheden: {', '.join(self.student_profile['skills'])}
    - Leerstijl: {self.student_profile['learning_style']}
    - Toekomstdoelen: {', '.join(self.student_profile['future_goals'])}
    - Praktische overwegingen: {', '.join(self.student_profile['constraints'])}

    Vraag of dit beeld klopt en of er nog aanvullingen nodig zijn.
    """,

            "recommendations": f"""
    Geef gedetailleerd advies over de best passende PXL-opleidingen.
    Baseer je op:
    1. De informatie uit het studentenprofiel
    2. De details uit de PXL-studiegids
    3. De match tussen student en opleiding

    Gebruik dit format voor elke aanbeveling:

    1. [Naam opleiding]
    - Waarom deze opleiding past bij de student (specifieke matches)
    - Belangrijkste vakken en programmakenmerken
    - Onderwijsmethoden en aansluiting bij leerstijl
    - Toekomstperspectieven
    - Praktische informatie en eventuele aandachtspunten

    Student profiel: {json.dumps(self.student_profile, indent=2)}
    """
        }

        return base_prompt + "\n\n" + stage_prompts.get(self.current_stage, "")

    def update_student_profile(self, user_message, ai_response):
        # Analyseer het antwoord van de student op basis van de huidige fase
        if self.current_stage == "interests":
            # Extractie prompt voor interesses
            extraction_prompt = f"""
            Analyseer dit gespreksfragment en extraheer de belangrijkste interesses van de student.
            Geef alleen een lijst van interesses terug in JSON-formaat.
            
            Student: {user_message}
            Advisor: {ai_response}
            """

            try:
                extraction = client.chat.completions.create(model="gpt-4o",
                messages=[
                    {"role": "system", "content": extraction_prompt}
                ],
                temperature=0.3)

                interests = json.loads(extraction.choices[0].message.content)
                self.student_profile["interests"].extend(interests)
            except:
                pass  # Silent fail if extraction fails

        # Vergelijkbare extractie voor andere fases...
        # (skills, learning_style, future_goals, constraints)

    def advance_stage_if_needed(self, ai_response):
        # Analyseer of het antwoord voldoende informatie bevat om door te gaan
        analysis_prompt = f"""
        Analyseer dit antwoord en bepaal of we voldoende informatie hebben verzameld voor de huidige fase "{self.current_stage}".
        Antwoord alleen met "ja" of "nee".

        Antwoord: {ai_response}
        """

        try:
            analysis = client.chat.completions.create(model="gpt-4o",
            messages=[
                {"role": "system", "content": analysis_prompt}
            ],
            temperature=0.3)

            should_advance = analysis.choices[0].message.content.strip().lower() == "ja"

            if should_advance:
                current_index = self.stages.index(self.current_stage)
                if current_index < len(self.stages) - 1:
                    self.current_stage = self.stages[current_index + 1]
        except:
            pass  # Silent fail if analysis fails

    def add_to_history(self, role, content):
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })