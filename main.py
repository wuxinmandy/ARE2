import streamlit as st
import time
from config import Config
from agents.requirement_agent import requirement_agent
from agents.review_agent import review_agent

# Page configuration
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional and concise CSS styling
st.markdown("""
<style>
    /* Global styling */
    .block-container {
        padding-top: 1rem;
        max-width: 1000px;
    }
    
    .main {
        background-color: #fafafa;
    }
    
    /* Header styling - more formal */
    .professional-header {
        background: #2c3e50;
        padding: 2rem;
        border-radius: 4px;
        color: white;
        text-align: left;
        margin-bottom: 2rem;
        border-left: 4px solid #3498db;
    }
    
    .professional-header h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 600;
        color: white;
    }
    
    .professional-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.85;
        font-size: 1rem;
        color: #ecf0f1;
    }
    
    /* Phase indicator - simplified */
    .phase-tracker {
        display: flex;
        justify-content: center;
        margin: 1.5rem 0;
        background: white;
        padding: 1rem;
        border-radius: 4px;
        border: 1px solid #e0e0e0;
    }
    
    .phase-item {
        display: flex;
        align-items: center;
        padding: 0.5rem 1.5rem;
        margin: 0 0.5rem;
        border-radius: 3px;
        font-size: 0.9rem;
        font-weight: 500;
        border: 1px solid transparent;
    }
    
    .phase-current {
        background: #3498db;
        color: white;
        border-color: #2980b9;
    }
    
    .phase-complete {
        background: #27ae60;
        color: white;
        border-color: #229954;
    }
    
    .phase-pending {
        background: #f8f9fa;
        color: #6c757d;
        border-color: #dee2e6;
    }
    
    /* Message containers - simplified */
    .message-container {
        margin-bottom: 1.5rem;
    }
    
    .user-message-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 1rem;
    }
    
    .assistant-message-container {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 1rem;
    }
    
    .message-box {
        max-width: 75%;
        padding: 1rem 1.25rem;
        border-radius: 4px;
        border: 1px solid #e0e0e0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .user-message {
        background: #3498db;
        color: white;
        border-color: #2980b9;
    }
    
    .assistant-message {
        background: white;
        color: #2c3e50;
        border-color: #bdc3c7;
    }
    
    /* Input area */
    .input-section {
        background: white;
        padding: 1.5rem;
        border-radius: 4px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
    
    /* Button styling - more formal */
    .stButton > button {
        background: #3498db;
        color: white;
        border: 1px solid #2980b9;
        border-radius: 4px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: background-color 0.2s;
        font-size: 0.9rem;
    }
    
    .stButton > button:hover {
        background: #2980b9;
        border-color: #21618c;
    }
    
    .stButton > button:focus {
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: white;
        border-right: 1px solid #e0e0e0;
    }
    
    /* Score display - professional */
    .score-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-left: 4px solid #27ae60;
        padding: 1.5rem;
        border-radius: 4px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .score-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0.5rem 0;
    }
    
    .score-label {
        color: #7f8c8d;
        font-size: 0.9rem;
        margin: 0;
    }
    
    /* Issue highlighting - subtle */
    .highlight-issue {
        background: #fff3cd;
        border-left: 3px solid #ffc107;
        padding: 3px 6px;
        margin: 2px 0;
        border-radius: 2px;
    }
    
    /* Welcome section */
    .welcome-section {
        background: white;
        padding: 2rem;
        border-radius: 4px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        text-align: left;
    }
    
    .welcome-section h2 {
        color: #2c3e50;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    .welcome-section p {
        color: #5d6d7e;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    /* Example cards - simplified */
    .example-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .example-item {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 4px;
        padding: 1rem;
        cursor: pointer;
        transition: all 0.2s;
        text-align: center;
    }
    
    .example-item:hover {
        background: #e9ecef;
        border-color: #3498db;
    }
    
    /* Review section */
    .review-content {
        background: white;
        padding: 1.5rem;
        border-radius: 4px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
    
    /* Text areas and inputs */
    .stTextArea > div > div > textarea {
        border-radius: 4px;
        border: 1px solid #bdc3c7;
    }
    
    .stTextInput > div > div > input {
        border-radius: 4px;
        border: 1px solid #bdc3c7;
    }
    
    /* Info boxes */
    .stInfo {
        border-radius: 4px;
    }
    
    /* Remove excessive padding */
    .element-container {
        margin-bottom: 0.5rem;
    }
    
    /* Professional spacing */
    h3 {
        color: #2c3e50;
        font-size: 1.2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #ecf0f1;
        padding-bottom: 0.5rem;
    }
    
    h4 {
        color: #34495e;
        font-size: 1rem;
        margin-bottom: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state"""
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = 'input'  # input, enhance, review
    if 'original_requirement' not in st.session_state:
        st.session_state.original_requirement = ''
    if 'enhanced_requirement' not in st.session_state:
        st.session_state.enhanced_requirement = ''
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'review_result' not in st.session_state:
        st.session_state.review_result = None

def show_header():
    """Display application header"""
    st.markdown(f"""
    <div class="professional-header">
        <h1>📋 {Config.APP_TITLE}</h1>
        <p>{Config.APP_DESCRIPTION}</p>
    </div>
    """, unsafe_allow_html=True)

def show_phase_indicator():
    """Show current phase indicator"""
    phases = [
        ('input', '1. Input Requirements'),
        ('enhance', '2. Enhancement & Review'),
        ('review', '3. Quality Assessment')
    ]
    
    phase_html = '<div class="phase-tracker">'
    
    for phase_id, phase_name in phases:
        if phase_id == st.session_state.current_phase:
            class_name = "phase-item phase-current"
        elif (phase_id == 'enhance' and st.session_state.current_phase == 'review') or \
             (phase_id == 'input' and st.session_state.current_phase in ['enhance', 'review']):
            class_name = "phase-item phase-complete"
        else:
            class_name = "phase-item phase-pending"
        
        phase_html += f'<div class="{class_name}">{phase_name}</div>'
    
    phase_html += '</div>'
    st.markdown(phase_html, unsafe_allow_html=True)

def show_model_selector():
    """Display model selector in sidebar"""
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        models = Config.get_available_models()
        
        model_options = [f"{m['name']}" for m in models]
        model_ids = [m['id'] for m in models]
        
        selected_idx = st.selectbox(
            "AI Model Selection",
            range(len(model_options)),
            format_func=lambda x: model_options[x]
        )
        
        selected_model = model_ids[selected_idx]
        selected_model_info = models[selected_idx]
        
        st.info(f"**Model:** {selected_model_info['description']}")
        
        if selected_model == 'demo':
            st.warning("**Note:** Demo mode active - Configure API keys for production use")
        
        st.markdown("---")
        
        # Reset functionality
        if st.button("🔄 Reset Session", use_container_width=True):
            for key in ['current_phase', 'original_requirement', 'enhanced_requirement', 'chat_history', 'review_result']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        
        return selected_model

def show_welcome_screen():
    """Show welcome screen for requirement input"""
    st.markdown("""
    <div class="welcome-section">
        <h2>Requirements Input</h2>
        <p>Please provide a brief description of your project requirements. Our AI system will analyze and enhance your requirements to create comprehensive documentation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input area
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    requirement = st.text_area(
        "Project Requirements",
        placeholder="Describe your project requirements here...\n\nExample: I need an e-commerce platform for selling handmade products with inventory management and customer reviews.",
        height=150,
        key="requirement_input"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Analysis", type="primary", use_container_width=True):
            if requirement.strip():
                st.session_state.original_requirement = requirement.strip()
                st.session_state.current_phase = 'enhance'
                st.rerun()
            else:
                st.warning("Please enter your requirements before proceeding.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Example prompts
    st.markdown("### Example Requirements")
    examples = [
        "E-commerce platform with payment integration",
        "Student information management system",
        "Project management application",
        "Restaurant ordering and delivery system"
    ]
    
    st.markdown('<div class="example-grid">', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, example in enumerate(examples):
        with cols[i % 2]:
            if st.button(example, key=f"example_{i}", use_container_width=True):
                st.session_state.original_requirement = example
                st.session_state.current_phase = 'enhance'
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_chat_message(role, content, timestamp=None):
    """Display a chat message"""
    if role == "user":
        st.markdown(f"""
        <div class="user-message-container">
            <div class="message-box user-message">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message-container">
            <div class="message-box assistant-message">
        """, unsafe_allow_html=True)
        st.markdown(content)
        st.markdown("</div></div>", unsafe_allow_html=True)

def show_enhancement_phase(selected_model):
    """Show requirement enhancement phase"""
    st.markdown("### Requirements Enhancement")
    
    # Initialize conversation if empty
    if not st.session_state.chat_history:
        with st.spinner("Analyzing requirements..."):
            result = requirement_agent.enhance_requirement(
                st.session_state.original_requirement,
                selected_model
            )
            
            if result["success"]:
                st.session_state.chat_history = [
                    {"role": "user", "content": f"Original requirement: {st.session_state.original_requirement}"},
                    {"role": "assistant", "content": result["enhanced_requirement"]}
                ]
                st.session_state.enhanced_requirement = result["enhanced_requirement"]
                st.rerun()
            else:
                st.error(f"Analysis failed: {result['error']}")
                return
    
    # Display chat history
    for message in st.session_state.chat_history:
        show_chat_message(message["role"], message["content"])
    
    # Input for continuing conversation
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Additional clarifications or modifications",
            placeholder="Ask questions or request changes to the requirements...",
            key="chat_input"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Align button with input
        
        send_col, review_col = st.columns(2)
        
        with send_col:
            if st.button("Send", key="send_btn"):
                if user_input.strip():
                    # Add user message
                    st.session_state.chat_history.append({
                        "role": "user", 
                        "content": user_input.strip()
                    })
                    
                    # Get AI response
                    with st.spinner("Processing..."):
                        result = requirement_agent.clarify_requirement(
                            st.session_state.enhanced_requirement,
                            user_input.strip(),
                            selected_model
                        )
                        
                        if result["success"]:
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": result["clarified_requirement"]
                            })
                            st.session_state.enhanced_requirement = result["clarified_requirement"]
                            st.rerun()
                        else:
                            st.error(f"Processing failed: {result['error']}")
        
        with review_col:
            if st.button("Review", key="review_btn"):
                if st.session_state.enhanced_requirement:
                    st.session_state.current_phase = 'review'
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_review_phase(selected_model):
    """Show requirement review phase"""
    st.markdown("### Quality Assessment")
    
    # Perform review if not done yet
    if not st.session_state.review_result:
        with st.spinner("Conducting quality assessment..."):
            result = review_agent.review_requirement(
                st.session_state.enhanced_requirement,
                selected_model
            )
            st.session_state.review_result = result
    
    if st.session_state.review_result and st.session_state.review_result["success"]:
        review_data = st.session_state.review_result["review"]
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("#### Final Requirements Document")
            
            # Display highlighted requirements
            highlighted_text = review_agent.highlight_issues(
                st.session_state.enhanced_requirement,
                review_data.get("issues", [])
            )
            
            st.markdown(f"""
            <div class="review-content">
                {highlighted_text}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Score display
            score = review_data.get("score", 0)
            
            st.markdown(f"""
            <div class="score-card">
                <div class="score-label">Quality Score</div>
                <div class="score-value">{score}/10</div>
                <div class="score-label">Overall Rating</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Summary
            st.markdown("#### Assessment Summary")
            st.info(review_data.get("summary", "No summary available"))
            
            # Issues list
            issues = review_data.get("issues", [])
            if issues:
                st.markdown(f"#### Issues Identified ({len(issues)})")
                
                for i, issue in enumerate(issues):
                    icon = "🔴" if issue["type"] == "error" else "🟡" if issue["type"] == "warning" else "🔵"
                    
                    with st.expander(f"{icon} {issue['location']}", expanded=False):
                        st.markdown(f"**Issue:** {issue['text']}")
                        st.markdown(f"**Recommendation:** {issue['suggestion']}")
            else:
                st.success("✅ No issues identified. Requirements are well-structured.")
            
            # Navigation
            st.markdown("---")
            if st.button("← Back to Enhancement", use_container_width=True):
                st.session_state.current_phase = 'enhance'
                st.session_state.review_result = None
                st.rerun()
    
    else:
        st.error("Assessment failed. Please try again.")
        if st.button("Retry Assessment"):
            st.session_state.review_result = None
            st.rerun()

def main():
    """Main function"""
    initialize_session_state()
    show_header()
    show_phase_indicator()
    
    # Sidebar
    selected_model = show_model_selector()
    
    # Main content based on current phase
    if st.session_state.current_phase == 'input':
        show_welcome_screen()
    elif st.session_state.current_phase == 'enhance':
        show_enhancement_phase(selected_model)
    elif st.session_state.current_phase == 'review':
        show_review_phase(selected_model)

if __name__ == "__main__":
    main() 