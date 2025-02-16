import streamlit as st 
from langchain_ollama import ChatOllama
from lanchain_core.output_parsers import StrOutputParser 


from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)

# CUstom CSS Styling

st.markdown("""
<style>
/* Deepseek-style Chat Interface */
[data-testid="stChatMessage"] {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    max-width: 85%;
}

[data-testid="stChatMessage"][role="user"] {
    background-color: #162F4D !important;
    color: white !important;
    margin-left: auto;
    border: 1px solid #0F2133 !important;
}

[data-testid="stChatMessage"][role="assistant"] {
    background-color: #FFFFFF !important;
    color: #1a1a1a !important;
    border: 1px solid #E5E7EB !important;
    margin-right: auto;
}

pre {
    background-color: #1E1E1E !important;
    color: #d4d4d4 !important;
    padding: 1rem !important;
    border-radius: 8px !important;
    overflow-x: auto;
    font-family: 'Consolas', 'Monaco', monospace !important;
    margin: 1rem 0 !important;
}

code {
    background-color: #f3f4f6 !important;
    padding: 0.2em 0.4em !important;
    border-radius: 4px !important;
    font-family: 'Consolas', 'Monaco', monospace !important;
    color: #dc2626 !important;
}

.stTextInput input {
    background-color: #FFFFFF !important;
    border: 2px solid #E5E7EB !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    color: #1a1a1a !important;
}

.stTextInput input:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
}

.stButton button {
    background-color: #3B82F6 !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 8px !important;
    transition: background-color 0.3s ease !important;
}

.stButton button:hover {
    background-color: #2563EB !important;
    color: white !important;
}

/* Additional Streamlit container styling */
.block-container {
    padding-top: 2rem;
    max-width: 800px;
}
</style>
""", unsafe_allow_html=True)
st.title(" DeepSeek Code Companion")
st.caption(" Your AI Pair Programmer with Debugging Superpowers")

#sidebar usage
with st.sidebar:
    st.title("Deepseek Settings")
    model_version = st.selectbox("Model Version", ["r1", "r2", "pro"])
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    st.markdown("---")
    st.markdown("**Advanced Options**")
    max_tokens = st.number_input("Max Tokens", 100, 2000, 500)
    
    if st.button("Save Configuration"):
        st.success("Settings saved!")

st.markdown("Built with [Ollama](https://ollama.ai/) | [LangChain](https://pyhton.langchain.com/)")


# Initiate the chat engine

llm_engine  = ChatOllama(
    model=model_version,
    base_url="http://localhost:11434",

    temperature=0.3

)


# System prompt configuration

system_prompt =SystemMessagePromptTemplate.from_template(
    "you are an expert AI coding assistant. Provide concise, correct solutions"
    "with strategic print statement for debugging. Always respond in English"
)


#session state manegment 
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content" : "Hi! I'm DeepSeek. How can I help you "}]

#Chat Container 
chat_container = st.container()

#Display chat messages

with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message['role']):
            st.markdown(message['content'])


# chat input and processing 

user_query = st.

