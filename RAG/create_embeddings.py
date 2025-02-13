import os
import json
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = os.getenv("PINECONE_INDEX")

pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index_name)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=openai_api_key)

def load_json_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

exoplanet_data = load_json_data("Data/exoplanet_discoveries.json")
phenomena_data = load_json_data("Data/cosmic_phenomena.json")
missions_data = load_json_data("Data/space_missions.json")

all_data = exoplanet_data + phenomena_data + missions_data


# Convert data to LangChain documents
documents = []
for entry in all_data:
    formatted_lines = []
    for key, value in entry.items():
        if value:
            formatted_key = key.replace('_', ' ').capitalize()
            formatted_lines.append(f"{formatted_key}: {value}")

    formatted_content = "\n".join(formatted_lines)
    
    doc = Document(
        page_content=formatted_content,
        metadata=entry
    )
    documents.append(doc)

# Generate embeddings and upload to Pinecone
for idx, doc in enumerate(documents):
    vector = embeddings.embed_query(doc.page_content)
    index.upsert(vectors=[{
        "id": doc.metadata.get("name", doc.metadata.get("mission_name", f"doc_{idx}")),  
        "values": vector,
        "metadata": doc.metadata
    }])

print("Embeddings successfully stored in Pinecone!")
