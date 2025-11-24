import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key found: {api_key[:5]}..." if api_key else "API Key NOT found")

if api_key:
    genai.configure(api_key=api_key)
    print("Listing available models:")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
        
        # Try a likely available model if gemini-1.5-pro failed, e.g., gemini-pro
        model_name = 'gemini-1.5-flash' 
        print(f"\nTrying model: {model_name}")
        model = genai.GenerativeModel(model_name)
        try:
            response = model.generate_content("Hello, can you hear me?")
            print("Response received:")
            print(response.text)
        except Exception as e:
            print(f"Error generating content with {model_name}: {e}")

            # Fallback check
            model_name = 'gemini-pro'
            print(f"\nTrying fallback model: {model_name}")
            model = genai.GenerativeModel(model_name)
            try:
                response = model.generate_content("Hello, can you hear me?")
                print("Response received:")
                print(response.text)
            except Exception as e:
                print(f"Error generating content with {model_name}: {e}")

    except Exception as e:
        print(f"Error listing models: {e}")
