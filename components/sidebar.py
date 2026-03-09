"""
Sidebar me create the sidebar component: component for ML Learning Assistant
Contains sidebar navigation and common elements
"""

import streamlit as st
import os


def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        st.markdown("### 🤖 ML Learning Assistant")
        st.markdown("---")
        
        # Navigation is handled by Streamlit's multi-page automatically
        # This sidebar shows common elements
        
        st.markdown("---")
        
        # API Status
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            st.markdown("""
            <div style="display:flex;align-items:center;gap:0.5rem;padding:0.5rem;background:rgba(16,185,129,0.1);border-radius:8px;">
                <span style="color:#10B981;font-size:1.2rem;">✅</span>
                <span style="color:#10B981;font-weight:600;">API Connected</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="display:flex;align-items:center;gap:0.5rem;padding:0.5rem;background:rgba(239,68,68,0.1);border-radius:8px;">
                <span style="color:#EF4444;font-size:1.2rem;">❌</span>
                <span style="color:#EF4444;font-weight:600;">API Not Found</span>
            </div>
            """, unsafe_allow_html=True)
            st.caption("💡 Add `GEMINI_API_KEY` to .env")
        
        st.markdown("---")
        
        # Quick Topics
        st.markdown("### 🚀 Quick Start")
        popular_topics = [
            "Neural Networks", "Backpropagation", "Gradient Descent",
            "Decision Trees", "Random Forest", "Support Vector Machine",
            "K-Means Clustering", "Linear Regression", "CNN", "RNN",
            "Transformers", "GANs", "Autoencoders", "Reinforcement Learning"
        ]
        
        if 'selected_topic' not in st.session_state:
            st.session_state['selected_topic'] = "Select a topic..."
        
        selected = st.selectbox(
            "📌 **Popular Topics:**",
            ["Select a topic..."] + popular_topics,
            label_visibility="collapsed",
            key="topic_selector"
        )
        
        if selected != "Select a topic...":
            st.session_state['selected_topic'] = selected
        
        # Learning History
        if 'learning_history' in st.session_state and st.session_state['learning_history']:
            st.markdown("---")
            st.markdown("### 📜 Recent Learning")
            for item in st.session_state['learning_history'][:5]:
                st.caption(f"• {item['topic']} ({item['mode']})")
        
        return st.session_state.get('selected_topic', None)


def init_session_state():
    """Initialize session state variables"""
    defaults = {
        'topic': '',
        'explanation': '',
        'code': '',
        'audio_path': '',
        'mermaid_code': '',
        'learning_history': [],
        'current_topic': '',
        'selected_topic': 'Select a topic...',
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def add_to_history(topic: str, mode: str):
    """Add topic to learning history"""
    import time
    
    if 'learning_history' not in st.session_state:
        st.session_state['learning_history'] = []
    
    history = st.session_state['learning_history']
    # Avoid duplicates, move to front if exists
    history = [h for h in history if h['topic'] != topic]
    history.insert(0, {'topic': topic, 'mode': mode, 'timestamp': time.time()})
    st.session_state['learning_history'] = history[:20]
