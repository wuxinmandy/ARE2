import streamlit as st
import time
from config import Config
from agents.requirement_agent import requirement_agent
from agents.enhanced_requirement_agent import enhanced_requirement_agent
from agents.review_agent import review_agent
import asyncio

# Page configuration
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional and minimalist CSS styling
st.markdown("""
<style>
    /* Global styling - cleaner background */
    .block-container {
        padding-top: 1.5rem;
        max-width: 1000px;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    .main {
        background-color: #fdfdfd;
    }
    
    /* Header styling - minimalist design */
    .professional-header {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2.5rem;
        border-radius: 12px;
        color: #495057;
        text-align: left;
        margin-bottom: 2.5rem;
        border: 1px solid #e9ecef;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .professional-header h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 500;
        color: #343a40;
        letter-spacing: -0.5px;
    }
    
    .professional-header p {
        margin: 0.8rem 0 0 0;
        opacity: 0.75;
        font-size: 1rem;
        color: #6c757d;
        font-weight: 400;
    }
    
    /* Phase indicator - ultra clean */
    .phase-tracker {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
        background: transparent;
        padding: 0;
    }
    
    .phase-item {
        display: flex;
        align-items: center;
        padding: 0.75rem 1.5rem;
        margin: 0 0.25rem;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 400;
        border: none;
        background: transparent;
        position: relative;
    }
    
    .phase-current {
        background: #f8f9fa;
        color: #495057;
        border: 1px solid #dee2e6;
    }
    
    .phase-complete {
        background: transparent;
        color: #6c757d;
        position: relative;
    }
    
    .phase-complete::after {
        content: "✓";
        margin-left: 0.5rem;
        color: #28a745;
        font-weight: 500;
    }
    
    .phase-pending {
        background: transparent;
        color: #adb5bd;
    }
    
    /* Message containers - cleaner spacing */
    .message-container {
        margin-bottom: 2rem;
    }
    
    .user-message-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 1.5rem;
    }
    
    .assistant-message-container {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 1.5rem;
    }
    
    .message-box {
        max-width: 70%;
        padding: 1.25rem 1.5rem;
        border-radius: 12px;
        border: none;
        font-size: 0.95rem;
        line-height: 1.7;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    
    .user-message {
        background: #f8f9fa;
        color: #495057;
        border: 1px solid #e9ecef;
    }
    
    .assistant-message {
        background: white;
        color: #495057;
        border: 1px solid #e9ecef;
    }
    
    /* Input area - clean and spacious */
    .input-section {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        margin: 2rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Button styling - minimal and clean */
    .stButton > button {
        background: #6c757d;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 400;
        transition: all 0.2s ease;
        font-size: 0.9rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        background: #5a6268;
        transform: translateY(-1px);
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    
    .stButton > button:focus {
        box-shadow: 0 0 0 3px rgba(108, 117, 125, 0.2);
        outline: none;
    }
    
    /* Sidebar styling - ultra minimal */
    .css-1d391kg {
        background: #fdfdfd;
        border-right: 1px solid #f1f3f4;
    }
    
    /* Score display - clean card design */
    .score-card {
        background: white;
        border: 1px solid #e9ecef;
        padding: 2rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .score-value {
        font-size: 2.5rem;
        font-weight: 300;
        color: #495057;
        margin: 0.5rem 0;
        letter-spacing: -1px;
    }
    
    .score-label {
        color: #6c757d;
        font-size: 0.9rem;
        margin: 0;
        font-weight: 400;
    }
    
    /* Issue highlighting - subtle and clean */
    .highlight-issue {
        background: #fff9e6;
        border-left: 2px solid #ffc107;
        padding: 4px 8px;
        margin: 3px 0;
        border-radius: 4px;
    }
    
    /* Welcome section - spacious and clean */
    .welcome-section {
        background: white;
        padding: 2.5rem;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        margin: 2rem 0;
        text-align: left;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .welcome-section h2 {
        color: #495057;
        margin-bottom: 1.5rem;
        font-size: 1.5rem;
        font-weight: 400;
        letter-spacing: -0.5px;
    }
    
    .welcome-section p {
        color: #6c757d;
        margin-bottom: 2rem;
        line-height: 1.7;
        font-weight: 400;
    }
    
    /* Example cards - minimal and elegant */
    .example-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .example-item {
        background: #fdfdfd;
        border: 1px solid #f1f3f4;
        border-radius: 8px;
        padding: 1.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: center;
    }
    
    .example-item:hover {
        background: white;
        border-color: #dee2e6;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Review section - clean and organized */
    .review-content {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        margin: 1.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Text areas and inputs - clean borders */
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 1px solid #dee2e6;
        padding: 1rem;
        font-size: 0.95rem;
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #dee2e6;
        padding: 0.75rem;
    }
    
    /* Info boxes - subtle styling */
    .stInfo {
        border-radius: 8px;
        background: #f8f9fa;
        border: 1px solid #e9ecef;
    }
    
    /* Reduced element spacing */
    .element-container {
        margin-bottom: 1rem;
    }
    
    /* Clean typography */
    h3 {
        color: #495057;
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #f1f3f4;
        padding-bottom: 0.75rem;
        font-weight: 400;
        letter-spacing: -0.3px;
    }
    
    h4 {
        color: #6c757d;
        font-size: 1rem;
        margin-bottom: 1rem;
        font-weight: 400;
    }
    
    /* Custom scrollbar for cleaner look */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f8f9fa;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #dee2e6;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #adb5bd;
    }
    
    /* Remove default streamlit styling */
    .stApp > header {
        background: transparent;
    }
    
    /* Clean selectbox styling */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1px solid #dee2e6;
    }
    
    /* Spacing improvements */
    .css-1kyxreq {
        margin-top: 1rem;
    }
    
    /* Footer spacing */
    .css-164nlkn {
        margin-top: 3rem;
    }
    
    /* Knowledge Base Features */
    .kb-panel {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .kb-suggestions {
        background: white;
        border-left: 3px solid #17a2b8;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .kb-question-card {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 0.9rem;
    }
    
    .kb-question-card:hover {
        border-color: #007bff;
        background: #f8f9fa;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .kb-status-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-left: 0.5rem;
    }
    
    .kb-enabled {
        background: #d4edda;
        color: #155724;
    }
    
    .kb-disabled {
        background: #f8d7da;
        color: #721c24;
    }
    
    .improvement-card {
        background: linear-gradient(135deg, #fff9e6 0%, #fff3cd 100%);
        border: 1px solid #ffc107;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .completeness-score {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
    
    .score-ring {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        margin: 0 auto 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        font-weight: 600;
        color: white;
    }
    
    .score-excellent { background: #28a745; }
    .score-good { background: #17a2b8; }
    .score-fair { background: #ffc107; color: #212529; }
    .score-poor { background: #dc3545; }
    
    /* Document Upload Styles */
    .upload-section {
        background: white;
        border: 2px dashed #dee2e6;
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .upload-section:hover {
        border-color: #007bff;
        background: #f8f9fa;
    }
    
    .upload-icon {
        font-size: 3rem;
        color: #6c757d;
        margin-bottom: 1rem;
    }
    
    .upload-text {
        color: #6c757d;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .upload-subtext {
        color: #adb5bd;
        font-size: 0.85rem;
    }
    
    .file-list {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .file-item {
        display: flex;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #e9ecef;
    }
    
    .file-item:last-child {
        border-bottom: none;
    }
    
    .file-icon {
        margin-right: 0.5rem;
        color: #6c757d;
    }
    
    .file-success {
        color: #28a745;
        font-weight: 500;
    }
    
    .file-error {
        color: #dc3545;
        font-weight: 500;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        border-radius: 12px;
        border: 2px dashed #dee2e6;
        padding: 1.5rem;
        text-align: center;
        background: white;
        transition: all 0.2s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #007bff;
        background: #f8f9fa;
    }
    
    .stFileUploader label {
        color: #6c757d !important;
        font-weight: 400 !important;
    }
    
    /* Upload progress */
    .upload-progress {
        background: linear-gradient(90deg, #007bff 0%, #0056b3 100%);
        color: white;
        padding: 0.75rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state with multi-session support"""
    # Initialize sessions structure
    if 'sessions' not in st.session_state:
        st.session_state.sessions = {}
    
    # Initialize current session ID
    if 'current_session_id' not in st.session_state:
        st.session_state.current_session_id = None
    
    # Initialize session counter for unique IDs
    if 'session_counter' not in st.session_state:
        st.session_state.session_counter = 0
    
    # Create default session if no sessions exist
    if not st.session_state.sessions and st.session_state.current_session_id is None:
        create_new_session()

def create_new_session(title=None):
    """Create a new chat session"""
    st.session_state.session_counter += 1
    session_id = f"session_{st.session_state.session_counter}"
    
    if title is None:
        title = f"New Session {st.session_state.session_counter}"
    
    st.session_state.sessions[session_id] = {
        'id': session_id,
        'title': title,
        'created_at': time.time(),
        'current_phase': 'input',
        'original_requirement': '',
        'enhanced_requirement': '',
        'chat_history': [],
        'review_result': None
    }
    
    st.session_state.current_session_id = session_id
    return session_id

def get_current_session():
    """Get current session data"""
    if st.session_state.current_session_id and st.session_state.current_session_id in st.session_state.sessions:
        return st.session_state.sessions[st.session_state.current_session_id]
    return None

def update_session_data(key, value):
    """Update current session data"""
    if st.session_state.current_session_id and st.session_state.current_session_id in st.session_state.sessions:
        st.session_state.sessions[st.session_state.current_session_id][key] = value

def switch_to_session(session_id):
    """Switch to a specific session"""
    if session_id in st.session_state.sessions:
        st.session_state.current_session_id = session_id

def delete_session(session_id):
    """Delete a session"""
    if session_id in st.session_state.sessions:
        del st.session_state.sessions[session_id]
        
        # If deleting current session, switch to another or create new
        if st.session_state.current_session_id == session_id:
            if st.session_state.sessions:
                st.session_state.current_session_id = list(st.session_state.sessions.keys())[0]
            else:
                create_new_session()

def show_chat_history_sidebar():
    """Display chat history navigation in sidebar"""
    with st.sidebar:
        st.markdown("### 💬 Chat Sessions")
        
        # New session button
        if st.button("➕ New Session", use_container_width=True, key="new_session_btn"):
            create_new_session()
            st.rerun()
        
        st.markdown("---")
        
        # Display session list
        if st.session_state.sessions:
            for session_id, session_data in st.session_state.sessions.items():
                is_current = session_id == st.session_state.current_session_id
                
                # Session title with status indicator
                title = session_data.get('title', 'Untitled Session')
                phase = session_data.get('current_phase', 'input')
                
                # Phase icon
                phase_icon = {
                    'input': '📝',
                    'enhance': '🔄', 
                    'review': '✅'
                }.get(phase, '📝')
                
                # Truncate long titles
                if len(title) > 25:
                    display_title = title[:22] + "..."
                else:
                    display_title = title
                
                # Session button with current indicator
                button_style = "🔵 " if is_current else ""
                button_text = f"{button_style}{phase_icon} {display_title}"
                
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    if st.button(button_text, key=f"session_btn_{session_id}", use_container_width=True):
                        if not is_current:
                            switch_to_session(session_id)
                            st.rerun()
                
                with col2:
                    # Delete button for non-current sessions or if more than one session exists
                    if len(st.session_state.sessions) > 1:
                        if st.button("🗑️", key=f"del_btn_{session_id}", help="Delete session"):
                            delete_session(session_id)
                            st.rerun()
        
        st.markdown("---")

def show_model_selector():
    """Display model selector in sidebar"""
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        models = Config.get_available_models()
        
        model_options = [f"{m['name']}" for m in models]
        model_ids = [m['id'] for m in models]
        
        selected_idx = st.selectbox(
            "AI Model",
            range(len(model_options)),
            format_func=lambda x: model_options[x],
            label_visibility="visible"
        )
        
        selected_model = model_ids[selected_idx]
        selected_model_info = models[selected_idx]
        
        # Cleaner info display
        if selected_model == 'demo':
            st.info("🔄 Demo Mode\n\nConfigure API keys for production use")
        else:
            st.success(f"✅ {selected_model_info['description']}")
        
        # Knowledge Base Status
        st.markdown("---")
        st.markdown("### 🧠 Knowledge Base")
        
        try:
            from services.knowledge_base import knowledge_base_service
            
            if knowledge_base_service.is_initialized:
                st.success("🟢 **LightRAG Enabled**\n\nAdvanced knowledge processing active")
            else:
                st.warning("🟡 **Basic Mode**\n\nInstall LightRAG for advanced features")
        except:
            st.error("🔴 **Not Available**\n\nKnowledge base disabled")
        
        # Show uploaded documents
        if 'uploaded_documents' in st.session_state and st.session_state.uploaded_documents:
            st.markdown("**📄 Uploaded Documents:**")
            for i, doc in enumerate(st.session_state.uploaded_documents[-3:]):  # Show last 3
                st.markdown(f"• `{doc['filename']}`")
            
            if len(st.session_state.uploaded_documents) > 3:
                st.markdown(f"*...and {len(st.session_state.uploaded_documents) - 3} more*")
        
        return selected_model

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
    current_session = get_current_session()
    if not current_session:
        return
        
    phases = [
        ('input', '1. Input Requirements'),
        ('enhance', '2. Enhancement & Review'),
        ('review', '3. Quality Assessment')
    ]
    
    phase_html = '<div class="phase-tracker">'
    
    for phase_id, phase_name in phases:
        if phase_id == current_session['current_phase']:
            class_name = "phase-item phase-current"
        elif (phase_id == 'enhance' and current_session['current_phase'] == 'review') or \
             (phase_id == 'input' and current_session['current_phase'] in ['enhance', 'review']):
            class_name = "phase-item phase-complete"
        else:
            class_name = "phase-item phase-pending"
        
        phase_html += f'<div class="{class_name}">{phase_name}</div>'
    
    phase_html += '</div>'
    st.markdown(phase_html, unsafe_allow_html=True)

def show_welcome_screen():
    """Show welcome screen for requirement input"""
    st.markdown("""
    <div class="welcome-section">
        <h2>Project Requirements</h2>
        <p>Share your project vision and we'll help you create comprehensive, well-structured requirements.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input area with cleaner spacing
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    requirement = st.text_area(
        "Project Description",
        placeholder="Describe what you want to build...\n\nExample: An e-commerce platform for handmade products with inventory management and customer reviews.",
        height=120,
        key="requirement_input",
        label_visibility="collapsed"
    )
    
    # Centered button with better spacing
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("✨ Analyze", type="primary", use_container_width=True):
            if requirement.strip():
                # Update current session with requirement and generate title
                update_session_data('original_requirement', requirement.strip())
                update_session_data('current_phase', 'enhance')
                
                # Generate session title from requirement (first 30 chars)
                title = requirement.strip()[:30]
                if len(requirement.strip()) > 30:
                    title += "..."
                update_session_data('title', title)
                
                st.rerun()
            else:
                st.warning("Please describe your project first.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Document Upload Section for Knowledge Base
    st.markdown("### 📚 Build Knowledge Base")
    st.markdown("Upload documents to enhance the AI's domain expertise for your project:")
    
    # Upload area
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Upload Documents for Knowledge Base",
        type=['txt', 'pdf', 'docx', 'doc'],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="Supported formats: TXT, PDF, DOCX, DOC"
    )
    
    if uploaded_files:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("**📄 Files ready to upload:**")
            for file in uploaded_files:
                file_size = len(file.getvalue()) / 1024  # KB
                st.markdown(f"- `{file.name}` ({file_size:.1f} KB)")
        
        with col2:
            if st.button("🔄 Process Documents", type="secondary", use_container_width=True):
                process_uploaded_documents(uploaded_files)
    
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
    """Show requirement enhancement phase with knowledge base integration"""
    current_session = get_current_session()
    if not current_session:
        return
        
    st.markdown("### Requirements Enhancement")
    
    # Knowledge Base Status Panel
    col1, col2 = st.columns([3, 1])
    
    with col2:
        # Import here to avoid circular imports
        from services.knowledge_base import knowledge_base_service
        
        kb_status = "🟢 Enabled" if knowledge_base_service.is_initialized else "🔴 Disabled"
        st.markdown(f"""
        <div class="kb-panel">
            <h4>🧠 AI Knowledge Base</h4>
            <p>Status: {kb_status}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show smart questions if available
        if current_session['original_requirement']:
            smart_questions = enhanced_requirement_agent.get_smart_questions(
                current_session['original_requirement']
            )
            
            if smart_questions:
                st.markdown("**💡 Smart Questions:**")
                for i, question in enumerate(smart_questions[:4]):
                    if st.button(f"❓ {question}", key=f"smart_q_{i}", use_container_width=True):
                        # Add the question to chat input
                        st.session_state['selected_question'] = question
    
    with col1:
        # Initialize conversation if empty
        if not current_session['chat_history']:
            with st.spinner("🧠 Analyzing requirements with AI knowledge base..."):
                # Try enhanced agent with knowledge base first
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    result = loop.run_until_complete(
                        enhanced_requirement_agent.enhance_requirement_with_kb(
                            current_session['original_requirement'],
                            selected_model
                        )
                    )
                    
                    if result["success"]:
                        initial_message = f"**Original requirement:** {current_session['original_requirement']}"
                        
                        # Show knowledge base suggestions if available
                        kb_suggestions_text = ""
                        if result.get("kb_suggestions"):
                            kb_suggestions_text = "\n\n**🧠 Knowledge Base Insights:**\n"
                            for suggestion in result["kb_suggestions"]:
                                kb_suggestions_text += f"- {suggestion}\n"
                        
                        chat_history = [
                            {"role": "user", "content": initial_message},
                            {"role": "assistant", "content": result["enhanced_requirement"] + kb_suggestions_text}
                        ]
                        update_session_data('chat_history', chat_history)
                        update_session_data('enhanced_requirement', result["enhanced_requirement"])
                        
                        # Store KB suggestions for later use
                        if result.get("kb_suggestions"):
                            update_session_data('kb_suggestions', result["kb_suggestions"])
                        
                        st.rerun()
                    else:
                        raise Exception("Enhanced agent failed")
                        
                except Exception as e:
                    # Fallback to regular agent
                    result = requirement_agent.enhance_requirement(
                        current_session['original_requirement'],
                        selected_model
                    )
                    if result["success"]:
                        chat_history = [
                            {"role": "user", "content": f"Original requirement: {current_session['original_requirement']}"},
                            {"role": "assistant", "content": result["enhanced_requirement"]}
                        ]
                        update_session_data('chat_history', chat_history)
                        update_session_data('enhanced_requirement', result["enhanced_requirement"])
                        st.rerun()
                    else:
                        st.error(f"Analysis failed: {result['error']}")
                        return
                finally:
                    if 'loop' in locals():
                        loop.close()
        
        # Display chat history
        for message in current_session['chat_history']:
            show_chat_message(message["role"], message["content"])
        
        # Show requirement improvement suggestions
        if current_session['enhanced_requirement']:
            show_requirement_improvements(current_session['enhanced_requirement'])
    
    # Input for continuing conversation
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        # Pre-fill with selected question if any
        default_value = st.session_state.get('selected_question', '')
        if default_value:
            del st.session_state['selected_question']  # Clear after use
        
        user_input = st.text_input(
            "Additional clarifications or modifications",
            placeholder="Ask questions or request changes to the requirements...",
            key="chat_input",
            value=default_value
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Align button with input
        
        send_col, review_col = st.columns(2)
        
        with send_col:
            if st.button("Send", key="send_btn"):
                if user_input.strip():
                    # Add user message
                    new_chat_history = current_session['chat_history'] + [{
                        "role": "user", 
                        "content": user_input.strip()
                    }]
                    update_session_data('chat_history', new_chat_history)
                    
                    # Get AI response with knowledge base
                    with st.spinner("🧠 Processing with knowledge base..."):
                        try:
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            
                            result = loop.run_until_complete(
                                enhanced_requirement_agent.clarify_requirement_with_kb(
                                    current_session['enhanced_requirement'],
                                    user_input.strip(),
                                    selected_model
                                )
                            )
                            
                            if result["success"]:
                                response_content = result["clarified_requirement"]
                                
                                # Add additional suggestions if available
                                if result.get("additional_suggestions"):
                                    response_content += "\n\n**💡 Additional Insights:**\n"
                                    for suggestion in result["additional_suggestions"]:
                                        response_content += f"- {suggestion}\n"
                                
                                final_chat_history = new_chat_history + [{
                                    "role": "assistant",
                                    "content": response_content
                                }]
                                update_session_data('chat_history', final_chat_history)
                                update_session_data('enhanced_requirement', result["clarified_requirement"])
                                st.rerun()
                            else:
                                raise Exception("Enhanced agent failed")
                                
                        except Exception as e:
                            # Fallback to regular agent
                            result = requirement_agent.clarify_requirement(
                                current_session['enhanced_requirement'],
                                user_input.strip(),
                                selected_model
                            )
                            if result["success"]:
                                final_chat_history = new_chat_history + [{
                                    "role": "assistant",
                                    "content": result["clarified_requirement"]
                                }]
                                update_session_data('chat_history', final_chat_history)
                                update_session_data('enhanced_requirement', result["clarified_requirement"])
                                st.rerun()
                            else:
                                st.error(f"Processing failed: {result['error']}")
                        finally:
                            if 'loop' in locals():
                                loop.close()
        
        with review_col:
            if st.button("Review", key="review_btn"):
                if current_session['enhanced_requirement']:
                    update_session_data('current_phase', 'review')
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_review_phase(selected_model):
    """Show requirement review phase"""
    current_session = get_current_session()
    if not current_session:
        return
        
    st.markdown("### Quality Assessment")
    
    # Perform review if not done yet
    if not current_session['review_result']:
        with st.spinner("Conducting quality assessment..."):
            result = review_agent.review_requirement(
                current_session['enhanced_requirement'],
                selected_model
            )
            update_session_data('review_result', result)
    
    if current_session['review_result'] and current_session['review_result']["success"]:
        review_data = current_session['review_result']["review"]
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("#### Final Requirements Document")
            
            # Display highlighted requirements
            highlighted_text = review_agent.highlight_issues(
                current_session['enhanced_requirement'],
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
                update_session_data('current_phase', 'enhance')
                update_session_data('review_result', None)
                st.rerun()
    
    else:
        st.error("Assessment failed. Please try again.")
        if st.button("Retry Assessment"):
            update_session_data('review_result', None)
            st.rerun()

def show_requirement_improvements(requirement_text: str):
    """显示需求改进建议"""
    try:
        # Get improvement suggestions
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        improvements = loop.run_until_complete(
            enhanced_requirement_agent.suggest_requirement_improvements(requirement_text)
        )
        
        if improvements.get("success"):
            improvement_data = improvements["improvements"]
            
            # Completeness Score
            score = improvement_data.get("completeness_score", 5)
            score_class = "score-excellent" if score >= 8 else "score-good" if score >= 6 else "score-fair" if score >= 4 else "score-poor"
            
            st.markdown(f"""
            <div class="completeness-score">
                <div class="score-ring {score_class}">
                    {score}/10
                </div>
                <div>Completeness Score</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Missing Elements
            missing = improvement_data.get("missing_elements", [])
            if missing:
                st.markdown("**⚠️ Missing Elements:**")
                for element in missing[:3]:  # Show top 3
                    st.markdown(f"<div class='improvement-card'>📝 {element}</div>", unsafe_allow_html=True)
            
            # Best Practices
            practices = improvement_data.get("best_practices", [])
            if practices:
                st.markdown("**✨ Best Practices:**")
                for practice in practices[:2]:  # Show top 2
                    st.markdown(f"<div class='kb-suggestions'>💡 {practice}</div>", unsafe_allow_html=True)
                    
    except Exception as e:
        # Silently fail for now
        pass
    finally:
        if 'loop' in locals():
            loop.close()

def process_uploaded_documents(uploaded_files):
    """Process uploaded documents and add to knowledge base"""
    try:
        from services.knowledge_base import knowledge_base_service
        
        processed_docs = []
        failed_docs = []
        
        with st.spinner("📖 Processing documents..."):
            for file in uploaded_files:
                try:
                    # Extract text content based on file type
                    text_content = extract_text_from_file(file)
                    
                    if text_content:
                        if knowledge_base_service.is_initialized:
                            # Add to LightRAG knowledge base
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            
                            # Insert document content into LightRAG
                            loop.run_until_complete(
                                knowledge_base_service.rag.ainsert(f"""
Document: {file.name}

Content:
{text_content}
                                """)
                            )
                            loop.close()
                        else:
                            # Store documents in session state for future use
                            if 'uploaded_documents' not in st.session_state:
                                st.session_state.uploaded_documents = []
                            
                            st.session_state.uploaded_documents.append({
                                'filename': file.name,
                                'content': text_content,
                                'timestamp': time.time()
                            })
                        
                        processed_docs.append(file.name)
                        
                    else:
                        failed_docs.append(file.name)
                        
                except Exception as e:
                    failed_docs.append(f"{file.name} (Error: {str(e)})")
        
        # Show results
        if processed_docs:
            if knowledge_base_service.is_initialized:
                st.success(f"✅ Successfully processed {len(processed_docs)} documents:")
                for doc in processed_docs:
                    st.markdown(f"- ✓ `{doc}`")
                st.info("🧠 Knowledge base updated! The AI can now use insights from your documents.")
            else:
                st.success(f"✅ Successfully uploaded {len(processed_docs)} documents:")
                for doc in processed_docs:
                    st.markdown(f"- ✓ `{doc}`")
                st.info("📄 Documents stored for future use. Knowledge base features will be available once LightRAG is properly installed.")
        
        if failed_docs:
            st.error(f"❌ Failed to process {len(failed_docs)} documents:")
            for doc in failed_docs:
                st.markdown(f"- ✗ `{doc}`")
    
    except Exception as e:
        st.error(f"Document processing failed: {str(e)}")

def extract_text_from_file(uploaded_file):
    """Extract text content from uploaded file"""
    try:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'txt':
            # Text file
            try:
                return uploaded_file.getvalue().decode('utf-8')
            except UnicodeDecodeError:
                # Try different encodings
                for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
                    try:
                        uploaded_file.seek(0)
                        return uploaded_file.getvalue().decode(encoding)
                    except:
                        continue
                st.warning(f"Could not decode text file {uploaded_file.name}")
                return None
        
        elif file_extension == 'pdf':
            # PDF file
            try:
                import pypdf
                from io import BytesIO
                
                pdf_reader = pypdf.PdfReader(BytesIO(uploaded_file.getvalue()))
                text_content = ""
                
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"
                
                if text_content.strip():
                    return text_content.strip()
                else:
                    st.warning(f"No text content found in PDF {uploaded_file.name}")
                    return None
            
            except ImportError:
                st.warning("PDF processing requires pypdf. Install with: `pip install pypdf`")
                return None
            except Exception as e:
                st.warning(f"Error processing PDF {uploaded_file.name}: {str(e)}")
                return None
        
        elif file_extension in ['docx', 'doc']:
            # Word document
            try:
                import docx2txt
                from io import BytesIO
                
                text_content = docx2txt.process(BytesIO(uploaded_file.getvalue()))
                if text_content and text_content.strip():
                    return text_content.strip()
                else:
                    st.warning(f"No text content found in Word document {uploaded_file.name}")
                    return None
            
            except ImportError:
                st.warning("Word document processing requires docx2txt. Install with: `pip install docx2txt`")
                return None
            except Exception as e:
                st.warning(f"Error processing Word document {uploaded_file.name}: {str(e)}")
                return None
        
        else:
            st.warning(f"Unsupported file type: {file_extension}")
            return None
    
    except Exception as e:
        st.error(f"Error extracting text from {uploaded_file.name}: {str(e)}")
        return None

def main():
    """Main function"""
    initialize_session_state()
    
    current_session = get_current_session()
    if not current_session:
        st.error("Session initialization failed")
        return
    
    show_header()
    show_phase_indicator()
    
    # Sidebar with chat history and settings
    show_chat_history_sidebar()
    selected_model = show_model_selector()
    
    # Main content based on current phase
    if current_session['current_phase'] == 'input':
        show_welcome_screen()
    elif current_session['current_phase'] == 'enhance':
        show_enhancement_phase(selected_model)
    elif current_session['current_phase'] == 'review':
        show_review_phase(selected_model)

if __name__ == "__main__":
    main() 