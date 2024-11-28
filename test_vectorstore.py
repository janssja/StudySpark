# test_vectorstore.py
from app.vectorstore.query_engine import QueryEngine
from dotenv import load_dotenv
import os

def print_results(query: str, results, max_length: int = 300):
    """Print query results in a readable format"""
    print("\n" + "="*80)
    print(f"QUERY: {query}")
    print("="*80)
    
    if not results:
        print("\nGeen resultaten gevonden.")
        return
        
    for i, doc in enumerate(results, 1):
        print(f"\nRESULT {i}:")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        
        # Print truncated content with ellipsis if too long
        content = doc.page_content.strip()
        if len(content) > max_length:
            content = content[:max_length] + "..."
        print(f"Content: {content}\n")
        print("-"*40)

def test_vectorstore():
    print("Initializing query engine...")
    engine = QueryEngine()
    
    # Test queries
    test_queries = [
        "Wat houdt de opleiding Toegepaste Informatica in?",
        "Welke vakken krijg je bij Bedrijfsmanagement?",
        "Ik ben geïnteresseerd in programmeren en technologie",
        "Ik wil graag met mensen werken en in de zorgsector",
        "Wat zijn de toekomstmogelijkheden bij Communicatie?",
        "Welke voorkennis is nodig voor Elektronica-ICT?",
    ]
    
    print(f"\nGoing to test {len(test_queries)} queries...")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nProcessing query {i}/{len(test_queries)}")
        results = engine.query_catalog(query, k=2)  # Get top 2 results per query
        print_results(query, results)
        
        if i < len(test_queries):
            input("\nDruk op Enter voor de volgende query...")

def main():
    # Load environment variables
    load_dotenv()
    
    print("Starting vectorstore test...")
    print("We gaan verschillende queries testen om de kwaliteit van de resultaten te evalueren.")
    
    try:
        test_vectorstore()
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"\nError during testing: {str(e)}")
        print("\nControleer of:")
        print("1. De vectorstore correct is aangemaakt (run setup_vectorstore.py eerst)")
        print("2. Je .env file een geldige OPENAI_API_KEY bevat")
        print("3. De PDF bestanden correct zijn verwerkt")
        print("\nStack trace voor debugging:")
        raise

if __name__ == "__main__":
    main()