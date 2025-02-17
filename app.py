import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)

# Custom CSS styling
st.markdown("""
<style>
    .main {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #2d2d2d;
    }
    .stTextInput textarea {
        color: #ffffff !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        color: white !important;
        background-color: #3d3d3d !important;
    }
    .stSelectbox svg {
        fill: white !important;
    }
    .stSelectbox option {
        background-color: #2d2d2d !important;
        color: white !important;
    }
    div[role="listbox"] div {
        background-color: #2d2d2d !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📄 DeepSeek Resume Pro")
st.caption("🎯 ATS-Optimized Resume Crafting with AI Assistance")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    selected_model = st.selectbox(
        "Choose Model",
        ["deepseek-r1:1.5b", "deepseek-r1:3b"],  # Use your installed DeepSeek models
        index=0
    )
    st.divider()
    st.markdown("### Key Features")
    st.markdown("""
    - ✅ ATS Optimization
    - ✨ Action Verb Suggestions
    - 📈 Quantifiable Achievements
    - 🎯 Job Description Matching
    - 📝 Professional Formatting
    """)
    st.divider()
    st.markdown("Built with [Ollama](https://ollama.ai/) | [LangChain](https://python.langchain.com/)")

# Initiate the chat engine
llm_engine = ChatOllama(
    model=selected_model,
    base_url="http://localhost:11434",
    temperature=0.2
)

# System prompt configuration
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are a professional resume consultant specializing in creating ATS-friendly resumes. "
    "Follow these rules:\n"
    "1. Analyze the user's current resume and job description\n"
    "2. Suggest improvements using industry-specific keywords\n"
    "3. Recommend quantifiable achievements\n"
    "4. Maintain clean, professional formatting\n"
    "5. Ensure consistency in tense and punctuation\n"
    "Ask clarifying questions to create targeted, achievement-oriented content."
)

# Session state management
if "message_log" not in st.session_state:
    st.session_state.message_log = [{
        "role": "ai", 
        "content": "Welcome! Let's craft your perfect resume. 🏆\n\n"
                    "1. Please share the target job description\n"
                    "2. Paste your current resume\n"
                    "3. I'll help optimize it for ATS systems!"
    }]

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input and processing
user_query = st.chat_input("Paste your resume text or ask a question...")

def generate_ai_response(prompt_chain):
    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
    return processing_pipeline.invoke({})

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

if user_query:
    # Add user message to log
    st.session_state.message_log.append({"role": "user", "content": user_query})
    
    # Generate AI response
    with st.spinner("🔍 Analyzing..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain)
    
    # Add AI response to log
    st.session_state.message_log.append({"role": "ai", "content": ai_response})
    
    # Rerun to update chat display
    st.rerun()