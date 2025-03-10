# RAG-Based AI Chatbot Model

## 🚀 Overview
This project implements a **Retrieval-Augmented Generation (RAG) based AI Chatbot** using **OpenAI's GPT-3.5**, **FAISS**, and **SQLite**. It provides intelligent responses by retrieving relevant context from a pre-defined knowledge base and generating responses accordingly.

## 🏗️ Features
- **Retrieval-Augmented Generation (RAG)**: Enhances response quality by fetching relevant text chunks.
- **FAISS Indexing**: Fast similarity search for efficient document retrieval.
- **Streamlit UI**: Interactive web-based chatbot interface.
- **SQLite Database**: Stores user conversations for reference.
- **OpenAI GPT-3.5 API**: Generates responses based on retrieved context.

## 📂 Project Structure
```
├── backend.py         
├── frontend.py        
├── data
│   ├── context.txt    
├── chat_history.db    
├── requirements.txt  
├── README.md         
```

## 🛠️ Setup & Installation
### 1️⃣ Clone the repository
```sh
git clone https://github.com/yourusername/RAG-AI-Chatbot.git
cd RAG-AI-Chatbot
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up OpenAI API Credentials
Modify `backend.py` and replace the placeholders with your **Azure OpenAI API Key**:
```python
openai.api_type = "azure"
openai.api_key = "YOUR_API_KEY"
openai.api_base = "YOUR_API_BASE_URL"
openai.api_version = "2023-09-15-preview"
```

### 5️⃣ Run the Chatbot
```sh
streamlit run frontend.py
```
This will launch the chatbot in your browser.

## 🔥 Usage
1. Click **New User** to start a fresh conversation.
2. Enter your question in the chat input.
3. The chatbot retrieves relevant information and generates a response.
4. Previous conversations are saved and displayed in the sidebar.

## 📜 License
This project is licensed under the MIT License. Feel free to use and modify it.

## 🙌 Acknowledgments
- **OpenAI** for GPT-3.5 API
- **Facebook AI** for FAISS
- **Streamlit** for UI development

💡 Happy Coding! 🚀

