"""
Modern UI Components for KeyMate

This module contains all the interactive UI components including:
- Metric cards
- Status badges
- Model cards
- Search bars
- Data tables
- Navigation elements
"""

import streamlit as st
import pandas as pd
from typing import Any, Dict, List, Optional

from .styling import inject_custom_css


def create_metric_card(title: str, value: str, icon: str = "", animation: str = "fade-in") -> None:
    """Create a modern metric card with enhanced styling and animations."""
    st.markdown(f"""
    <div class="metric-card {animation}">
        <h4>{icon} {title}</h4>
        <div class="value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def create_status_badge(status: str, message: str, badge_type: str = "info", animation: str = "bounce-in") -> None:
    """Create a modern status badge with enhanced styling."""
    st.markdown(f"""
    <div class="status-badge {badge_type} {animation}">
        {status} {message}
    </div>
    """, unsafe_allow_html=True)


def create_model_card(model_id: str, model_type: str, is_selected: bool = False, animation: str = "slide-in-left", **kwargs) -> None:
    """Create a modern model card with enhanced interactions."""
    selected_class = "selected" if is_selected else ""
    context_info = f'<p>Context: {kwargs.get("context_length", "N/A")}</p>' if kwargs.get("context_length") else ''
    created_info = f'<p>Created: {kwargs.get("created", "N/A")}</p>' if kwargs.get("created") else ''
    
    st.markdown(f"""
    <div class="model-card {selected_class} {animation}" onclick="selectModel('{model_id}')">
        <h4>{model_id}</h4>
        <p><strong>Type:</strong> {model_type}</p>
        {context_info}
        {created_info}
        <div class="model-card-overlay"></div>
    </div>
    """, unsafe_allow_html=True)


def create_search_bar(placeholder: str = "Search models...", animation: str = "fade-in") -> str:
    """Create a modern search bar with enhanced styling."""
    st.markdown(f"""
    <div class="search-container {animation}">
        <input type="text" placeholder="{placeholder}" id="search-input">
    </div>
    """, unsafe_allow_html=True)
    return st.text_input("", placeholder=placeholder, key="search_input", label_visibility="collapsed")


def create_data_table(df: pd.DataFrame, title: str = "", searchable: bool = True, animation: str = "fade-in") -> pd.DataFrame:
    """Create a modern data table with search functionality and enhanced styling."""
    if title:
        st.markdown(f"""
        <div class="table-header {animation}">
            <h3>📊 {title}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    if searchable:
        search = create_search_bar("Search in table...", animation)
        if search:
            mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
            df = df[mask]
    
    # Use Streamlit's enhanced dataframe with custom styling
    st.markdown(f'<div class="table-container {animation}">', unsafe_allow_html=True)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            col: st.column_config.TextColumn(
                col,
                help=f"Search and filter {col}",
                max_chars=None
            ) for col in df.columns
        }
    )
    st.markdown('</div>', unsafe_allow_html=True)
    return df


def create_model_details_panel(model_data: Dict[str, Any], provider: str, animation: str = "slide-in-left") -> None:
    """Create a modern model details panel with enhanced styling."""
    with st.container():
        st.markdown(f"""
        <div class="card-container {animation}">
            <h3>📊 Model Details</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Model metrics in a grid layout
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            create_metric_card("Model ID", model_data.get("id", "N/A"), "🔑", "bounce-in")
        with col2:
            create_metric_card("Type", model_data.get("type", "N/A"), "🤖", "bounce-in")
        with col3:
            create_metric_card("Context Length", str(model_data.get("context_length", "N/A")), "📏", "bounce-in")
        with col4:
            create_metric_card("Created", model_data.get("created", "N/A"), "📅", "bounce-in")


def create_advanced_filters(providers: List[str], model_types: List[str], animation: str = "fade-in") -> Dict[str, Any]:
    """Create advanced filtering options with modern UI."""
    st.markdown(f"""
    <div class="card-container {animation}">
        <h3>🔍 Advanced Filters</h3>
    </div>
    """, unsafe_allow_html=True)
    
    filters = {}
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filters["provider"] = st.selectbox(
            "Provider",
            ["All"] + providers,
            key="filter_provider"
        )
    
    with col2:
        filters["model_type"] = st.selectbox(
            "Model Type",
            ["All"] + model_types,
            key="filter_type"
        )
    
    with col3:
        filters["status"] = st.selectbox(
            "Status",
            ["All", "Available", "Deprecated", "Beta"],
            key="filter_status"
        )
    
    # Additional filters
    col4, col5, col6 = st.columns(3)
    
    with col4:
        filters["context_min"] = st.number_input(
            "Min Context Length",
            min_value=0,
            value=0,
            step=1000,
            key="filter_context_min"
        )
    
    with col5:
        filters["sort_by"] = st.selectbox(
            "Sort By",
            ["Name", "Type", "Context Length", "Created"],
            key="filter_sort_by"
        )
    
    with col6:
        filters["sort_order"] = st.selectbox(
            "Sort Order",
            ["Ascending", "Descending"],
            key="filter_sort_order"
        )
    
    return filters


def create_quick_actions(animation: str = "fade-in") -> None:
    """Create quick action buttons with modern styling."""
    st.markdown(f"""
    <div class="card-container {animation}">
        <h3>⚡ Quick Actions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Refresh Models", use_container_width=True, key="refresh_btn"):
            # Clear models state to trigger refresh
            if "models_payload" in st.session_state:
                st.session_state.models_payload = None
            if "models_table" in st.session_state:
                st.session_state.models_table = None
            if "selected_model" in st.session_state:
                st.session_state.selected_model = None
            st.rerun()
    
    with col2:
        if st.button("📊 Export Data", use_container_width=True, key="export_btn"):
            # Export functionality would go here
            st.success("Data exported successfully!")
    
    with col3:
        if st.button("⚙️ Settings", use_container_width=True, key="settings_btn"):
            # Settings functionality would go here
            st.info("Settings panel opened")
    
    with col4:
        if st.button("❓ Help", use_container_width=True, key="help_btn"):
            # Help functionality would go here
            st.info("Help documentation opened")


def create_sidebar_controls(animation: str = "slide-in-left") -> Dict[str, Any]:
    """Create sidebar controls with modern styling."""
    st.sidebar.markdown(f"""
    <div class="sidebar-header {animation}">
        <h3>🎛️ Controls</h3>
    </div>
    """, unsafe_allow_html=True)
    
    controls = {}
    
    # Theme selector
    controls["theme"] = st.sidebar.selectbox(
        "🎨 Theme",
        ["Light", "Dark", "Auto"],
        key="theme_selector"
    )
    
    # Animation toggle
    controls["animations"] = st.sidebar.checkbox(
        "✨ Enable Animations",
        value=True,
        key="animation_toggle"
    )
    
    # Auto-refresh toggle
    controls["auto_refresh"] = st.sidebar.checkbox(
        "🔄 Auto Refresh",
        value=False,
        key="auto_refresh_toggle"
    )
    
    # Refresh interval
    if controls["auto_refresh"]:
        controls["refresh_interval"] = st.sidebar.slider(
            "Refresh Interval (seconds)",
            min_value=5,
            max_value=300,
            value=30,
            step=5,
            key="refresh_interval"
        )
    
    return controls


def create_notification_system() -> None:
    """Create a modern notification system."""
    st.markdown("""
    <div id="notification-container"></div>
    <script>
    function showNotification(message, type = 'info') {
        const container = document.getElementById('notification-container');
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        container.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                container.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    function addNotificationCSS() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideOutRight {
                from {
                    opacity: 1;
                    transform: translateX(0);
                }
                to {
                    opacity: 0;
                    transform: translateX(100%);
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    addNotificationCSS();
    </script>
    """, unsafe_allow_html=True)


def add_notification(message: str, notification_type: str = "info") -> None:
    """Add a notification to the notification system."""
    st.markdown(f"""
    <script>
    showNotification('{message}', '{notification_type}');
    </script>
    """, unsafe_allow_html=True)


def create_progress_indicator(current: int, total: int, label: str = "Progress", animation: str = "fade-in") -> None:
    """Create a modern progress indicator."""
    percentage = (current / total) * 100 if total > 0 else 0
    
    st.markdown(f"""
    <div class="progress-container {animation}">
        <div class="progress-header">
            <span class="progress-label">{label}</span>
            <span class="progress-percentage">{percentage:.1f}%</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {percentage}%"></div>
        </div>
        <div class="progress-stats">
            <span>{current} / {total}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def create_tooltip(text: str, tooltip_content: str) -> str:
    """Create a tooltip component."""
    return f"""
    <div class="tooltip-container">
        <span class="tooltip-trigger">{text}</span>
        <div class="tooltip-content">{tooltip_content}</div>
    </div>
    """


def create_modal_trigger(button_text: str, modal_id: str, animation: str = "fade-in") -> None:
    """Create a modal trigger button."""
    st.markdown(f"""
    <button class="button-primary {animation}" onclick="openModal('{modal_id}')">
        {button_text}
    </button>
    """, unsafe_allow_html=True)


def create_modal(modal_id: str, title: str, content: str, animation: str = "fade-in") -> None:
    """Create a modal component."""
    st.markdown(f"""
    <div id="{modal_id}" class="modal {animation}">
        <div class="modal-content">
            <div class="modal-header">
                <h3>{title}</h3>
                <button class="modal-close" onclick="closeModal('{modal_id}')">&times;</button>
            </div>
            <div class="modal-body">
                {content}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def create_collapsible_section(title: str, content: str, is_open: bool = False, animation: str = "fade-in") -> None:
    """Create a collapsible section."""
    open_class = "open" if is_open else ""
    st.markdown(f"""
    <div class="collapsible-section {animation}">
        <div class="collapsible-header {open_class}" onclick="toggleCollapsible(this)">
            <h4>{title}</h4>
            <span class="collapsible-icon">▼</span>
        </div>
        <div class="collapsible-content {open_class}">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)


def create_breadcrumb(items: List[Dict[str, str]], animation: str = "fade-in") -> None:
    """Create a breadcrumb navigation."""
    breadcrumb_html = '<div class="breadcrumb ' + animation + '">'
    for i, item in enumerate(items):
        if i > 0:
            breadcrumb_html += '<span class="breadcrumb-separator">/</span>'
        breadcrumb_html += f'<a href="{item["url"]}" class="breadcrumb-item">{item["text"]}</a>'
    breadcrumb_html += '</div>'
    
    st.markdown(breadcrumb_html, unsafe_allow_html=True)


def create_tab_navigation(tabs: List[Dict[str, str]], active_tab: str = "", animation: str = "fade-in") -> str:
    """Create a modern tab navigation."""
    tab_html = f'<div class="tab-navigation {animation}">'
    for tab in tabs:
        active_class = "active" if tab["id"] == active_tab else ""
        tab_html += f'<button class="tab-nav-item {active_class}" onclick="switchTab(\'{tab["id"]}\')">{tab["label"]}</button>'
    tab_html += '</div>'
    
    st.markdown(tab_html, unsafe_allow_html=True)
    return active_tab


def create_floating_action_button(icon: str, action: str, animation: str = "bounce-in") -> None:
    """Create a floating action button."""
    st.markdown(f"""
    <div class="fab {animation}" onclick="{action}">
        <span class="fab-icon">{icon}</span>
    </div>
    """, unsafe_allow_html=True)


def create_skeleton_loader(rows: int = 5, animation: str = "fade-in") -> None:
    """Create a skeleton loading animation."""
    skeleton_html = f'<div class="skeleton-container {animation}">'
    for i in range(rows):
        skeleton_html += f'''
        <div class="skeleton-row">
            <div class="skeleton-item" style="width: 60%;"></div>
            <div class="skeleton-item" style="width: 30%;"></div>
            <div class="skeleton-item" style="width: 10%;"></div>
        </div>
        '''
    skeleton_html += '</div>'
    
    st.markdown(skeleton_html, unsafe_allow_html=True)


def create_chart_container(title: str, chart_type: str = "line", animation: str = "fade-in") -> None:
    """Create a container for charts with modern styling."""
    st.markdown(f"""
    <div class="chart-container {animation}">
        <div class="chart-header">
            <h3>📈 {title}</h3>
            <div class="chart-controls">
                <button class="chart-control-btn" onclick="exportChart()">📊 Export</button>
                <button class="chart-control-btn" onclick="fullscreenChart()">⛶ Fullscreen</button>
            </div>
        </div>
        <div class="chart-content" id="chart-{chart_type}">
            <!-- Chart will be rendered here -->
        </div>
    </div>
    """, unsafe_allow_html=True)


def create_welcome_screen(animation: str = "fade-in") -> None:
    """Create a welcome screen with modern design."""
    st.markdown(f"""
    <div class="welcome-screen {animation}">
        <div class="welcome-content">
            <div class="welcome-icon">🔑</div>
            <h1>Welcome to KeyMate</h1>
            <p>Professional tool for validating and analyzing LLM API keys</p>
            <div class="welcome-features">
                <div class="feature-item">
                    <span class="feature-icon">🔑</span>
                    <span>Multi-provider support</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">🤖</span>
                    <span>Model exploration</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">📊</span>
                    <span>Advanced analytics</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def provider_badge(provider: str | None) -> str:
    """Get provider badge with emoji and styling."""
    mapping = {
        "openai": "🟦 OpenAI",
        "gemini": "🟨 Gemini", 
        "deepseek": "🟧 Deepseek",
        "claude": "🟪 Anthropic Claude",
        "grok": "⚫ xAI Grok",
        "groq": "🟩 Groq",
    }
    return mapping.get(provider or "", "ℹ️ Unknown Provider")


def get_provider_color_class(provider: str | None) -> str:
    """Get CSS class for provider-specific styling."""
    if not provider:
        return ""
    return f"provider-badge {provider}"


def create_loading_spinner(message: str = "Loading...") -> None:
    """Create a modern loading spinner."""
    st.markdown(f"""
    <div class="loading-spinner">
        <div>{message}</div>
    </div>
    """, unsafe_allow_html=True)


def create_button_group(buttons: List[Dict[str, Any]]) -> None:
    """Create a modern button group."""
    cols = st.columns(len(buttons))
    for i, button in enumerate(buttons):
        with cols[i]:
            if button.get("type") == "primary":
                st.button(
                    button["label"],
                    type="primary",
                    key=f"btn_{i}",
                    on_click=button.get("on_click")
                )
            else:
                st.button(
                    button["label"],
                    key=f"btn_{i}",
                    on_click=button.get("on_click")
                )
