import os
import time
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_models import ChatOllama
from deep_translator import GoogleTranslator
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai

# Set the Streamlit page configuration and theme
st.set_page_config(page_title="SAHAB", layout="wide")
st.header("SMART AUTOMATED HIERARCHICAL ANALYSIS BOT")

# Sidebar configuration
with st.sidebar:
    st.title("S.A.H.A.B")
    col1, col2, col3 = st.columns([1, 30, 1])
    with col2:
        st.image("images/Judge.png", use_column_width=True)
    model_mode = st.toggle("Online Mode", value=True)
    selected_language = st.selectbox("Start by Selecting your Language", 
                                     ["English", "Assamese", "Bengali", "Gujarati", "Hindi", "Kannada", "Malayalam", "Marathi", 
                                      "Nepali", "Odia", "Punjabi", "Sindhi", "Tamil", "Telugu", "Urdu"])

# Configure Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# Hide Streamlit's default menu
def hide_hamburger_menu():
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

hide_hamburger_menu()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(k=2, memory_key="chat_history", return_messages=True)

# Function to split text into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create a vector store
def get_vector_store(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="law-ai/InLegalBERT")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store

# Load and process your text data (Replace this with your actual legal text data)
text_data = """
[Your legal text data here]
"""

text_chunks = get_text_chunks(text_data)
vector_store = get_vector_store(text_chunks)
db_retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

def get_response_online(prompt, context):
    full_prompt = f"""
    As a legal chatbot specializing in the Indian Penal Code and Department of Justice services, you are tasked with providing highly accurate and contextually appropriate responses. Ensure your answers meet these criteria:
    - Respond in a bullet-point format to clearly delineate distinct aspects of the legal query or service information.
    - Each point should accurately reflect the breadth of the legal provision or service in question, avoiding over-specificity unless directly relevant to the user's query.
    - Clarify the general applicability of the legal rules, sections, or services mentioned, highlighting any common misconceptions or frequently misunderstood aspects.
    - Limit responses to essential information that directly addresses the user's question, providing concise yet comprehensive explanations.
    - When asked about live streaming of court cases, provide the relevant links for court live streams.
    - For queries about various DoJ services or information, provide accurate links and guidance.
    - Avoid assuming specific contexts or details not provided in the query, focusing on delivering universally applicable legal interpretations or service information unless otherwise specified.
    - Conclude with a brief summary that captures the essence of the legal discussion or service information and corrects any common misinterpretations related to the topic.

    CONTEXT: {context}
    QUESTION: {prompt}
    ANSWER:
    """
    response = model.generate_content(full_prompt, stream=True)
    return response

def get_response_offline(prompt, context):
    llm = ChatOllama(model="phi3")
    # Implement offline response generation here
    # This is a placeholder and needs to be implemented based on your offline requirements
    return "Offline mode is not fully implemented yet."

def translate_answer(answer, target_language):
    translator = GoogleTranslator(source='auto', target=target_language)
    translated_answer = translator.translate(answer)
    return translated_answer

def reset_conversation():
    st.session_state.messages = []
    st.session_state.memory.clear()

def get_trimmed_chat_history():
    max_history = 10
    return st.session_state.messages[-max_history:]

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle user input
input_prompt = st.chat_input("Start with your legal query")
if input_prompt:
    with st.chat_message("user"):
        st.markdown(f"{input_prompt}")

    st.session_state.messages.append({"role": "user", "content": input_prompt})
    trimmed_history = get_trimmed_chat_history()

    with st.chat_message("assistant"):
        with st.spinner("Thinking 💡..."):
            context = db_retriever.get_relevant_documents(input_prompt)
            context_text = "\n".join([doc.page_content for doc in context])
            
            if model_mode:
                response = get_response_online(input_prompt, context_text)
            else:
                response = get_response_offline(input_prompt, context_text)

            message_placeholder = st.empty()
            full_response = "⚠️ **_Gentle reminder: We generally ensure precise information, but do double-check._** \n\n\n"
            
            if model_mode:
                for chunk in response:
                    full_response += chunk.text
                    time.sleep(0.02)  # Adjust the sleep time to control the "typing" speed
                    message_placeholder.markdown(full_response + "  ", unsafe_allow_html=True)
            else:
                full_response += response
                message_placeholder.markdown(full_response, unsafe_allow_html=True)

            # Translate the answer to the selected language
            if selected_language != "English":
                translated_answer = translate_answer(full_response, selected_language.lower())
                message_placeholder.markdown(translated_answer, unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

        if st.button('🗑️ Reset', on_click=reset_conversation):
            st.experimental_rerun()

# Footer
def footer():
    st.markdown("""
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f1f1f1;
            color: black;
            text-align: center;
        }
        </style>
        <div class="footer">
        </div>
        """, unsafe_allow_html=True)

# Display the footer
footer()
