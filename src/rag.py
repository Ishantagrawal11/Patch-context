from langchain_ollama import ChatOllama
from retriever import retriever

# Local Ollama model
llm = ChatOllama(model="llama3.2")


def ask_question(query):
    docs = retriever.invoke(query)

    if not docs:
        return "I don't know based on the repository.", []

    context_parts = []
    sources = []

    for doc in docs:
        context_parts.append(doc.page_content)
        source = doc.metadata.get("source")
        if source and source not in sources:
            sources.append(source)

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are PatchContext, an expert GitHub repository assistant.

Answer the user's question using ONLY the repository context below.
Do not invent facts, dates, IDs, or details.
If the answer is not supported by the context, say exactly:
"I don't know based on the repository."

Repository context:
{context}

User question:
{query}

Answer concisely and directly.
"""

    response = llm.invoke(prompt)
    return response.content, sources
