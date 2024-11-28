import json
import fitz  # PyMuPDF voor PDF-verwerking

# Functie om specifieke secties van de PDF te extraheren
def extract_study_directions(pdf_path):
    data = []
    
    with fitz.open(pdf_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text = page.get_text("text")
            # Sectie opdelen voor elk programma door te zoeken naar de patroonwoorden zoals "Jij wil" enz.
            if "Professionele bachelor" in text or "Academische bachelor" in text:
                program_data = parse_program_details(text)
                if program_data:
                    data.append(program_data)
    
    return data

def parse_program_details(text):
    # Split en verwerk tekst om secties zoals "Jij wil" enz. op te halen
    program = {}
    lines = text.splitlines()
    
    # Dummy placeholders, hier komt logica om de juiste secties te herkennen
    program["department"] = extract_department(lines)
    program["program_type"] = extract_program_type(lines)
    program["program_name"] = extract_program_name(lines)
    program["specializations"] = extract_specializations(lines)
    
    # Subsecties beschrijven
    description = {}
    description["overview"] = extract_section_text(lines, "Jij wil")
    description["program_details"] = extract_section_text(lines, "Jouw opleiding")
    description["extra"] = extract_section_text(lines, "Net dat tikkeltje meer")
    description["career_perspective"] = extract_section_text(lines, "Jouw toekomst")
    description["study_modes"] = extract_study_modes(lines)
    
    program["description"] = description
    return program

# Helpers voor het ophalen van secties
def extract_department(lines):
    # Specifieke logica om de afdeling te vinden
    return "PXL-Business"  # Voorbeeldwaarde

def extract_program_type(lines):
    # Zoek in regels naar woorden als "Professionele bachelor"
    return "Professionele bachelor"  # Voorbeeldwaarde

def extract_program_name(lines):
    # Logica om de programma naam te extraheren
    return "Bedrijfsmanagement Allround"  # Voorbeeldwaarde

def extract_specializations(lines):
    # Zoek en split op woorden als 'keuzetrajecten' of 'afstudeerrichtingen'
    return ["Digital & AI Business Management", "Entrepreneurship"]  # Voorbeeldwaarden

def extract_section_text(lines, section_title):
    # Zoek sectietitel, retourneer de daaropvolgende tekstregel
    for i, line in enumerate(lines):
        if section_title in line:
            return lines[i + 1] if i + 1 < len(lines) else ""
    return ""

def extract_study_modes(lines):
    # Zoek en haal studievormen op zoals "Dagonderwijs", "Avondopleiding"
    modes = []
    for line in lines:
        if "Dagonderwijs" in line or "Avondopleiding" in line:
            modes.append(line.strip())
    return modes

# Inladen en opslaan als JSON
pdf_path = "/mnt/data/PXL Brochure 25-26.pdf"
study_directions = extract_study_directions(pdf_path)

with open("studierichtingen.json", "w") as json_file:
    json.dump(study_directions, json_file, ensure_ascii=False, indent=4)

print("Data succesvol opgeslagen in studierichtingen.json")
