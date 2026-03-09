"""
Styling component for ML Learning Assistant
Contains all CSS styles for the application
"""

import streamlit as st


def apply_styles():
    """Apply global styles to the application"""
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
    
    /* Cards */
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


def show_success(message: str):
    """Show success message"""
    st.success(f"✅ {message}")


def show_error(message: str):
    """Show error message"""
    st.error(f"❌ {message}")


def show_warning(message: str):
    """Show warning message"""
    st.warning(f"⚠️ {message}")
