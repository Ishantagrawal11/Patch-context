from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Load embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS vector store
# Run the app from the project root:
#     streamlit run src/app.py
# so that this relative path resolves correctly.
db = FAISS.load_local(
    "vectorstore",
    embedding_model,
    allow_dangerous_deserialization=True,
)


BASE_SEARCH_KWARGS = {
    "k": 5,
    "fetch_k": 20,
}


def detect_document_type(query: str):
    """Detect whether the user is asking about commits, issues, or PRs."""
    q = query.lower().strip()

    # Check pull requests before the generic "request" wording.
    if any(term in q for term in (
        "pull request",
        "pull requests",
        "pull-request",
        "pull-requests",
        "pr #",
        "prs",
        "prs",
    )):
        return "pull_request"

    if any(term in q for term in (
        "issue",
        "issues",
        "bug",
        "bugs",
        "problem",
    )):
        return "issue"

    if any(term in q for term in (
        "commit",
        "commits",
        "commit history",
        "recent changes",
        "latest changes",
        "changes in the repository",
        "what changed",
    )):
        return "commit"

    return None


def retrieve(query: str):
    """Retrieve relevant repository documents, optionally filtered by type."""
    document_type = detect_document_type(query)

    search_kwargs = dict(BASE_SEARCH_KWARGS)
    if document_type:
        search_kwargs["filter"] = {"type": document_type}

    query_retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs=search_kwargs,
    )

    return query_retriever.invoke(query)


# Backward-compatible object used by rag.py and other code.
class QueryAwareRetriever:
    def invoke(self, query: str):
        return retrieve(query)


retriever = QueryAwareRetriever()
