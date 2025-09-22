import streamlit as st
import requests
import time
from backend import RAGBackend

# Initialize document set first
if "document_set" not in st.session_state:
    st.session_state.document_set = "employee"

# Page config
page_titles = {
    "employee": "Employee Knowledge Assistant",
    "police": "Police Procedures Assistant", 
    "insurance": "Insurance Agency Assistant",
    "nutanix": "Nutanix Enterprise AI Assistant",
    "law": "NC Driving Law Assistant"
}
page_title = page_titles.get(st.session_state.document_set, "Knowledge Assistant")
st.set_page_config(
    page_title=page_title,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Weaviate Magic Chat style
st.markdown("""
<style>
    .stApp {
        background-color: #0f1419;
        color: #ffffff;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 10rem;
        max-width: 800px;
    }
    
    .stChatMessage {
        background-color: transparent;
        border: none;
        padding: 1rem 0;
    }
    
    .stChatMessage[data-testid="chat-message-user"] {
        background-color: transparent;
    }
    
    .stChatMessage[data-testid="chat-message-assistant"] {
        background-color: #1a1f2e;
        border-radius: 12px;
        margin: 1rem 0;
        padding: 1.5rem;
    }
    
    section[data-testid="stChatInput"] {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(180deg, transparent 0%, #0f1419 50%);
        padding: 2rem 1rem 1rem;
        z-index: 1000;
    }
    
    .stChatInput > div {
        max-width: 800px;
        margin: 0 auto;
        background-color: #1a1f2e;
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 0.75rem 1rem;
    }
    
    .stChatInput input {
        background-color: transparent;
        border: none;
        color: #ffffff;
        font-size: 16px;
    }
    
    .stChatInput input::placeholder {
        color: #718096;
    }
    
    .sidebar .stSelectbox > div > div {
        background-color: #1a1f2e;
        border: 1px solid #2d3748;
        border-radius: 8px;
        color: #ffffff;
    }
    
    .sidebar .stTextInput > div > div > input {
        background-color: #1a1f2e;
        border: 1px solid #2d3748;
        border-radius: 8px;
        color: #ffffff;
    }
    
    .sidebar .stTextInput > div > div > input::placeholder {
        color: #718096;
    }
    
    .sidebar {
        background-color: #0f1419;
    }
    
    .sidebar .stMarkdown {
        color: #ffffff;
    }
    
    h1 {
        color: #ffffff;
        font-weight: 600;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .welcome-message {
        text-align: center;
        color: #718096;
        margin: 2rem 0;
        font-size: 18px;
    }
    
    .stError {
        background-color: #2d1b1b;
        border: 1px solid #e53e3e;
        color: #fed7d7;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "rag_backend" not in st.session_state:
    st.session_state.rag_backend = RAGBackend("employee")
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
if "input_tokens" not in st.session_state:
    st.session_state.input_tokens = 0
if "output_tokens" not in st.session_state:
    st.session_state.output_tokens = 0

# Sidebar configuration
with st.sidebar:
    st.markdown("### Document Set")
    
    document_set = st.selectbox(
        "Select Knowledge Base",
        ["employee", "police", "insurance", "law", "nutanix"],
        format_func=lambda x: "Employee Knowledge" if x == "employee" else ("Police Procedures" if x == "police" else ("Insurance Agency" if x == "insurance" else ("NC Driving Law Assistant" if x == "law" else "Nutanix Enterprise AI Assistant"))),
        index=0 if st.session_state.document_set == "employee" else (1 if st.session_state.document_set == "police" else (2 if st.session_state.document_set == "insurance" else (3 if st.session_state.document_set == "law" else 4)))
    )
    
    # Handle document set change
    if document_set != st.session_state.document_set:
        st.session_state.document_set = document_set
        st.session_state.rag_backend.switch_document_set(document_set)
        st.session_state.messages = []  # Clear chat history
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Configuration")
    
    # CPU Mode Toggle
    cpu_mode = st.checkbox(
        "CPU-Only Mode",
        value=False,
        help="Use CPU-optimized models for inference"
    )
    
    endpoint_url = st.text_input(
        "API Endpoint",
        value="",
        help="OpenAI-compatible API endpoint"
    )
    
    # Model selection based on CPU mode
    if cpu_mode:
        model_help = "CPU-optimized model for inference"
    else:
        model_help = "GPU-accelerated model for responses"
    
    model_name = st.text_input(
        "Model Name",
        value="",
        help=model_help
    )
    
    api_key = st.text_input(
        "API Key",
        value="",
        type="password",
        help="Your API key"
    )
    
    # Test connection button
    if st.button("Test Connection", help="Test API connection with current settings"):
        if all([endpoint_url, model_name, api_key]):
            with st.spinner("Testing connection..."):
                try:
                    import requests
                    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                    test_data = {
                        "model": model_name,
                        "messages": [{"role": "user", "content": "Hello"}],
                        "max_tokens": 10,
                        "stream": False
                    }
                    response = requests.post(endpoint_url, headers=headers, json=test_data, timeout=10)
                    if response.status_code == 200:
                        st.success(f"Connection successful! Model: {model_name}")
                    else:
                        st.error(f"Connection failed: {response.status_code}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
        else:
            st.error("Please fill in all configuration fields first.")
    
    # CPU Mode indicator
    if cpu_mode:
        st.markdown("**CPU Mode Active**")
    else:
        st.markdown("**GPU Mode Active**")
    
    st.markdown("---")
    st.markdown("### Token Usage")
    st.markdown(f"**Input:** {st.session_state.input_tokens:,}")
    st.markdown(f"**Output:** {st.session_state.output_tokens:,}")
    st.markdown(f"**Total:** {st.session_state.total_tokens:,}")
    
    st.markdown("---")
    st.markdown("### Sample Questions")
    
    if st.session_state.document_set == "employee":
        st.markdown("How do I request a badge?")
        st.markdown("What's the VPN setup process?")
        st.markdown("How to book a conference room?")
        st.markdown("Expense report submission steps?")
        st.markdown("How do I reset my password?")
        st.markdown("What's the remote work policy?")
    elif st.session_state.document_set == "police":
        st.markdown("What are the arrest procedures?")
        st.markdown("How do I handle evidence?")
        st.markdown("Traffic stop protocols?")
        st.markdown("Use of force guidelines?")
        st.markdown("How to prepare for court testimony?")
        st.markdown("What are radio communication protocols?")
    elif st.session_state.document_set == "insurance":
        st.markdown("How do I file an auto insurance claim?")
        st.markdown("What does homeowners insurance cover?")
        st.markdown("How do life insurance benefits work?")
        st.markdown("What are workers compensation procedures?")
        st.markdown("How is property damage assessed?")
        st.markdown("What are customer service standards?")
    elif st.session_state.document_set == "nutanix":
        st.markdown("How do I deploy AI workloads on Nutanix?")
        st.markdown("What GPU configurations are supported?")
        st.markdown("What professional services are in the NAI GPT Pro Bundle?")
        st.markdown("How do I launch Nutanix Enterprise AI on Amazon Web Services?")
        st.markdown("How many nodes do I need to run Nutanix Enterprise AI on Nutanix Kubernetes Platform?")
    else:
        st.markdown("What are NC speeding law penalties?")
        st.markdown("How does the license points system work?")
        st.markdown("What are reckless driving penalties?")
        st.markdown("What are NC DUI laws and penalties?")
        st.markdown("How do I defend a traffic violation?")
        st.markdown("What are commercial driver regulations?")

# Main header
if not st.session_state.messages:
    if st.session_state.document_set == "employee":
        st.markdown("# Employee Knowledge Assistant")
        st.markdown('<div class="welcome-message">Ask me anything about company processes and policies</div>', unsafe_allow_html=True)
    elif st.session_state.document_set == "police":
        st.markdown("# Police Procedures Assistant")
        st.markdown('<div class="welcome-message">Ask me anything about police procedures and protocols</div>', unsafe_allow_html=True)
    elif st.session_state.document_set == "insurance":
        st.markdown("# Insurance Agency Assistant")
        st.markdown('<div class="welcome-message">Ask me anything about insurance policies and procedures</div>', unsafe_allow_html=True)
    elif st.session_state.document_set == "nutanix":
        st.markdown("# Nutanix Enterprise AI Assistant")
        st.markdown('<div class="welcome-message">Ask me anything about Nutanix Enterprise AI and infrastructure</div>', unsafe_allow_html=True)
    else:
        st.markdown("# NC Driving Law Assistant")
        st.markdown('<div class="welcome-message">Ask me anything about NC driving laws and traffic regulations</div>', unsafe_allow_html=True)



# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Check if we need to generate response for last message
if (st.session_state.messages and 
    st.session_state.messages[-1]["role"] == "user" and 
    len(st.session_state.messages) % 2 == 1):
    
    prompt = st.session_state.messages[-1]["content"]
    
    # Generate response with streaming
    with st.chat_message("assistant"):
        try:
            response_placeholder = st.empty()
            response_placeholder.markdown("Generating response...")
            
            response_gen, input_tokens, output_tokens = st.session_state.rag_backend.generate_response_stream(
                prompt, endpoint_url, model_name, api_key, cpu_mode
            )
            
            # Real-time streaming display
            full_response = ""
            
            for chunk in response_gen:
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")
                time.sleep(0.01)
            
            # Final response without cursor
            response_placeholder.markdown(full_response)
            
            # Add to message history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # Update token counts
            st.session_state.input_tokens += input_tokens
            st.session_state.output_tokens += output_tokens
            st.session_state.total_tokens += input_tokens + output_tokens
            
            st.rerun()
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.rerun()

# Chat input
if prompt := st.chat_input("Type your question here..."):
    # Strip whitespace from prompt
    prompt = prompt.strip()
    
    if not all([endpoint_url, model_name, api_key]):
        st.error("Please configure the API settings in the sidebar first.")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate response with streaming
        with st.chat_message("assistant"):
            try:
                response_placeholder = st.empty()
                response_placeholder.markdown("Generating response...")
                
                response_gen, input_tokens, output_tokens = st.session_state.rag_backend.generate_response_stream(
                    prompt, endpoint_url, model_name, api_key, cpu_mode
                )
                
                # Real-time streaming display
                full_response = ""
                
                for chunk in response_gen:
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
                    time.sleep(0.01)
                
                # Final response without cursor
                response_placeholder.markdown(full_response)
                
                # Add to message history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                # Update token counts
                st.session_state.input_tokens += input_tokens
                st.session_state.output_tokens += output_tokens
                st.session_state.total_tokens += input_tokens + output_tokens
                
                st.rerun()
                
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.rerun()