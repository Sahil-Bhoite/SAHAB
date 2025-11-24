from transformers import AutoTokenizer, AutoModel
import torch

print("Loading Tokenizer...")
try:
    tokenizer = AutoTokenizer.from_pretrained("law-ai/InLegalBERT")
    print("Tokenizer loaded.")
except Exception as e:
    print(f"Error loading tokenizer: {e}")

print("Loading Model...")
try:
    model = AutoModel.from_pretrained("law-ai/InLegalBERT")
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
