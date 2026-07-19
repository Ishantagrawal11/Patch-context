from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS vector store
db = FAISS.load_local(
    "vectorstore",
    embedding_model,
    allow_dangerous_deserialization=True
)

# Create retriever
retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 20
    }
)

query = input("Ask a question: ")

docs = retriever.invoke(query)

print("\nTop Retrieved Documents:\n")

for i, doc in enumerate(docs, start=1):
    print("=" * 60)
    print(f"Document {i}")
    print(doc.page_content)
    print(doc.metadata)