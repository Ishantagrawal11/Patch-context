from retriever import retriever
from langchain_ollama import ChatOllama

# Load Ollama Model
llm = ChatOllama(model="llama3.2")

def ask_question(query):

    docs = retriever.invoke(query)

    context = ""

    sources = []

    for doc in docs:

        context += doc.page_content + "\n\n"

        if "source" in doc.metadata:
            sources.append(doc.metadata["source"])

    prompt = f"""
You are an expert software engineer.

Use ONLY the context below to answer the user's question.

If the answer is not present, say:
"I don't know based on the repository."

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content, sources