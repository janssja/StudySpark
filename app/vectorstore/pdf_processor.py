# app/vectorstore/pdf_processor.py
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings  # Updated import
from langchain_community.vectorstores import FAISS
import os
from typing import List, Dict
from config import Config

class CatalogProcessor:
    def __init__(self, pdf_directory="catalogs"):
        self.pdf_directory = pdf_directory
        self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf = PdfReader(file)
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error processing {pdf_path}: {str(e)}")
            return ""

    def process_pdfs(self) -> List[Dict[str, str]]:
        """Process all PDFs in directory and return list of documents"""
        documents = []
        if not os.path.exists(self.pdf_directory):
            raise FileNotFoundError(f"Directory {self.pdf_directory} not found!")

        for filename in os.listdir(self.pdf_directory):
            if filename.endswith('.pdf'):
                file_path = os.path.join(self.pdf_directory, filename)
                text = self.extract_text_from_pdf(file_path)
                if text:
                    documents.append({
                        "content": text,
                        "source": filename,
                        "type": "program_description"
                    })
        return documents

    def create_vectorstore(self):
        """Create FAISS vectorstore from PDF content"""
        try:
            # Process PDFs and get documents
            documents = self.process_pdfs()
            if not documents:
                raise ValueError("No documents were processed successfully")

            # Split documents into chunks
            texts = []
            metadatas = []
            for doc in documents:
                chunks = self.text_splitter.split_text(doc["content"])
                texts.extend(chunks)
                metadatas.extend([{
                    "source": doc["source"],
                    "type": doc["type"]
                }] * len(chunks))

            # Create vectorstore
            print(f"Creating vectorstore with {len(texts)} text chunks...")
            vectorstore = FAISS.from_texts(
                texts=texts,
                embedding=self.embeddings,
                metadatas=metadatas
            )

            # Save vectorstore
            save_path = "app/vectorstore/faiss_index"
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            vectorstore.save_local(save_path)
            print(f"Vectorstore saved to {save_path}")

            return vectorstore

        except Exception as e:
            print(f"Error creating vectorstore: {str(e)}")
            raise