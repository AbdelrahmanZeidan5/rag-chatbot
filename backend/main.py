from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = os.getenv("PINECONE_INDEX")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


llm = ChatOpenAI(model_name="gpt-4o", openai_api_key=openai_api_key)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=openai_api_key)

pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index_name)


qa_prompt = ChatPromptTemplate.from_template(
    """
    You are a knowledgeable assistant specializing in space exploration, astronomy, and cosmic discoveries.
    Your role is to provide accurate and well-structured answers based on the retrieved context.

    Guidelines for Your Responses:
    1. If the user greets you (e.g., "Hi", "Hello", "Hey"), respond politely without mentioning space-related topics.
    2. If the user asks about space missions, exoplanets, or cosmic phenomena, generate a response based only on the retrieved context ONLY.
    3. If the retrieved context does not provide relevant information, respond with: "I don't have enough data to answer. "
    4. Do NOT generate or assume information that is not present in the provided context.

    User Query:
    {query}

    Retrieved Context:
    {context}

    Provide a clear and structured response based only on the retrieved context.
    """
)


question_answer_chain = create_stuff_documents_chain(llm, qa_prompt, document_variable_name="context")


class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
def chat(request: ChatRequest):
    """Handles user queries using Pinecone retrieval and OpenAI response generation"""
    try:
        user_query = request.query.strip().lower()

        greetings = ["hi", "hello", "hey", "good morning", "good evening", "how are you"]
        if user_query in greetings:
            return {
                "query": request.query,
                "response": "Hello! How can I assist you today?",
                "context": "No retrieval needed."
            }

        query_embedding = embeddings.embed_query(request.query)

        retrieval_results = index.query(
            vector=query_embedding,
            top_k=3,
            include_metadata=True
        )

        retrieval_results_dict = retrieval_results.to_dict()

        if not retrieval_results_dict.get("matches"):
            return {
                "query": request.query,
                "response": "I don't have enough data to answer.",
                "context": "No relevant documents found."
            }

        retrieved_docs = []
        for match in retrieval_results_dict["matches"]:
            metadata = match["metadata"]

            formatted_metadata = "\n".join([f"{key.capitalize()}: {value}" for key, value in metadata.items() if value])

            doc = Document(
                page_content=formatted_metadata,
                metadata=metadata
            )
            retrieved_docs.append(doc)


        input_payload = {"query": request.query, "context": retrieved_docs}

        response = question_answer_chain.invoke(input_payload)

        return {
            "query": request.query,
            "response": response if isinstance(response, str) else response.get("output_text", "No valid response."),
            "context": [
                {key: value for key, value in doc.metadata.items() if value}
                for doc in retrieved_docs
            ]

        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
