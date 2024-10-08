# SAHAB - Smart Assistant for Handling Advocacy and Briefings

SAHAB is an AI-driven RAG-based multi-modal chatbot designed to enhance user interaction on the Department of Justice (DoJ) website. It provides accurate, context-aware information on legal matters, court procedures, and DoJ services, utilizing advanced algorithms and Language Models (LLMs) to efficiently process and retrieve relevant data.


https://github.com/user-attachments/assets/299a69c2-8634-497b-891f-55e9d50deac1



## Problem Statement

Developing an AI-based interactive Chatbot or virtual assistant for the Department of Justice's Website.
- **Problem Statement ID**: 1700
- **Theme**: Smart Automation
- **PS Category**: Software

## Features

- **Multilingual Support**: Communicate in various Indian languages including English, Hindi, Bengali, and more.
- **AI-Powered Responses**: Utilizes advanced language models to provide accurate legal information.
- **User-Friendly Interface**: Clean and intuitive Streamlit-based UI for easy interaction.
- **Offline Mode**: Option to switch between online and offline modes for flexibility.
- **Conversation Memory**: Maintains context through conversation history.
- **Legal Text Analysis**: Processes and retrieves information from legal documents.
- **Adaptive Learning**: Continuously updates and expands its knowledge base.
- **Personalized Experience**: Tailors responses based on each user's interaction history.

## How It Addresses the Problem

- Simplifies access to critical information by allowing users to navigate complex legal topics effortlessly.
- Streamlines the process of finding essential legal details, improving the accessibility of information for citizens.
- Reduces dependency on manual searches and costly legal advice by offering initial, reliable guidance.

## Architecture and Data Flow

[Include an image or description of the project's architecture here]

## Technologies Used

- **Programming Language**: Python
- **Frameworks**: Streamlit, LangChain
- **Libraries**: FAISS, GoogleTranslator, HuggingFace Embeddings, Together, Ollama
- **Embeddings**: law-ai/InLegalBERT

## Demo

Try SAHAB live: [SAHAB Demo](https://sahab-demo.streamlit.app)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Sahil-Bhoite/SAHAB.git
   cd SAHAB
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your API keys in `config.py`.

## Usage

Run the Streamlit app:

```
streamlit run new.py
```

Navigate to the provided local URL in your web browser to interact with SAHAB.

## Challenges and Solutions

### Challenge: Accuracy of LLM Responses
Legal queries require precise and context-aware answers. Incorrect or vague responses could lead to misinformation.

### Solution: Predefined System Prompts
- Use specific prompt instructions to ensure clear and correct answers.
- Implement a prompt design that:
  - Breaks down answers into clear points.
  - Corrects common mistakes and explains exceptions.
  - Focuses on the most relevant information.

## Impact and Benefits

### Social Benefits
- Encourages legal education and awareness, leading to a more legally informed society.

### Economic Benefits
- Reduces dependency on costly legal advice by offering initial, reliable guidance and information.

### Operational Benefits
- Eases the burden on government helpdesks by streamlining access to essential legal resources and information.

### Environmental Benefits
- Minimizes the need for physical documents by providing a digital, eco-friendly alternative for accessing legal materials.

## Future Enhancements

[Add any planned future enhancements or features here]

## Contributing

Contributions to SAHAB are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Sahil-Bhoite/SAHAB/blob/main/LICENSE) file for details.

## Contact

Sahil Bhoite - [LinkedIn](https://www.linkedin.com/in/sahil-bhoite/)

Project Link: [https://github.com/Sahil-Bhoite/SAHAB](https://github.com/Sahil-Bhoite/SAHAB)

## Acknowledgements

- Thanks to the Langchain community for their excellent tools and documentation.
- Gratitude to the open-source community for various libraries used in this project.

## References

- G, Shubhashri & N, Unnamalai & G, Kamalika. (2018). LAWBO: a smart lawyer chatbot. 348-351. 10.1145/3152494.3167988. [Link](https://www.researchgate.net/publication/324464758_LAWBO_a_smart_lawyer_chatbot)
- Queudot, Marc & Charton, Éric & Meurs, Marie-Jean. (2020). Improving Access to Justice with Legal Chatbots. Stats. 3. 356-375. 10.3390/stats3030023. [Link](https://www.mdpi.com/2571-905X/3/3/23)

