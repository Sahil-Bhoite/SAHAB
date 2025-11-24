# SAHAB - Smart Assistant for Handling Advocacy and Briefings

SAHAB is an AI-driven legal chatbot designed to provide accessible legal information based on the Indian Penal Code (IPC) and Department of Justice (DoJ) services. It leverages RAG (Retrieval-Augmented Generation) to provide grounded answers.

## Tech Stack

*   **Frontend:** React, TypeScript, Vite, Tailwind CSS, Framer Motion, Three.js (@react-three/fiber)
*   **Backend:** Python, FastAPI
*   **AI Model:** Google Gemini 2.5 Pro
*   **Embeddings:** law-ai/InLegalBERT (Custom implementation using Transformers)
*   **Vector Database:** FAISS (Locally persisted)
*   **Translation:** Deep Translator

## Features

*   **Intelligent Legal Q&A:** Ask questions about IPC sections, offenses, and penalties.
*   **RAG-Powered:** Retrieves relevant context from the IPC to ensure accuracy.
*   **Confident & Transparent:** Provides direct answers or clearly states if information is outside the IPC scope (e.g., CrPC), advising professional consultation.
*   **Multilingual Support:** Supports 12 Indian languages including Hindi, Tamil, Telugu, Bengali, and more.
*   **Streaming Responses:** Real-time streaming of AI responses for a better user experience.
*   **Persistent Index:** FAISS index is saved to disk for faster subsequent startups.
*   **Modern UI:** Responsive design with a 3D interactive hero element and chat interface.

## Setup and Installation

### Prerequisites
*   Python 3.10+
*   Node.js 18+
*   A Google Gemini API Key

### Backend Setup
1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Configure Environment:
    Create a `.env` file in the `backend` directory:
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```
4.  Run the server:
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    *Note: The first run may take several minutes to download the `InLegalBERT` model and build the FAISS index. Subsequent runs will be faster.*

### Frontend Setup
1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```
    The application will be accessible at `http://localhost:5173`.

## Usage Limits
The current demo version allows up to 2 free queries per session. For extended access, please contact the owner.

## Disclaimer
SAHAB provides general information, not legal advice. Please refer to official legal documents for verified information.
