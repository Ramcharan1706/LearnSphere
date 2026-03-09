"""
ML Learning Assistant - Streamlit Application
A comprehensive machine learning learning platform with improved code structure.

Features:
- Text Explanation using AI
- Code Generation for ML algorithms
- Audio Learning with multi-language support
- Image Visualization with Mermaid diagrams

Powered by Google Gemini AI
"""

import streamlit as st
import os
import time
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import utility modules
from utils.genai_utils import generate_explanation, generate_code_example, generate_visual_description
from utils.audio_utils import generate_audio
from utils.image_utils import generate_mermaid_diagram, get_diagram_suggestions
from utils.code_executor import clean_code_block

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION & SETUP
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="ML Learning Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

class SessionManager:
    """Manages all session state variables"""
    
    @staticmethod
    def init():
        """Initialize all session state variables"""
        defaults = {
            'topic': '',
            'explanation': '',
            'code': '',
            'audio_path': '',
            'mermaid_code': '',
            'learning_history': [],
            'current_topic': '',
            'language': 'en',
            'viz_type': 'Mermaid Diagram',
            'include_comments': True,
            'slow_speech': False,
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @staticmethod
    def add_to_history(topic, mode):
        """Add topic to learning history"""
        if 'learning_history' not in st.session_state:
            st.session_state['learning_history'] = []
        
        history = st.session_state['learning_history']
        # Avoid duplicates, move to front if exists
        history = [h for h in history if h['topic'] != topic]
        history.insert(0, {'topic': topic, 'mode': mode, 'timestamp': time.time()})
        st.session_state['learning_history'] = history[:20]  # Keep last 20

# Initialize session state
SessionManager.init()

# ═══════════════════════════════════════════════════════════════════════════════
# STYLING - Dark Modern Theme (Improved)
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* CSS Variables */
    :root {
        --bg-primary: #0A0A0F;
        --bg-secondary: #12121A;
        --bg-tertiary: #1A1A24;
        --bg-card: #1E1E2A;
        --bg-card-hover: #252532;
        --accent-primary: #6366F1;
        --accent-secondary: #8B5CF6;
        --accent-teal: #14B8A6;
        --accent-pink: #EC4899;
        --accent-cyan: #06B6D4;
        --gradient-main: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
        --gradient-cool: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 100%);
        --gradient-warm: linear-gradient(135deg, #F59E0B 0%, #EC4899 100%);
        --text-primary: #F8FAFC;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        --success: #10B981;
        --error: #EF4444;
        --warning: #F59E0B;
        --border-color: rgba(255, 255, 255, 0.08);
        --shadow-glow: 0 0 40px rgba(99,102,241,0.3);
    }
    
    .stApp { background: var(--bg-primary); font-family: 'Inter', sans-serif; }
    #MainMenu, footer, header { visibility: hidden !important; }
    h1, h2, h3, h4 { color: var(--text-primary) !important; font-family: 'Inter', sans-serif !important; }
    p, span, div, label { color: var(--text-secondary) !important; font-family: 'Inter', sans-serif !important; }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #1E1E2A 0%, #2D1B69 50%, #1E1E2A 100%);
        border-radius: 24px;
        padding: 3.5rem 2rem;
        margin-bottom: 2.5rem;
        border: 1px solid var(--border-color);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%236366F1' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    }
    .hero-content { position: relative; z-index: 1; }
    .hero-title { font-size: 3.5rem; font-weight: 800; color: var(--text-primary); margin-bottom: 0.5rem; }
    .hero-title .gradient { background: var(--gradient-main); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .hero-subtitle { color: var(--text-secondary); font-size: 1.25rem; margin-bottom: 1.5rem; }
    .hero-badges { display: flex; justify-content: center; gap: 0.75rem; flex-wrap: wrap; }
    .hero-badge { background: rgba(255,255,255,0.05); padding: 0.5rem 1rem; border-radius: 50px; color: var(--text-secondary); font-size: 0.85rem; border: 1px solid var(--border-color); }
    
    /* Cards with Hover Effects */
    .mode-card {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        height: 100%;
    }
    .mode-card:hover {
        transform: translateY(-4px);
        border-color: var(--accent-primary);
        box-shadow: 0 10px 30px rgba(99,102,241,0.2);
    }
    .mode-card h3 { font-size: 1.25rem; margin-bottom: 0.5rem; color: var(--text-primary) !important; }
    .mode-card p { font-size: 0.9rem; line-height: 1.6; color: var(--text-secondary) !important; }
    .mode-icon { font-size: 2.5rem; margin-bottom: 0.75rem; display: block; }
    
    /* Feature Tags */
    .feature-tag {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        color: var(--accent-primary);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-right: 0.25rem;
        margin-top: 0.5rem;
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        color: var(--text-primary) !important;
        font-size: 1rem !important;
    }
    .stTextInput > div > div > input:focus { border-color: var(--accent-primary) !important; box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important; }
    .stTextInput > div > div > input::placeholder { color: var(--text-muted) !important; }
    
    /* Selectbox */
    .stSelectbox > div > div > div { background: var(--bg-tertiary) !important; border: 1px solid var(--border-color) !important; border-radius: 12px !important; }
    
    /* Checkbox */
    .stCheckbox > label { color: var(--text-secondary) !important; font-size: 0.9rem; }
    
    /* Buttons */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"] {
        background: var(--gradient-main) !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(99,102,241,0.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99,102,241,0.4) !important;
    }
    .stButton > button[kind="secondary"] {
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }
    .stButton > button[kind="secondary"]:hover {
        border-color: var(--accent-primary) !important;
        background: var(--bg-card-hover) !important;
    }
    
    /* Output Containers */
    .output-container {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        border: 1px solid var(--border-color);
    }
    .output-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    /* Stats Cards */
    .stat-card {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    .stat-card:hover { transform: translateY(-2px); border-color: var(--accent-primary); }
    .stat-value { font-size: 2rem; font-weight: 800; background: var(--gradient-main); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stat-label { color: var(--text-muted); font-size: 0.85rem; margin-top: 0.25rem; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background: var(--bg-secondary); border-right: 1px solid var(--border-color); }
    [data-testid="stSidebar"] * { color: var(--text-primary) !important; }
    [data-testid="stSidebar"] .stRadio > div > label {
        background: rgba(255,255,255,0.03);
        padding: 0.6rem 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.25rem;
        transition: all 0.2s ease;
    }
    [data-testid="stSidebar"] .stRadio > div > label:hover { background: rgba(255,255,255,0.08); }
    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] { background: var(--accent-primary) !important; }
    
    /* Alerts */
    .stSuccess { background: rgba(16,185,129,0.1) !important; color: #10B981 !important; border: none !important; }
    .stError { background: rgba(239,68,68,0.1) !important; color: #EF4444 !important; border: none !important; }
    .stWarning { background: rgba(245,158,11,0.1) !important; color: #F59E0B !important; border: none !important; }
    .stInfo { background: rgba(99,102,241,0.1) !important; color: #6366F1 !important; border: none !important; }
    
    /* Progress Bar */
    .stProgress > div > div > div { background: var(--gradient-main) !important; }
    
    /* Spinner */
    .stSpinner > div { border-top-color: var(--accent-primary) !important; }
    
    /* Divider */
    hr { border-color: var(--border-color) !important; }
    
    /* Code Block */
    .stCodeBlock { border-radius: 12px; }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--bg-tertiary);
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg-secondary); }
    ::-webkit-scrollbar-thumb { background: var(--accent-primary); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 🤖 ML Learning Assistant")
    st.markdown("---")
    
    # Mode selection
    mode = st.radio(
        "📚 **Select Mode:**",
        ["🏠 Home", "📝 Text Explanation", "💻 Code Generation", "🎧 Audio Learning", "📊 Visualization"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # API Status with styling
    #api_key = os.getenv("GEMINI_API_KEY")
    #if api_key:
    #    st.markdown("""
   #     <div style="display:flex;align-items:center;gap:0.5rem;padding:0.5rem;background:rgba(16,185,129,0.1);border-radius:8px;">
     #       <span style="color:#10B981;font-size:1.2rem;">✅</span>
       #     <span style="color:#10B981;font-weight:600;">API Connected</span>
      #  </div>
        #""", unsafe_allow_html=True)
   #else:
    #    st.markdown("""
     #   <div style="display:flex;align-items:center;gap:0.5rem;padding:0.5rem;background:rgba(239,68,68,0.1);border-radius:8px;">
      #      <span style="color:#EF4444;font-size:1.2rem;">❌</span>
       #     <span style="color:#EF4444;font-weight:600;">API Not Found</span>
       # </div>
        #""", unsafe_allow_html=True)
        #st.caption("💡 Add `GEMINI_API_KEY` to .env file")
   # st.markdown("---")
    
    # Quick Topics
    st.markdown("### 🚀 Quick Start")
    popular_topics = [
        "Neural Networks", "Backpropagation", "Gradient Descent",
        "Decision Trees", "Random Forest", "Support Vector Machine",
        "K-Means Clustering", "Linear Regression", "CNN", "RNN",
        "Transformers", "GANs", "Autoencoders", "Reinforcement Learning"
    ]
    selected_topic = st.selectbox(
        "📌 **Popular Topics:**",
        ["Select a topic..."] + popular_topics,
        label_visibility="collapsed"
    )
    
    # Learning History
    if 'learning_history' in st.session_state and st.session_state['learning_history']:
        st.markdown("---")
        st.markdown("### 📜 Recent Learning")
        for idx, item in enumerate(st.session_state['learning_history'][:5]):
            # Create a unique key for each history button
            if st.button(f"📖 {item['topic'][:20]}...", key=f"history_{idx}_{item['timestamp']}", use_container_width=True):
                st.session_state['selected_topic'] = item['topic']

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def show_loading_spinner(message: str):
    """Show a loading spinner with custom message"""
    return st.spinner(f"⏳ {message}...")

def show_success(message: str):
    """Show success message with custom styling"""
    st.success(f"✅ {message}")

def show_error(message: str):
    """Show error message"""
    st.error(f"❌ {message}")

def show_warning(message: str):
    """Show warning message"""
    st.warning(f"⚠️ {message}")

# ═══════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ═══════════════════════════════════════════════════════════════════════════════

if mode == "🏠 Home":
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-content">
            <h1 class="hero-title">ML Learning <span class="gradient">Assistant</span></h1>
            <p class="hero-subtitle">Master Machine Learning with AI-powered interactive learning experiences</p>
            <div class="hero-badges">
                <span class="hero-badge">🤖 AI-Powered</span>
                <span class="hero-badge">📚 100+ Topics</span>
                <span class="hero-badge">🌐 7 Languages</span>
                <span class="hero-badge">⚡ Real-time Generation</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown("## 🎯 Choose Your Learning Path")
    st.markdown("Select a mode from the sidebar to start learning machine learning concepts in your preferred format.")
    st.markdown("")
    
    # Feature Cards
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="mode-card">
            <span class="mode-icon">📝</span>
            <h3>Text Explanation</h3>
            <p>Get comprehensive explanations of ML concepts powered by Google Gemini AI. Perfect for understanding theory and fundamentals.</p>
            <span class="feature-tag">Beginner</span>
            <span class="feature-tag">Detailed</span>
            <span class="feature-tag">Structured</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="mode-card">
            <span class="mode-icon">💻</span>
            <h3>Code Generation</h3>
            <p>Generate production-ready Python implementations of ML algorithms with detailed comments and best practices.</p>
            <span class="feature-tag">Python</span>
            <span class="feature-tag">Ready to Run</span>
            <span class="feature-tag">Best Practices</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="mode-card">
            <span class="mode-icon">🎧</span>
            <h3>Audio Learning</h3>
            <p>Convert explanations to audio with multi-language support. Learn on the go with text-to-speech technology.</p>
            <span class="feature-tag">7 Languages</span>
            <span class="feature-tag">MP3 Download</span>
            <span class="feature-tag">Hands-Free</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="mode-card">
            <span class="mode-icon">📊</span>
            <h3>Visualization</h3>
            <p>Visualize ML concepts with auto-generated Mermaid.js diagrams and AI-powered visual descriptions.</p>
            <span class="feature-tag">Mermaid.js</span>
            <span class="feature-tag">Flowcharts</span>
            <span class="feature-tag">Architecture</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Statistics
    st.markdown("## 📈 Platform Statistics")
    
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.markdown('<div class="stat-card"><div class="stat-value">4</div><div class="stat-label">Learning Modes</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="stat-card"><div class="stat-value">7</div><div class="stat-label">Languages</div></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="stat-card"><div class="stat-value">Gemini</div><div class="stat-label">AI Model</div></div>', unsafe_allow_html=True)
    with col_d:
        st.markdown('<div class="stat-card"><div class="stat-value">100+</div><div class="stat-label">ML Topics</div></div>', unsafe_allow_html=True)
    
    # Tips
    st.info("💡 **Tip:** Use the Quick Start dropdown in the sidebar to instantly load popular ML topics!")

# ═══════════════════════════════════════════════════════════════════════════════
# TEXT EXPLANATION PAGE
# ═══════════════════════════════════════════════════════════════════════════════

elif mode == "📝 Text Explanation":
    st.markdown("## 📝 Text Explanation")
    st.markdown("Get detailed, AI-powered explanations of any machine learning topic.")
    st.markdown("")
    
    # Input Section
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        topic = st.text_input(
            "**Enter topic:**",
            value=selected_topic if selected_topic != "Select a topic..." else "",
            placeholder="e.g., Backpropagation in Neural Networks",
            label_visibility="collapsed"
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("🔍 Generate", type="primary", use_container_width=True, key="btn_generate_text")
    
    # Output Section
    if generate_btn:
        if topic.strip():
            with show_loading_spinner("AI is generating your explanation..."):
                result = generate_explanation(topic)
            
            if result["success"]:
                show_success("Explanation generated successfully!")
                
                # Save to session
                st.session_state['explanation'] = result['explanation']
                st.session_state['current_topic'] = topic
                SessionManager.add_to_history(topic, "Text")
                
                # Display output
                st.markdown(f"""
                <div class="output-container">
                    <div class="output-header">
                        <strong style="color:var(--text-primary);font-size:1.1rem;">📚 {topic}</strong>
                    </div>
                    <div style="line-height:1.8;color:var(--text-secondary);">
                        {result['explanation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Additional options
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🎧 Create Audio", use_container_width=True, key="btn_create_audio"):
                        st.session_state['mode_redirect'] = 'Audio'
                with col2:
                    if st.button("📊 Create Diagram", use_container_width=True, key="btn_create_diagram"):
                        st.session_state['mode_redirect'] = 'Visual'
            else:
                show_error(result['error'])
        else:
            show_warning("Please enter a topic to learn about.")
    
    # Show saved explanation
    elif st.session_state.get('explanation') and st.session_state.get('current_topic'):
        st.markdown("---")
        st.markdown("### 📋 Previous Explanation")
        with st.expander(f"View: {st.session_state['current_topic']}", expanded=False):
            st.markdown(st.session_state['explanation'])

# ═══════════════════════════════════════════════════════════════════════════════
# CODE GENERATION PAGE
# ═══════════════════════════════════════════════════════════════════════════════

elif mode == "💻 Code Generation":
    st.markdown("## 💻 Code Generation")
    st.markdown("Generate production-ready Python implementations of ML algorithms.")
    st.markdown("")
    
    # Input Section
    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input(
            "**Algorithm or concept:**",
            value=selected_topic if selected_topic != "Select a topic..." else "",
            placeholder="e.g., K-Means Clustering from scratch",
            label_visibility="collapsed"
        )
    with col2:
        include_comments = st.checkbox("Comments", value=True)
    
    st.markdown("")
    generate_btn = st.button("⚡ Generate Code", type="primary", use_container_width=True, key="btn_generate_code")
    
    # Output Section
    if generate_btn:
        if topic.strip():
            with show_loading_spinner("Generating Python code..."):
                result = generate_code_example(topic, include_comments)
            
            if result["success"]:
                show_success("Code generated successfully!")
                
                # Save to session
                st.session_state['code'] = result['code']
                SessionManager.add_to_history(topic, "Code")
                
                # Clean and display code
                cleaned = clean_code_block(result["code"])
                
                st.markdown(f"""
                <div class="output-container">
                    <div class="output-header">
                        <strong style="color:var(--text-primary);">💻 {topic}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.code(cleaned, language="python")
                
                # Download button
                st.download_button(
                    "📥 Download Python File",
                    data=cleaned,
                    file_name=f"{topic.replace(' ', '_').lower()}.py",
                    mime="text/x-python",
                    use_container_width=True
                )
            else:
                show_error(result['error'])
        else:
            show_warning("Please enter an algorithm or concept.")

# ═══════════════════════════════════════════════════════════════════════════════
# AUDIO LEARNING PAGE
# ═══════════════════════════════════════════════════════════════════════════════

elif mode == "🎧 Audio Learning":
    st.markdown("## 🎧 Audio Learning")
    st.markdown("Convert ML explanations to audio for hands-free learning.")
    st.markdown("")
    
    # Input Section
    topic = st.text_input(
        "**Topic to learn:**",
        value=selected_topic if selected_topic != "Select a topic..." else "",
        placeholder="e.g., Gradient Descent"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox(
            "🌐 Language",
            ["en", "es", "fr", "de", "hi", "ja", "zh-CN"],
            index=0,
            format_func=lambda x: {
                "en": "🇬🇧 English", "es": "🇪🇸 Spanish", "fr": "🇫🇷 French",
                "de": "🇩🇪 German", "hi": "🇮🇳 Hindi", "ja": "🇯🇵 Japanese",
                "zh-CN": "🇨🇳 Chinese"
            }[x]
        )
    with col2:
        slow = st.checkbox("🐢 Slow speech (for clarity)", value=False)
    
    st.markdown("")
    generate_btn = st.button("🎙️ Generate Audio", type="primary", use_container_width=True, key="btn_generate_audio")
    
    # Output Section
    if generate_btn:
        if topic.strip():
            # Step 1: Generate text
            with show_loading_spinner("Generating explanation text..."):
                text_result = generate_explanation(topic)
            
            if not text_result["success"]:
                show_error(text_result['error'])
            else:
                explanation = text_result['explanation']
                
                # Show text preview
                with st.expander("📄 View Text Explanation", expanded=False):
                    st.markdown(explanation)
                
                # Step 2: Generate audio
                with show_loading_spinner("Converting to audio..."):
                    audio_result = generate_audio(explanation, language=language, slow=slow)
                
                if audio_result["success"]:
                    show_success("Audio generated successfully!")
                    
                    audio_path = audio_result["audio_url"].lstrip("/")
                    if os.path.exists(audio_path):
                        with open(audio_path, "rb") as f:
                            audio_bytes = f.read()
                        
                        st.markdown("""
                        <div class="output-container">
                            <div class="output-header">
                                <strong style="color:var(--text-primary);">🎧 Audio Player</strong>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.audio(audio_bytes, format="audio/mp3")
                        st.download_button(
                            "📥 Download MP3",
                            data=audio_bytes,
                            file_name=f"{topic.replace(' ', '_').lower()}.mp3",
                            mime="audio/mpeg",
                            use_container_width=True
                        )
                        
                        SessionManager.add_to_history(topic, "Audio")
                    else:
                        show_warning("Audio file generated but could not be located.")
                else:
                    show_error(audio_result['error'])
        else:
            show_warning("Please enter a topic.")

# ═══════════════════════════════════════════════════════════════════════════════
# VISUALIZATION PAGE
# ═══════════════════════════════════════════════════════════════════════════════

elif mode == "📊 Visualization":
    st.markdown("## 📊 Image Visualization")
    st.markdown("Generate visual diagrams of ML concepts.")
    st.markdown("")
    
    # Input Section
    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input(
            "**Concept to visualize:**",
            value=selected_topic if selected_topic != "Select a topic..." else "",
            placeholder="e.g., Neural Network Architecture",
            label_visibility="collapsed"
        )
    with col2:
        viz_type = st.selectbox(
            "Type:",
            ["Mermaid Diagram", "AI Visual Description"],
            label_visibility="collapsed"
        )
    
    st.markdown("")
    generate_btn = st.button("🎨 Generate Visualization", type="primary", use_container_width=True, key="btn_generate_viz")
    
    # Output Section
    if generate_btn:
        if topic.strip():
            if viz_type == "Mermaid Diagram":
                with show_loading_spinner("Generating Mermaid diagram..."):
                    result = generate_mermaid_diagram(topic)
                
                if result["success"]:
                    show_success("Diagram generated successfully!")
                    
                    mermaid_code = result["mermaid_code"].strip()
                    SessionManager.add_to_history(topic, "Visual")
                    
                    # Render diagram
                    mermaid_html = f"""
                    <html>
                    <head>
                        <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
                        <script>mermaid.initialize({{startOnLoad:true, theme:'dark'}});</script>
                    </head>
                    <body style="background:#1E1E2A;padding:20px;border-radius:16px;">
                        <div class="mermaid">{mermaid_code}</div>
                    </body>
                    </html>
                    """
                    
                    st.markdown("""
                    <div class="output-container">
                        <div class="output-header">
                            <strong style="color:var(--text-primary);">📊 {topic}</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.components.v1.html(mermaid_html, height=450)
                    
                    # Show code
                    with st.expander("📝 View Mermaid Source Code"):
                        st.code(mermaid_code, language="text")
                else:
                    show_error(result['error'])
            
            elif viz_type == "AI Visual Description":
                with show_loading_spinner("Generating AI visual description..."):
                    result = generate_visual_description(topic)
                
                if result["success"]:
                    show_success("Visual description generated successfully!")
                    
                    description = result['description']
                    SessionManager.add_to_history(topic, "Visual")
                    
                    # Display the AI-generated visual description
                    st.markdown("""
                    <div class="output-container">
                        <div class="output-header">
                            <strong style="color:var(--text-primary);">🎨 AI Visual Description for: {topic}</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Format and display the description with markdown
                    st.markdown(f"""
                    <div style="background: var(--bg-tertiary); padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
                        {description}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Also show diagram suggestions
                    suggestions = get_diagram_suggestions(topic)
                    if suggestions.get('success'):
                        st.markdown("### 🎯 Recommended Diagram Types")
                        
                        for idx, diagram in enumerate(suggestions.get('diagram_types', [])):
                            with st.expander(f"{diagram['type']}", expanded=False):
                                st.markdown(f"**Description:** {diagram['description']}")
                                st.markdown(f"**Recommended Tools:** {', '.join(diagram['tools'])}")
                else:
                    show_error(result['error'])
            
