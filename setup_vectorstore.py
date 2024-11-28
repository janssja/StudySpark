# setup_vectorstore.py
import os
from app.vectorstore.pdf_processor import CatalogProcessor
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()

    # Create necessary directories
    os.makedirs("app/vectorstore", exist_ok=True)
    os.makedirs("catalogs", exist_ok=True)
    
    print("Starting vectorstore setup...")
    
    try:
        processor = CatalogProcessor()
        processor.create_vectorstore()
        print("Setup complete! Vectorstore created successfully.")
    except FileNotFoundError:
        print("\nError: No PDF files found!")
        print("Please add your PDF files to the 'catalogs' directory.")
    except Exception as e:
        print(f"\nError during setup: {str(e)}")
        print("\nPlease ensure:")
        print("1. You have PDF files in the 'catalogs' directory")
        print("2. Your .env file contains a valid OPENAI_API_KEY")
        print("3. All required packages are installed")

if __name__ == "__main__":
    main()