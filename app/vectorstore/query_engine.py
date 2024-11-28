# app/vectorstore/query_engine.py
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from config import Config

class QueryEngine:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        try:
            self.vectorstore = FAISS.load_local(
                "app/vectorstore/faiss_index", 
                self.embeddings,
                allow_dangerous_deserialization=True  # Added this parameter
            )
            print("Vectorstore loaded successfully!")
        except Exception as e:
            print(f"Error loading vectorstore: {str(e)}")
            self.vectorstore = None

    def query_catalog(self, query: str, k: int = 3):
        """Query the vectorstore for relevant program information"""
        if not self.vectorstore:
            print("Warning: Vectorstore not available")
            return []
            
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"Error querying vectorstore: {str(e)}")
            return []