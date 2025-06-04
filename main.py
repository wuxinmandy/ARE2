import streamlit as st
import time
from config import Config
from agents.requirement_agent import requirement_agent
from agents.enhanced_requirement_agent import enhanced_requirement_agent
from agents.review_agent import review_agent
import asyncio
import logging

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
        margin-bottom: 0.5rem;
    }
    
    .score-label {
        color: #6c757d;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Input focus states */
    .stTextArea textarea:focus {
        border-color: #6c757d !important;
        box-shadow: 0 0 0 3px rgba(108, 117, 125, 0.1) !important;
    }
    
    /* Refined spacing */
    .element-container {
        margin-bottom: 1rem;
    }
    
    /* Clean selectbox */
    .stSelectbox > div > div {
        background-color: white;
        border: 1px solid #e9ecef;
    }
    
    /* Improved file uploader */
    .stFileUploader > div {
        background-color: #f8f9fa;
        border: 2px dashed #dee2e6;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
    }
    
    .stFileUploader > div:hover {
        border-color: #6c757d;
        background-color: #f1f3f4;
    }
    
    /* Sidebar file uploader - more compact */
    .css-1d391kg .stFileUploader > div {
        padding: 1rem;
        border: 1px dashed #dee2e6;
        background-color: #fdfdfd;
        margin: 0.5rem 0;
    }
    
    .css-1d391kg .stFileUploader > div:hover {
        border-color: #6c757d;
        background-color: #f8f9fa;
    }
    
    /* Sidebar file uploader text */
    .css-1d391kg .stFileUploader label {
        font-size: 0.8rem !important;
        color: #6c757d !important;
    }
    
    /* Sidebar button styling */
    .css-1d391kg .stButton > button {
        padding: 0.5rem 1rem;
        font-size: 0.8rem;
        margin: 0.25rem 0;
    }
    
    /* Enhanced progress indicators */
    .stProgress > div > div {
        background-color: #6c757d;
    }
    
    /* Improved alerts */
    .stAlert {
        border-radius: 8px;
        border: none;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom knowledge base panel */
    .kb-panel {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
    }
    
    .kb-panel h4 {
        margin: 0 0 0.5rem 0;
        color: #495057;
        font-size: 0.9rem;
    }
    
    .kb-panel p {
        margin: 0;
        color: #6c757d;
        font-size: 0.8rem;
    }
    
    /* Smart questions styling */
    .smart-question {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.25rem 0;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .smart-question:hover {
        background: #f8f9fa;
        border-color: #6c757d;
    }
    
    /* Improvement suggestions */
    .improvement-card {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 6px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #856404;
    }
    
    .kb-suggestions {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 6px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #0c5460;
    }
    
    .completeness-score {
        display: flex;
        flex-direction: column;
        align-items: center;
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .score-ring {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .score-excellent {
        background: #d4edda;
        color: #155724;
        border: 2px solid #28a745;
    }
    
    .score-good {
        background: #d1ecf1;
        color: #0c5460;
        border: 2px solid #17a2b8;
    }
    
    .score-fair {
        background: #fff3cd;
        color: #856404;
        border: 2px solid #ffc107;
    }
    
    .score-poor {
        background: #f8d7da;
        color: #721c24;
        border: 2px solid #dc3545;
    }
    
    /* Welcome section styling */
    .welcome-section {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        margin-bottom: 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .welcome-section h2 {
        margin: 0 0 1rem 0;
        color: #343a40;
        font-size: 1.5rem;
        font-weight: 500;
    }
    
    .welcome-section p {
        margin: 0;
        color: #6c757d;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize simplified session state"""
    # Initialize basic session state
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = 'input'
    
    if 'original_requirement' not in st.session_state:
        st.session_state.original_requirement = ''
    
    if 'enhanced_requirement' not in st.session_state:
        st.session_state.enhanced_requirement = ''
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'review_result' not in st.session_state:
        st.session_state.review_result = None
    
    if 'show_knowledge_graph' not in st.session_state:
        st.session_state.show_knowledge_graph = False

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
            
            # Show Knowledge Graph button if we have documents OR LightRAG is initialized
            docs_summary = knowledge_base_service.get_documents_summary()
            can_show_graph = knowledge_base_service.is_initialized or docs_summary['total_documents'] > 0
            
            if can_show_graph:
                # Knowledge Graph Visualization Button
                if st.button("🕸️ View Knowledge Graph", use_container_width=True, key="kg_btn"):
                    st.session_state.show_knowledge_graph = True
                    st.rerun()
            else:
                st.info("💡 Upload documents to enable knowledge graph visualization")
                
            # Show document summary
            if docs_summary['total_documents'] > 0:
                st.markdown(f"""
                **📊 Knowledge Base Summary:**
                - **Total Documents:** {docs_summary['total_documents']}
                - **Total Size:** {docs_summary['total_size_mb']} MB
                - **File Types:** {', '.join(docs_summary['file_types'].keys())}
                """)
                
                # Show recent documents
                uploaded_docs = knowledge_base_service.get_uploaded_documents()
                if uploaded_docs:
                    st.markdown("**📄 Recent Documents:**")
                    # Show last 3 documents
                    for doc in uploaded_docs[-3:]:
                        upload_time = doc['upload_time'][:10]  # Show date only
                        st.markdown(f"• `{doc['filename']}` ({upload_time})")
                    
                    if len(uploaded_docs) > 3:
                        st.markdown(f"*...and {len(uploaded_docs) - 3} more*")
                    
                    # Document management expander
                    with st.expander("📁 Manage Documents"):
                        st.markdown("**All Uploaded Documents:**")
                        for i, doc in enumerate(uploaded_docs):
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"📄 `{doc['filename']}`")
                                st.caption(f"Size: {doc['file_size'] // 1024} KB | Type: {doc['file_type']}")
                                if doc['content_preview']:
                                    st.caption(f"Preview: {doc['content_preview'][:50]}...")
                            with col2:
                                if st.button("🗑️", key=f"del_doc_{i}", help=f"Delete {doc['filename']}"):
                                    with st.spinner(f"Deleting {doc['filename']}..."):
                                        loop = asyncio.new_event_loop()
                                        asyncio.set_event_loop(loop)
                                        
                                        result = loop.run_until_complete(
                                            knowledge_base_service.remove_document(doc['filename'])
                                        )
                                        loop.close()
                                        
                                        if result['success']:
                                            st.success(f"Deleted {doc['filename']}")
                                            st.rerun()
                                        else:
                                            st.error(f"Failed to delete: {result['error']}")
            else:
                st.info("📄 No documents uploaded yet.")
                
        except Exception as e:
            st.error(f"🔴 **Not Available**\n\nKnowledge base error: {str(e)}")
        
        # Document Upload Section - moved from welcome screen
        st.markdown("---")
        st.markdown("### 📚 Upload Documents")
        
        # Show current knowledge base status briefly
        try:
            docs_summary = knowledge_base_service.get_documents_summary()
            if docs_summary['total_documents'] > 0:
                st.markdown(f"💡 **{docs_summary['total_documents']} documents** ready to enhance AI analysis")
            else:
                st.markdown("📄 Upload documents to enhance AI capabilities")
        except:
            st.markdown("📄 Upload documents to enhance AI capabilities")
        
        # File uploader in sidebar
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['txt', 'pdf', 'docx', 'doc'],
            accept_multiple_files=True,
            label_visibility="collapsed",
            help="Supported: TXT, PDF, DOCX, DOC",
            key="sidebar_file_uploader"
        )
        
        if uploaded_files:
            # Show files ready to upload
            st.markdown("**📄 Ready to process:**")
            for file in uploaded_files:
                file_size = len(file.getvalue()) / 1024  # KB
                st.markdown(f"• `{file.name}` ({file_size:.1f} KB)")
            
            # Process button
            if st.button("🔄 Process Documents", type="secondary", use_container_width=True, key="sidebar_process_btn"):
                process_uploaded_documents(uploaded_files)
        
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
                # Update session state
                st.session_state.original_requirement = requirement.strip()
                st.session_state.current_phase = 'enhance'
                st.rerun()
            else:
                st.warning("Please describe your project first.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Optional: Add some helpful tips or examples
    st.markdown("### 💡 Tips for Better Requirements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 Be Specific**
        - Mention target users
        - Include key features
        - Specify platforms needed
        
        **📱 Consider Context**
        - Business goals
        - Technical constraints  
        - Timeline expectations
        """)
    
    with col2:
        st.markdown("""
        **✨ Good Example:**
        *"A mobile-first e-commerce app for local artisans to sell handmade goods. Need inventory management, payment processing, and customer reviews. Targeting iOS/Android with 1000+ concurrent users."*
        
        **❌ Too Vague:**
        *"Make a website for selling stuff."*
        """)

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
        if st.session_state.original_requirement:
            smart_questions = enhanced_requirement_agent.get_smart_questions(
                st.session_state.original_requirement
            )
            
            if smart_questions:
                st.markdown("**💡 Smart Questions:**")
                for i, question in enumerate(smart_questions[:4]):
                    if st.button(f"❓ {question}", key=f"smart_q_{i}", use_container_width=True):
                        # Add the question to chat input
                        st.session_state['selected_question'] = question
    
    with col1:
        # Initialize conversation if empty
        if not st.session_state.chat_history:
            with st.spinner("🧠 Analyzing requirements with AI knowledge base..."):
                # Try enhanced agent with knowledge base first
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    result = loop.run_until_complete(
                        enhanced_requirement_agent.enhance_requirement_with_kb(
                            st.session_state.original_requirement,
                            selected_model
                        )
                    )
                    loop.close()
                    
                    if result['success']:
                        st.session_state.enhanced_requirement = result['enhanced_requirement']
                        
                        # Add to chat history
                        st.session_state.chat_history.append({
                            "role": "user",
                            "content": st.session_state.original_requirement,
                            "timestamp": time.time()
                        })
                        
                        st.session_state.chat_history.append({
                            "role": "assistant", 
                            "content": result['enhanced_requirement'],
                            "timestamp": time.time(),
                            "kb_used": result.get('knowledge_base_used', False),
                            "suggestions": result.get('kb_suggestions', []),
                            "questions": result.get('clarification_questions', [])
                        })
                    else:
                        st.error(f"Failed to enhance requirements: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"Error during requirement enhancement: {str(e)}")
                    logging.error(f"Enhancement error: {e}")
        
        # Display chat history
        for message in st.session_state.chat_history:
            show_chat_message(message["role"], message["content"])
        
        # Chat input area
        st.markdown("---")
        
        # Check for selected question
        initial_text = ""
        if 'selected_question' in st.session_state:
            initial_text = st.session_state['selected_question']
            del st.session_state['selected_question']
        
        user_input = st.text_area(
            "Ask follow-up questions or provide additional information:",
            value=initial_text,
            height=100,
            placeholder="Example: What specific payment methods should be supported? Can you add mobile app requirements?",
            key="chat_input"
        )
        
        col1_inner, col2_inner, col3_inner = st.columns([1, 1, 1])
        
        with col1_inner:
            if st.button("💬 Continue Discussion", use_container_width=True):
                if user_input.strip():
                    # Add user message
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": user_input.strip(),
                        "timestamp": time.time()
                    })
                    
                    # Get clarification from enhanced agent
                    with st.spinner("🔄 Processing your input..."):
                        try:
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            
                            result = loop.run_until_complete(
                                enhanced_requirement_agent.clarify_requirement_with_kb(
                                    st.session_state.enhanced_requirement,
                                    user_input.strip(),
                                    selected_model
                                )
                            )
                            loop.close()
                            
                            if result['success']:
                                st.session_state.enhanced_requirement = result['clarified_requirement']
                                
                                # Add assistant response
                                st.session_state.chat_history.append({
                                    "role": "assistant",
                                    "content": result['clarified_requirement'],
                                    "timestamp": time.time(),
                                    "kb_used": result.get('knowledge_base_used', False)
                                })
                            else:
                                st.error(f"Failed to process input: {result.get('error', 'Unknown error')}")
                                
                        except Exception as e:
                            st.error(f"Error processing input: {str(e)}")
                            logging.error(f"Clarification error: {e}")
                    
                    st.rerun()
                else:
                    st.warning("Please enter your question or additional information.")
        
        with col2_inner:
            if st.button("📋 Review Requirements", use_container_width=True):
                if st.session_state.enhanced_requirement:
                    st.session_state.current_phase = 'review'
                    st.rerun()
                else:
                    st.warning("No enhanced requirements to review yet.")
        
        with col3_inner:
            if st.button("🔄 Start Over", use_container_width=True):
                # Reset session state
                st.session_state.current_phase = 'input'
                st.session_state.original_requirement = ''
                st.session_state.enhanced_requirement = ''
                st.session_state.chat_history = []
                st.session_state.review_result = None
                st.rerun()

def show_review_phase(selected_model):
    """Show requirement review phase"""
    st.markdown("### Quality Assessment")
    
    if not st.session_state.enhanced_requirement:
        st.warning("No enhanced requirements to review. Please go back to the enhancement phase.")
        if st.button("← Back to Enhancement"):
            st.session_state.current_phase = 'enhance'
            st.rerun()
        return
    
    # Auto-review if not done yet
    if not st.session_state.review_result:
        with st.spinner("🔍 Conducting quality assessment..."):
            review_result = review_agent.review_requirement(
                st.session_state.enhanced_requirement, 
                selected_model
            )
            st.session_state.review_result = review_result
    
    # Display current requirement
    st.markdown("#### 📄 Enhanced Requirements")
    st.markdown(f"""
    <div class="assistant-message-container">
        <div class="message-box assistant-message">
            {st.session_state.enhanced_requirement}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display review results
    if st.session_state.review_result and st.session_state.review_result['success']:
        review_data = st.session_state.review_result['review']
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 🔍 Quality Assessment Results")
            
            # Issues
            issues = review_data.get('issues', [])
            if issues:
                for issue in issues:
                    issue_type = issue.get('type', 'info')
                    issue_text = issue.get('text', '')
                    suggestion = issue.get('suggestion', '')
                    
                    if issue_type == 'error':
                        st.error(f"❌ **{issue_text}**\n\n💡 {suggestion}")
                    elif issue_type == 'warning':
                        st.warning(f"⚠️ **{issue_text}**\n\n💡 {suggestion}")
                    else:
                        st.info(f"💡 **{issue_text}**\n\n✨ {suggestion}")
            else:
                st.success("✅ No major issues found in the requirements!")
            
            # Summary
            summary = review_data.get('summary', '')
            if summary:
                st.markdown("#### 📋 Summary")
                st.markdown(summary)
        
        with col2:
            # Score display
            score = review_data.get('score', 5)
            if score >= 8:
                score_class = "score-excellent"
            elif score >= 6:
                score_class = "score-good"
            elif score >= 4:
                score_class = "score-fair"
            else:
                score_class = "score-poor"
                
            st.markdown(f"""
            <div class="completeness-score">
                <div class="score-ring {score_class}">
                    {score}/10
                </div>
                <div>Quality Score</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Failed to generate quality assessment.")
    
    # Show improvements from knowledge base
    show_requirement_improvements(st.session_state.enhanced_requirement)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Back to Enhancement", use_container_width=True):
            st.session_state.current_phase = 'enhance'
            st.rerun()
    
    with col2:
        if st.button("🔄 Re-analyze", use_container_width=True):
            st.session_state.review_result = None
            st.rerun()
    
    with col3:
        if st.button("🔄 Start Over", use_container_width=True):
            # Reset session state
            st.session_state.current_phase = 'input'
            st.session_state.original_requirement = ''
            st.session_state.enhanced_requirement = ''
            st.session_state.chat_history = []
            st.session_state.review_result = None
            st.rerun()

def show_requirement_improvements(requirement_text: str):
    """Show AI-suggested requirement improvements"""
    try:
        # Import here to avoid circular imports
        from services.knowledge_base import knowledge_base_service
        
        if not knowledge_base_service.is_initialized:
            return
        
        with st.spinner("🧠 Analyzing improvement opportunities..."):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            improvement_result = loop.run_until_complete(
                enhanced_requirement_agent.suggest_requirement_improvements(requirement_text)
            )
            loop.close()
            
        if improvement_result.get('success'):
            improvement_data = improvement_result['improvements']
            
            st.markdown("#### 🚀 Knowledge Base Insights")
            
            # Completeness Score
            score = improvement_data.get("completeness_score", 5)
            if score >= 8:
                score_class = "score-excellent"
            elif score >= 6:
                score_class = "score-good"
            elif score >= 4:
                score_class = "score-fair"
            else:
                score_class = "score-poor"
                
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
        duplicate_docs = []
        
        with st.spinner("📖 Processing documents..."):
            for file in uploaded_files:
                try:
                    # Extract text content based on file type
                    text_content = extract_text_from_file(file)
                    
                    if text_content:
                        # Use the new knowledge base service to add document
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        
                        result = loop.run_until_complete(
                            knowledge_base_service.add_document(file.name, text_content)
                        )
                        loop.close()
                        
                        if result['success']:
                            processed_docs.append(file.name)
                        elif result.get('duplicate'):
                            duplicate_docs.append(file.name)
                        else:
                            failed_docs.append(f"{file.name}: {result['error']}")
                    else:
                        failed_docs.append(f"{file.name}: Failed to extract text content")
                        
                except Exception as e:
                    failed_docs.append(f"{file.name}: {str(e)}")
        
        # Show detailed results - more compact for sidebar
        if processed_docs:
            st.success(f"✅ **{len(processed_docs)} documents processed**")
            if knowledge_base_service.is_initialized:
                st.info("🧠 Knowledge base updated! AI can now use these insights.")
            else:
                st.info("📄 Documents stored for future use.")
        
        if duplicate_docs:
            st.warning(f"⚠️ **{len(duplicate_docs)} duplicates skipped**")
        
        if failed_docs:
            st.error(f"❌ **{len(failed_docs)} documents failed**")
            with st.expander("Show errors"):
                for doc in failed_docs:
                    st.markdown(f"• {doc}")
        
        # Show updated summary - compact version
        if processed_docs or duplicate_docs:
            docs_summary = knowledge_base_service.get_documents_summary()
            st.markdown(f"""
            **📊 Knowledge Base:**
            - **{docs_summary['total_documents']} docs** ({docs_summary['total_size_mb']} MB)
            """)
    
    except Exception as e:
        st.error(f"Processing failed: {str(e)}")
        logging.error(f"Document processing error: {e}")

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

def show_knowledge_graph_modal():
    """Display knowledge graph visualization modal"""
    if st.session_state.show_knowledge_graph:
        # Create a modal-like dialog
        st.markdown("""
        <style>
        .knowledge-graph-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .modal-content {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            max-width: 90%;
            max-height: 90%;
            overflow: auto;
            position: relative;
        }
        .close-button {
            position: absolute;
            top: 10px;
            right: 15px;
            font-size: 24px;
            cursor: pointer;
            color: #6c757d;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Modal header with close button
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown("# 🕸️ Knowledge Graph Visualization")
        with col2:
            if st.button("✕", key="close_kg_modal"):
                st.session_state.show_knowledge_graph = False
                st.rerun()
        
        st.markdown("---")
        
        # Generate and display the knowledge graph
        with st.spinner("🔄 Loading knowledge graph..."):
            try:
                graph_data = get_knowledge_graph_data()
                
                if graph_data:
                    # Display graph statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🔗 Nodes", len(graph_data.get('nodes', [])))
                    with col2:
                        st.metric("↔️ Edges", len(graph_data.get('edges', [])))
                    with col3:
                        st.metric("📊 Components", graph_data.get('components', 0))
                    
                    # Graph visualization options
                    st.markdown("### 🎛️ Visualization Options")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        layout_type = st.selectbox(
                            "Layout Algorithm",
                            ["spring", "circular", "kamada_kawai", "random"],
                            index=0,
                            key="layout_select"
                        )
                    
                    with col2:
                        show_labels = st.checkbox("Show Node Labels", value=True, key="labels_check")
                    
                    # Generate and display the graph
                    fig = create_knowledge_graph_visualization(graph_data, layout_type, show_labels)
                    
                    if fig:
                        st.plotly_chart(fig, use_container_width=True, height=600)
                        
                        # Graph analysis
                        st.markdown("### 📊 Graph Analysis")
                        show_graph_analysis(graph_data)
                    else:
                        st.error("Failed to generate graph visualization")
                else:
                    st.warning("📭 No knowledge graph data available. Upload some documents first!")
                    
            except Exception as e:
                st.error(f"Error loading knowledge graph: {str(e)}")
                logging.error(f"Knowledge graph error: {e}")

def get_knowledge_graph_data():
    """Extract knowledge graph data from LightRAG"""
    try:
        from services.knowledge_base import knowledge_base_service
        import os
        import json
        
        # Always try to create a graph from documents first
        docs = knowledge_base_service.get_uploaded_documents()
        
        # If we have documents, create a document-based graph
        if docs and len(docs) > 0:
            return create_document_based_knowledge_graph(docs)
        
        # If no documents available, try LightRAG data
        if not knowledge_base_service.is_initialized:
            return None
            
        # Try to access LightRAG graph data
        working_dir = knowledge_base_service.working_dir
        
        # Look for graph data files that LightRAG might create
        entities = []
        relationships = []
        
        # Check for entities file
        entities_file = working_dir / "kv_store" / "entities.json"
        if entities_file.exists():
            try:
                with open(entities_file, 'r', encoding='utf-8') as f:
                    entities_data = json.load(f)
                    entities = list(entities_data.keys())[:50]  # Limit to 50 for performance
            except:
                pass
        
        # Check for relationships file
        relationships_file = working_dir / "kv_store" / "relationships.json"
        if relationships_file.exists():
            try:
                with open(relationships_file, 'r', encoding='utf-8') as f:
                    rel_data = json.load(f)
                    relationships = list(rel_data.keys())[:100]  # Limit to 100 for performance
            except:
                pass
        
        # If we have LightRAG data, use it
        if entities and relationships:
            # Build graph structure
            nodes = []
            edges = []
            
            # Add entity nodes
            for i, entity in enumerate(entities):
                nodes.append({
                    'id': f"entity_{i}",
                    'label': entity[:30] + "..." if len(entity) > 30 else entity,
                    'type': 'entity',
                    'size': 10
                })
            
            # Add relationship edges
            for i, rel in enumerate(relationships[:50]):  # Limit edges
                if len(nodes) >= 2:
                    source_idx = i % len(nodes)
                    target_idx = (i + 1) % len(nodes)
                    edges.append({
                        'source': nodes[source_idx]['id'],
                        'target': nodes[target_idx]['id'],
                        'label': rel[:20] + "..." if len(rel) > 20 else rel,
                        'type': 'relationship'
                    })
            
            return {
                'nodes': nodes,
                'edges': edges,
                'components': len(set([edge['source'] for edge in edges] + [edge['target'] for edge in edges]))
            }
        
        # Fall back to document-based graph if no LightRAG data
        return create_document_based_knowledge_graph(docs) if docs else None
        
    except Exception as e:
        logging.error(f"Error extracting knowledge graph: {e}")
        # Always try to fall back to document-based graph
        try:
            from services.knowledge_base import knowledge_base_service
            docs = knowledge_base_service.get_uploaded_documents()
            return create_document_based_knowledge_graph(docs) if docs else None
        except:
            return None

def create_document_based_knowledge_graph(docs):
    """Create a knowledge graph based on uploaded documents"""
    try:
        if not docs or len(docs) == 0:
            return None
        
        nodes = []
        edges = []
        
        # Create document nodes
        for i, doc in enumerate(docs[:15]):  # Limit to 15 documents for performance
            nodes.append({
                'id': f"doc_{i}",
                'label': doc['filename'][:25] + "..." if len(doc['filename']) > 25 else doc['filename'],
                'type': 'document',
                'size': min(20, max(10, doc['file_size'] // 1000))  # Size based on file size
            })
        
        # Create file type nodes
        file_types = {}
        for doc in docs:
            file_type = doc['file_type'].upper()
            if file_type not in file_types:
                file_types[file_type] = len([d for d in docs if d['file_type'] == doc['file_type']])
        
        type_nodes = {}
        for file_type, count in file_types.items():
            type_node_id = f"type_{file_type.lower()}"
            nodes.append({
                'id': type_node_id,
                'label': f"{file_type} Files ({count})",
                'type': 'file_type',
                'size': min(30, 15 + count * 2)
            })
            type_nodes[file_type] = type_node_id
        
        # Create keyword/topic nodes based on filenames
        keywords = set()
        for doc in docs:
            filename_lower = doc['filename'].lower()
            # Extract keywords from filename
            if 'trading' in filename_lower or 'stock' in filename_lower:
                keywords.add('Trading Systems')
            if 'risk' in filename_lower or 'management' in filename_lower:
                keywords.add('Risk Management')
            if 'delivery' in filename_lower or 'futures' in filename_lower:
                keywords.add('Futures & Delivery')
            if 'system' in filename_lower or 'requirements' in filename_lower:
                keywords.add('System Requirements')
            if 'financial' in filename_lower or 'finance' in filename_lower:
                keywords.add('Financial Services')
        
        # Add keyword nodes
        keyword_nodes = {}
        for keyword in keywords:
            keyword_id = f"keyword_{keyword.lower().replace(' ', '_')}"
            nodes.append({
                'id': keyword_id,
                'label': keyword,
                'type': 'topic',
                'size': 25
            })
            keyword_nodes[keyword] = keyword_id
        
        # Create edges between documents and file types
        for i, doc in enumerate(docs[:15]):
            doc_id = f"doc_{i}"
            file_type = doc['file_type'].upper()
            type_node_id = type_nodes.get(file_type)
            
            if type_node_id:
                edges.append({
                    'source': doc_id,
                    'target': type_node_id,
                    'label': 'file_type',
                    'type': 'classification'
                })
        
        # Create edges between documents and topics
        for i, doc in enumerate(docs[:15]):
            doc_id = f"doc_{i}"
            filename_lower = doc['filename'].lower()
            
            for keyword, keyword_id in keyword_nodes.items():
                if any(word in filename_lower for word in keyword.lower().split()):
                    edges.append({
                        'source': doc_id,
                        'target': keyword_id,
                        'label': 'relates_to',
                        'type': 'semantic'
                    })
        
        # Create connections between related documents
        for i in range(len(docs) - 1):
            if i >= 14:  # Limit to first 15 docs
                break
            for j in range(i + 1, min(len(docs), 15)):
                doc1 = docs[i]
                doc2 = docs[j]
                
                # Check if documents are related (same type or similar names)
                if (doc1['file_type'] == doc2['file_type'] or 
                    any(word in doc1['filename'].lower() and word in doc2['filename'].lower() 
                        for word in ['system', 'requirements', 'management', 'trading', 'risk'])):
                    
                    edges.append({
                        'source': f"doc_{i}",
                        'target': f"doc_{j}",
                        'label': 'related',
                        'type': 'similarity'
                    })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'components': len(set([edge['source'] for edge in edges] + [edge['target'] for edge in edges]))
        }
        
    except Exception as e:
        logging.error(f"Error creating document-based graph: {e}")
        return None

def create_sample_knowledge_graph():
    """Create a sample knowledge graph when no data is available"""
    # This function is now replaced by create_document_based_knowledge_graph
    return None

def create_knowledge_graph_visualization(graph_data, layout="spring", show_labels=True):
    """Create interactive knowledge graph visualization using plotly"""
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        import networkx as nx
        import numpy as np
        
        if not graph_data or not graph_data.get('nodes'):
            return None
        
        # Create NetworkX graph
        G = nx.Graph()
        
        # Add nodes
        node_info = {}
        for node in graph_data['nodes']:
            G.add_node(node['id'])
            node_info[node['id']] = node
        
        # Add edges
        for edge in graph_data['edges']:
            if edge['source'] in node_info and edge['target'] in node_info:
                G.add_edge(edge['source'], edge['target'])
        
        # Calculate layout
        if layout == "spring":
            pos = nx.spring_layout(G, k=1, iterations=50)
        elif layout == "circular":
            pos = nx.circular_layout(G)
        elif layout == "kamada_kawai":
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.random_layout(G)
        
        # Extract coordinates
        x_nodes = [pos[node][0] for node in G.nodes()]
        y_nodes = [pos[node][1] for node in G.nodes()]
        
        # Create edge traces
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        # Edge trace
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Node trace
        node_trace = go.Scatter(
            x=x_nodes, y=y_nodes,
            mode='markers+text' if show_labels else 'markers',
            hoverinfo='text',
            text=[node_info[node]['label'] if show_labels else '' for node in G.nodes()],
            textposition="middle center",
            marker=dict(
                size=[node_info[node].get('size', 10) for node in G.nodes()],
                color=[hash(node_info[node]['type']) % 10 for node in G.nodes()],
                colorscale='Viridis',
                line=dict(width=2, color='white')
            )
        )
        
        # Update hover text
        hover_text = []
        for node in G.nodes():
            info = node_info[node]
            hover_text.append(f"<b>{info['label']}</b><br>Type: {info['type']}<br>Connections: {G.degree(node)}")
        
        node_trace.hovertext = hover_text
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title=dict(
                               text="Knowledge Graph Visualization",
                               x=0.5,
                               font=dict(size=20)
                           ),
                           titlefont_size=16,
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           annotations=[ dict(
                               text="Interactive Knowledge Graph - Hover over nodes for details",
                               showarrow=False,
                               xref="paper", yref="paper",
                               x=0.005, y=-0.002,
                               xanchor="left", yanchor="bottom",
                               font=dict(color="#888", size=12)
                           )],
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           plot_bgcolor='white'
                       ))
        
        return fig
        
    except ImportError:
        st.error("📦 Knowledge graph visualization requires additional packages. Install with:\n\n```bash\npip install plotly networkx\n```")
        return None
    except Exception as e:
        st.error(f"Error creating visualization: {str(e)}")
        logging.error(f"Visualization error: {e}")
        return None

def show_graph_analysis(graph_data):
    """Show detailed analysis of the knowledge graph"""
    try:
        import networkx as nx
        
        # Create NetworkX graph for analysis
        G = nx.Graph()
        
        for node in graph_data['nodes']:
            G.add_node(node['id'])
        
        for edge in graph_data['edges']:
            G.add_edge(edge['source'], edge['target'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Graph Metrics:**")
            
            if len(G.nodes()) > 0:
                density = nx.density(G)
                st.markdown(f"- **Density:** {density:.3f}")
                
                if len(G.nodes()) > 1:
                    try:
                        avg_clustering = nx.average_clustering(G)
                        st.markdown(f"- **Average Clustering:** {avg_clustering:.3f}")
                    except:
                        st.markdown("- **Average Clustering:** N/A")
                
                # Connected components
                components = list(nx.connected_components(G))
                st.markdown(f"- **Connected Components:** {len(components)}")
                
                # Degree statistics
                degrees = dict(G.degree())
                if degrees:
                    avg_degree = sum(degrees.values()) / len(degrees)
                    max_degree = max(degrees.values())
                    st.markdown(f"- **Average Degree:** {avg_degree:.1f}")
                    st.markdown(f"- **Max Degree:** {max_degree}")
        
        with col2:
            st.markdown("**🏆 Top Connected Nodes:**")
            
            if len(G.nodes()) > 0:
                degrees = dict(G.degree())
                sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
                
                for i, (node_id, degree) in enumerate(sorted_nodes[:5]):
                    node_info = next((n for n in graph_data['nodes'] if n['id'] == node_id), None)
                    if node_info:
                        label = node_info['label'][:25] + "..." if len(node_info['label']) > 25 else node_info['label']
                        st.markdown(f"- **{label}:** {degree} connections")
                    
                    if i >= 4:  # Limit to top 5
                        break
        
        # Node type distribution
        if graph_data['nodes']:
            st.markdown("**📈 Node Type Distribution:**")
            
            type_counts = {}
            for node in graph_data['nodes']:
                node_type = node.get('type', 'unknown')
                type_counts[node_type] = type_counts.get(node_type, 0) + 1
            
            for node_type, count in type_counts.items():
                percentage = (count / len(graph_data['nodes'])) * 100
                st.markdown(f"- **{node_type.title()}:** {count} nodes ({percentage:.1f}%)")
                
    except ImportError:
        st.info("💡 Install networkx for advanced graph analysis")
    except Exception as e:
        st.error(f"Error in graph analysis: {str(e)}")

def main():
    """Main function"""
    initialize_session_state()
    
    # Check if knowledge graph modal should be shown
    if st.session_state.show_knowledge_graph:
        show_knowledge_graph_modal()
        return  # Don't show other content when modal is open
    
    show_header()
    show_phase_indicator()
    
    # Sidebar with settings
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