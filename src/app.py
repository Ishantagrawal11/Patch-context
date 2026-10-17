import streamlit as st
from rag import ask_question

st.set_page_config(
    page_title="PatchContext",
    page_icon="📚",
    layout="wide",
)

st.title("📚 PatchContext")
st.caption("GitHub Repository AI Assistant")

question = st.text_input("Ask your question")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                answer, sources = ask_question(question.strip())
            except Exception as exc:
                st.error(f"Something went wrong: {exc}")
            else:
                st.subheader("🤖 AI Answer")
                st.write(answer)

                st.subheader("📌 Sources")
                if not sources:
                    st.info("No sources found.")
                else:
                    for source in sources:
                        st.markdown(f"- [Open source]({source})")
