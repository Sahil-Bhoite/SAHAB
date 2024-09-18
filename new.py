import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_together import Together
from langchain_community.chat_models import ChatOllama
from config import TOGETHER_API_KEY  # Import API key from config.py
from deep_translator import GoogleTranslator
from langchain.text_splitter import RecursiveCharacterTextSplitter

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

# Set environment variables
os.environ['TOGETHER_API_KEY'] = TOGETHER_API_KEY

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
eFiling in India allows users to file cases and documents electronically, saving time and resources. Here are some general guidelines:
1. Register for an account on the eCourts website (https://services.ecourts.gov.in/ecourtindia_v6/) and complete the verification process.
2. Once registered, log in to access the eFiling services.
3. Choose the appropriate court and case type, then fill out the required forms and upload supporting documents.
4. Pay the necessary court fees through the ePay system integrated within the eCourts platform.
5. After submission, track the case status using the eCourts Case Information System (CIS).

ePay is an integrated payment gateway within the eCourts platform, allowing users to pay court fees, fines, and other charges electronically. Here are some general guidelines:
1. Ensure you have a valid payment method, such as a debit card, credit card, or net banking account.
2. Once you've filled out the required forms and uploaded supporting documents for eFiling, proceed to the payment section.
3. Choose your preferred payment method and follow the prompts to complete the transaction.
4. After successful payment, you will receive a confirmation receipt, which should be saved for future reference.

For more detailed information on eFiling and ePay, visit https://doj.gov.in/efiling/

The Department of Justice (DoJ) provides comprehensive information on its official website (https://doj.gov.in/). Here, you can find details about various services, schemes, initiatives, and legal resources.

Some important resources include:
- National Legal Services Authority (NALSA): https://nalsa.gov.in/
- eCourts(Know Your Case Status) : https://services.ecourts.gov.in/ecourtindia_v6/
- Legal Aid Clinics: https://nalsa.gov.in/services/legal-aid-clinics
- Legal Services to Women and Children: https://nalsa.gov.in/services/legal-services-women-and-children
- Alternative Dispute Resolution (ADR): https://doj.gov.in/page/alternative-dispute-resolution
- Legal Education: https://doj.gov.in/page/legal-education
- Access to Justice: https://doj.gov.in/page/access-justice
- Information about various divisions of DoJ - https://judgments.ecourts.gov.in/pdfsearch/index.php
- Virtual Justice Clock(Case pendency information): https://justiceclock.ecourts.gov.in/justiceClock/

Live streaming of court proceedings is available for several courts:
- Supreme Court of India: https://www.sci.gov.in
- Gujarat High Court: https://gujarathighcourt.nic.in/streamingboard/
- Gauhati High Court: https://ghconline.gov.in/index.php/live-streaming-of-court-proceedings-1/
- Jharkhand High Court: https://www.youtube.com/channel/UC43OwYFDEuS8OrK_PSIabSg/videos?view=57
- Karnataka High Court: https://www.youtube.com/c/HighCourtofKarnatakaOfficial
- Madhya Pradesh High Court: https://www.youtube.com/channel/UCCIVFftzmBqzBKoijOmIl1A
- Orissa High Court: https://www.youtube.com/channel/UCtTgN30THhZfQ6sQ_v3KBHQ
- Patna High Court: https://www.youtube.com/channel/UCvb5s5UdLjpaiDpBeaCxVEw
"""

text_chunks = get_text_chunks(text_data)
vector_store = get_vector_store(text_chunks)
db_retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Define the prompt template
prompt_template = """
<s>[INST]
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
CHAT HISTORY: {chat_history}
QUESTION: {question}
ANSWER:
- [Provide a response based on the criteria above]
</s>[INST]
"""

prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question', 'chat_history'])

def get_conversational_chain_online(vector_store):
    api_key = os.getenv('TOGETHER_API_KEY')
    llm = Together(model="mistralai/Mixtral-8x22B-Instruct-v0.1", temperature=0.5, max_tokens=1024, together_api_key=api_key)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, memory=st.session_state.memory, retriever=db_retriever, combine_docs_chain_kwargs={'prompt': prompt})
    return conversation_chain

def get_conversational_chain_offline(vector_store):
    llm = ChatOllama(model="phi3")
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, memory=st.session_state.memory, retriever=db_retriever, combine_docs_chain_kwargs={'prompt': prompt})
    return conversation_chain

# Initialize the conversation chain based on the selected mode
if model_mode:
    qa = get_conversational_chain_online(vector_store)
else:
    qa = get_conversational_chain_offline(vector_store)

def extract_answer(full_response):
    """Extracts the answer from the LLM's full response."""
    answer_start = full_response.find("ANSWER:")
    if answer_start != -1:
        answer_start += len("ANSWER:")
        answer = full_response[answer_start:].strip()
        return answer
    return full_response

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
            result = qa.invoke(input=input_prompt, context=trimmed_history)
            message_placeholder = st.empty()
            answer = extract_answer(result["answer"])

            # Translate the answer to the selected language
            if selected_language == "English":
                translated_answer = answer
            else:
                translated_answer = translate_answer(answer, selected_language.lower())

            # Initialize the response message
            full_response = "⚠️ **_Gentle reminder: We generally ensure precise information, but do double-check._** \n\n\n"
            full_response += translated_answer
            message_placeholder.markdown(full_response + "  ", unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": translated_answer})

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
