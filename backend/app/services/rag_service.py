import os
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.core.config import settings
from transformers import AutoTokenizer, AutoModel
import torch
from typing import List

class CustomHuggingFaceEmbeddings(Embeddings):
    def __init__(self, model_name="law-ai/InLegalBERT"):
        print(f"Loading custom embeddings model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        print("Custom embeddings model loaded.")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Mean pooling
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings[0].tolist()

# Configure Google Generative AI
genai.configure(api_key=settings.GOOGLE_API_KEY)

class RAGService:
    def __init__(self):
        self.vector_store = None
        self.retriever = None
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        self._initialize_vector_store()

    def _initialize_vector_store(self):
        print("Initializing Vector Store...")
        try:
            index_path = os.path.join(os.path.dirname(__file__), "../../data/faiss_index")
            file_path = os.path.join(os.path.dirname(__file__), "../../data/ipc_law.txt")
            
            print("Loading Embeddings model...")
            embeddings = CustomHuggingFaceEmbeddings(model_name="law-ai/InLegalBERT")
            print("Embeddings model loaded.")

            if os.path.exists(index_path):
                print("Loading existing FAISS index from disk...")
                self.vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
                print("FAISS index loaded successfully.")
            else:
                print("Creating new FAISS index...")
                if not os.path.exists(file_path):
                    print(f"Warning: Data file not found at {file_path}")
                    return

                with open(file_path, "r", encoding="utf-8") as f:
                    text_data = f.read()
                print("File read successfully.")

                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                chunks = text_splitter.split_text(text_data)
                print(f"Text split into {len(chunks)} chunks.")
                
                self.vector_store = FAISS.from_texts(chunks, embedding=embeddings)
                self.vector_store.save_local(index_path)
                print("FAISS index created and saved to disk.")

            self.retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
            print("Vector Store Initialized Successfully.")
        except Exception as e:
            print(f"Error initializing vector store: {e}")

    def get_response_stream(self, prompt: str):
        if not self.retriever:
            yield "System is initializing, please try again in a moment."
            return

        # Retrieve context
        try:
            context_docs = self.retriever.get_relevant_documents(prompt)
            context_text = "\n".join([doc.page_content for doc in context_docs])
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            context_text = ""

        full_prompt = f"""
        You are SAHAB, an authoritative legal assistant . 
        Your primary source of information is the provided legal context.
        
        Guidelines:
        1. Respond professionally and confidently.
        2. Cite specific section numbers from the CONTEXT when available.
        3. Do not use emojis.
        4. IF the answer is found in the CONTEXT, rely strictly on it.
        5. IF the answer is NOT in the CONTEXT (e.g., questions about CrPC, Evidence Act, or general definitions not in IPC):
           - Provide a brief, general legal definition based on your general knowledge.
           - Do NOT mention that the information is missing from your database.
           - Suggest consulting the relevant act (e.g., CrPC for bail).

        CONTEXT: {context_text}
        QUESTION: {prompt}
        ANSWER:
        """
        
        try:
            response = self.model.generate_content(full_prompt, stream=True)
            for chunk in response:
                yield chunk.text
        except Exception as e:
            yield f"Error generating response: {e}"

rag_service = RAGService()
