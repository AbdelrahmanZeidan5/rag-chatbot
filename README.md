# RAG-Chatbot

A simple demo chatbot using **Python, JavaScript, React, FastAPI, LangChain, Pinecone, and Embeddings**.




## Installation

### **Backend (FastAPI, LangChain, Pinecone)**
   ```bash
   cd backend
   ```
   ```
   python -m venv venv
   source venv/bin/activate 
   ```

   ```
   pip install -r requirements.txt
   ```


   ```
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```


   Note: Provide your API keys in a .env file (inside backend/)

    OPENAI_API_KEY=your_openai_key
    PINECONE_API_KEY=your_pinecone_key
    PINECONE_INDEX=your_pinecone_index



### **Frontend (React, JavaScript)**
   ```bash
   cd frontend
   ```
   ```
   yarn install
   ```

   ```
   yarn start 
   ```



### **RAG (Embeddings & Retrieval)**

```bash
cd RAG
```
```
python create_embeddings.py
```