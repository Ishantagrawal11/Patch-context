import streamlit as st
from rag import ask_question

st.set_page_config(
    page_title="PatchContext",
    page_icon="📚",
    layout="wide"
)

st.title("📚 PatchContext")
st.caption("GitHub Repository AI Assistant")

question = st.text_input(
    "Ask your question"
)

if st.button("Ask"):

    if question:

        with st.spinner("Thinking..."):

            answer, sources = ask_question(question)

        st.subheader("🤖 AI Answer")

        st.write(answer)

        st.subheader("📌 Sources")

        if len(sources)==0:

            st.info("No sources")

        else:

            for s in sources:

                st.write("•", s)