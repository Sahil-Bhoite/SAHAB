from langchain_community.embeddings import HuggingFaceEmbeddings
print("Loading Embeddings model...")
try:
    embeddings = HuggingFaceEmbeddings(model_name="law-ai/InLegalBERT")
    print("Embeddings model loaded successfully.")
except Exception as e:
    print(f"Error loading embeddings: {e}")
