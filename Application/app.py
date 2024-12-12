import streamlit as st
from vector_database import query_index
from llm_integrations import get_response_from_llm

# Streamlit App Configuration
st.set_page_config(
    page_title="Fitness Assistant",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar for settings or common queries
st.sidebar.title("Explore Topics")
common_queries = ["Weight Loss", "Strength Training", "Yoga Benefits", "Cardio Exercises"]
selected_query = st.sidebar.selectbox("Quick Topics", ["-- Select --"] + common_queries)

# Main Title and Description
st.title("💪 AI-Powered Fitness Assistant")
st.markdown(
    """
    Welcome to your personalized fitness guide!  
    Ask any fitness-related questions or explore common topics to get tailored insights.
    """
)

# Input Section
st.header("📝 Ask Your Question")
query_text = st.text_input("Enter your question:", value=selected_query if selected_query != "-- Select --" else "")

# Number of Results
top_k = st.slider("Number of relevant contexts to retrieve:", min_value=1, max_value=10, value=5)

# Retrieve and Display Response
if st.button("Get Answer"):
    if query_text.strip():
        # Retrieve context from Elasticsearch
        with st.spinner("Retrieving relevant contexts..."):
            context_results = query_index(query_text, top_k=top_k)

        if context_results:
            st.subheader("📄 Relevant Contexts")
            context_text = "\n".join([f"- {result['text']}" for result in context_results])
            st.markdown(context_text)

            # Generate response using LLM
            with st.spinner("Generating response with LLM..."):
                prompt = f"Using the following context, answer the question:\n\nContext:\n{context_text}\n\nQuestion: {query_text}"
                response = get_response_from_llm(prompt)

            st.subheader("🤖 LLM Response")
            st.markdown(response)
        else:
            st.warning("No relevant context found. Try rephrasing your question or increasing the number of results.")
    else:
        st.error("Please enter a valid question.")

# Footer Section
st.markdown(
    """
    ---
    Powered by:
    - **[Pinecone](https://www.pinecone.io/)** for vector database management.  
    - **[Google Generative AI](https://cloud.google.com/vertex-ai/docs/generative-ai/overview)** for advanced AI capabilities.  
    - **[Streamlit](https://streamlit.io/)** for an interactive frontend.
    """
)
