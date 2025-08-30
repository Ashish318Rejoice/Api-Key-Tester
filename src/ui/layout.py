"""
Layout Components for KeyMate

This module contains layout-related components including:
- Header and footer
- Navigation elements
- Sidebar controls
- Notification system
"""

import streamlit as st
from typing import Any, Dict, List

from .styling import inject_custom_css


# App constants
APP_TITLE = "🔑 KeyMate"
APP_SUBTITLE = "Professional validation, exploration, and analysis of LLM API keys"
FOOTER_COPY = "🔒 Keys are never stored or logged • Built with Streamlit"


def render_modern_header() -> None:
    """Render modern header with gradient background."""
    st.set_page_config(
        page_title="KeyMate",
        page_icon="🔑",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inject custom CSS
    inject_custom_css()
    
    # Modern header with gradient
    st.markdown(f"""
    <div class="main-header">
        <h1>{APP_TITLE}</h1>
        <p>{APP_SUBTITLE}</p>
    </div>
    """, unsafe_allow_html=True)


def create_modern_footer() -> None:
    """Create modern footer."""
    st.markdown(f"""
    <div class="footer">
        <div class="footer-content">
            <div>
                <strong>v1.3.0</strong> • KeyMate
            </div>
            <div>
                {FOOTER_COPY}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def create_sidebar_controls() -> Dict[str, Any]:
    """Create modern sidebar controls."""
    with st.sidebar:
        st.markdown("## 🎛️ Controls")
        
        # Mode selection
        mode = st.selectbox(
            "Mode",
            ["Validate & List Models", "Model Insights ", "Advanced Analysis"],
            key="app_mode"
        )
        
        st.divider()
        
        # Advanced settings
        with st.expander("⚙️ Advanced Settings", expanded=False):
            timeout = st.slider("Timeout (seconds)", 5, 60, 30)
            retries = st.slider("Max Retries", 0, 5, 3)
            show_raw = st.toggle("Show Raw JSON", value=False)
            auto_refresh = st.toggle("Auto Refresh", value=False)
            
            if st.button("Reset Session", type="secondary"):
                st.session_state.clear()
                st.rerun()
        
        st.divider()
        
        # Theme and appearance
        with st.expander("🎨 Appearance", expanded=False):
            theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
            density = st.selectbox("Density", ["Comfortable", "Compact"])
        
        return {
            "mode": mode,
            "timeout": timeout,
            "retries": retries,
            "show_raw": show_raw,
            "auto_refresh": auto_refresh,
            "theme": theme,
            "density": density
        }


def create_notification_system() -> None:
    """Create a modern notification system."""
    if "notifications" not in st.session_state:
        st.session_state.notifications = []
    
    # Display notifications
    for notification in st.session_state.notifications:
        if notification["type"] == "success":
            st.success(notification["message"])
        elif notification["type"] == "error":
            st.error(notification["message"])
        elif notification["type"] == "warning":
            st.warning(notification["message"])
        elif notification["type"] == "info":
            st.info(notification["message"])
    
    # Clear notifications after display
    st.session_state.notifications = []


def add_notification(message: str, notification_type: str = "info") -> None:
    """Add a notification to the queue."""
    if "notifications" not in st.session_state:
        st.session_state.notifications = []
    
    st.session_state.notifications.append({
        "message": message,
        "type": notification_type
    })


def get_state() -> Dict[str, Any]:
    """Get or initialize session state."""
    if "state" not in st.session_state:
        st.session_state.state = {
            "api_key": "",
            "provider": None,
            "is_valid": None,
            "status_msg": "",
            "account_status": None,
            "models_payload": None,
            "models_table": None,
            "selected_model": None,
            "raw_model_json": None,
            "show_raw_json": False,
            "current_tab": "validation",
            "search_query": "",
            "filter_type": "all",
        }
    return st.session_state.state
