import json

from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load documents
with open("data/documents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = []

for item in data:
    documents.append(
        Document(
            page_content=item["text"],
            metadata=item["metadata"]
        )
    )

print(f"Loaded {len(documents)} documents")

# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create FAISS vector store
db = FAISS.from_documents(documents, embedding_model)

# Save locally
db.save_local("vectorstore")

print("✅ FAISS vector database created successfully!")