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

# Set the Streamlit page configuration and theme
st.set_page_config(page_title="SAHAB", layout="wide")
st.header("SMART AUTOMATED HIERARCHICAL ANALYSIS BOT")
with st.sidebar:
    st.title("S.A.H.A.B")
    # Display the logo image
    col1, col2, col3 = st.columns([1, 30, 1])
    with col2:
        st.image("images/Judge.png", use_column_width=True)

    # Add toggle for online/offline mode
    model_mode = st.toggle("Online Mode", value=True)

# Set environment variables
os.environ['TOGETHER_API_KEY'] = TOGETHER_API_KEY

def hide_hamburger_menu():
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

hide_hamburger_menu()

# Initialize session state for messages and memory
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(k=2, memory_key="chat_history", return_messages=True)

# Function to split text into chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter

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
text_data = "Your legal text data here"
text_chunks = get_text_chunks(text_data)
vector_store = get_vector_store(text_chunks)
db_retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Define the prompt template
prompt_template = """
<s>[INST]
As a legal chatbot specializing in the Indian Penal Code, you are tasked with providing highly accurate and contextually appropriate responses. Ensure your answers meet these criteria:
- Respond in a bullet-point format to clearly delineate distinct aspects of the legal query.
- Each point should accurately reflect the breadth of the legal provision in question, avoiding over-specificity unless directly relevant to the user's query.
- Clarify the general applicability of the legal rules or sections mentioned, highlighting any common misconceptions or frequently misunderstood aspects.
- Limit responses to essential information that directly addresses the user's question, providing concise yet comprehensive explanations.
- Avoid assuming specific contexts or details not provided in the query, focusing on delivering universally applicable legal interpretations unless otherwise specified.
- Conclude with a brief summary that captures the essence of the legal discussion and corrects any common misinterpretations related to the topic.

CONTEXT: {context}
CHAT HISTORY: {chat_history}
QUESTION: {question}
ANSWER:
- [Detail the first key aspect of the law, ensuring it reflects general application]
- [Provide a concise explanation of how the law is typically interpreted or applied]
- [Correct a common misconception or clarify a frequently misunderstood aspect]
- [Detail any exceptions to the general rule, if applicable]
- [Include any additional relevant information that directly relates to the user's query]
</s>[INST]
"""

prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question', 'chat_history'])

def get_conversational_chain_online(vector_store): # For online LLM
    api_key = os.getenv('TOGETHER_API_KEY')
    llm = Together(model="mistralai/Mixtral-8x22B-Instruct-v0.1", temperature=0.5, max_tokens=1024, together_api_key=api_key)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, memory=st.session_state.memory, retriever=db_retriever, combine_docs_chain_kwargs={'prompt': prompt})
    return conversation_chain

def get_conversational_chain_offline(vector_store): # For offline LLM
    llm = ChatOllama(model="phi3")  # Initialize the ChatOllama instance with the phi3 model
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, memory=st.session_state.memory, retriever=db_retriever, combine_docs_chain_kwargs={'prompt': prompt})
    return conversation_chain

# Initialize the conversation chain based on the selected mode
if model_mode:
    qa = get_conversational_chain_online(vector_store)
else:
    qa = get_conversational_chain_offline(vector_store)

def extract_answer(full_response):
    """Extracts the answer from the LLM's full response by removing the instructional text."""
    answer_start = full_response.find("ANSWER:")
    if answer_start != -1:
        answer_start += len("ANSWER:")
        return full_response[answer_start:].strip()
    return full_response

def reset_conversation():
    st.session_state.messages = []
    st.session_state.memory.clear()

def get_trimmed_chat_history():
    # Only keep a certain number of recent messages to avoid repetition
    max_history = 10  # Adjust as needed
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
    trimmed_history = get_trimmed_chat_history()  # Use trimmed history

    with st.chat_message("assistant"):
        with st.spinner("Thinking 💡..."):
            result = qa.invoke(input=input_prompt, context=trimmed_history)
            message_placeholder = st.empty()
            answer = extract_answer(result["answer"])

            # Initialize the response message
            full_response = "⚠️ **_Gentle reminder: We generally ensure precise information, but do double-check._** \n\n\n"
            full_response += answer  # Append the model's answer
            message_placeholder.markdown(full_response + "  ", unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": answer})

        if st.button('🗑️ Reset', on_click=reset_conversation):
            st.experimental_rerun()

# Footer.py content
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