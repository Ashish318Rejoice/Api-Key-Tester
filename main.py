#!/usr/bin/env python3
"""
🔑 KeyMate - Main Application

This is the main entry point for the professional, modern Streamlit application
that provides a comprehensive interface for validating LLM API keys and analyzing models.

Features:
- Professional UI with modern design
- Multi-provider support (OpenAI, Gemini, Claude, Deepseek, Grok, Groq)
- Real-time validation and model exploration
- Advanced filtering and search capabilities
- Responsive design for all devices

Run this file to launch the application:
    streamlit run app.py
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st

# Import our modular components
from src.ui import (
    render_modern_header, create_modern_footer, get_state, provider_badge,
    create_metric_card, create_status_badge, create_data_table, create_advanced_filters,
    create_quick_actions, create_sidebar_controls, create_notification_system,
    add_notification, get_provider_color_class, create_model_details_panel
)
from src.core import LLMKeyTester
from src.config import get_config, is_demo_mode


def clear_models_state():
    """Clear models-related state to trigger refresh."""
    if "models_payload" in st.session_state:
        st.session_state.models_payload = None
    if "models_table" in st.session_state:
        st.session_state.models_table = None
    if "selected_model" in st.session_state:
        st.session_state.selected_model = None


def initialize_state():
    """Initialize application state."""
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "provider" not in st.session_state:
        st.session_state.provider = ""
    if "is_valid" not in st.session_state:
        st.session_state.is_valid = None
    if "models_payload" not in st.session_state:
        st.session_state.models_payload = None
    if "models_table" not in st.session_state:
        st.session_state.models_table = None
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = None
    if "account_status" not in st.session_state:
        st.session_state.account_status = None
    if "status_msg" not in st.session_state:
        st.session_state.status_msg = None
    if "raw_model_json" not in st.session_state:
        st.session_state.raw_model_json = None
    if "show_raw_json" not in st.session_state:
        st.session_state.show_raw_json = False
    if "_last_api_key" not in st.session_state:
        st.session_state._last_api_key = ""
    if "_last_provider" not in st.session_state:
        st.session_state._last_provider = ""


def mask_key(key: str) -> str:
    """Mask API key for display."""
    if not key:
        return ""
    if len(key) <= 6:
        return key[0:1] + "*" * (len(key) - 2) + key[-1:]
    return f"{key[:3]}…{key[-2:]}"


def normalize_models_for_table(provider: str, payload: dict) -> pd.DataFrame:
    """Convert provider payloads into a unified table for display."""
    rows: List[Dict[str, Any]] = []
    
    # Provider-specific structures
    if provider == "openai":
        for mid in payload.get("all_models", []) or []:
            model_type = "Embedding" if "embedding" in (mid or "").lower() else "Chat"
            rows.append({
                "Model ID": mid,
                "Type": model_type,
                "Context Length": None,
                "Created": None,
                "Status": "Available",
            })
    elif provider == "gemini":
        for name in payload.get("all_models", []) or []:
            model_type = "Embedding" if "embedding" in (name or "").lower() else "Chat"
            rows.append({
                "Model ID": name,
                "Type": model_type,
                "Context Length": None,
                "Created": None,
                "Status": "Available",
            })
    else:
        # Generic fallback
        for mid in payload.get("all_models", []) or []:
            rows.append({
                "Model ID": mid,
                "Type": "Unknown",
                "Context Length": None,
                "Created": None,
                "Status": "Available",
            })

    df = pd.DataFrame(rows, columns=["Model ID", "Type", "Context Length", "Created", "Status"])
    # Add provider column
    df["Provider"] = provider
    # Reorder columns to put Provider first
    df = df[["Provider", "Model ID", "Type", "Context Length", "Created", "Status"]]
    return df.reset_index(drop=True)


def create_dashboard_metrics(state: Dict[str, Any]) -> None:
    """Create dashboard metrics cards."""
    st.markdown("### 📊 Dashboard Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_models = len(state.get("models_table", pd.DataFrame())) if state.get("models_table") is not None else 0
        create_metric_card("Total Models", str(total_models), "🤖")
    
    with col2:
        provider = state.get("provider", "Unknown")
        create_metric_card("Provider", provider_badge(provider), "🏢")
    
    with col3:
        status = "Valid" if state.get("is_valid") else "Invalid" if state.get("is_valid") is False else "Not Tested"
        create_metric_card("API Status", status, "🔑")
    
    with col4:
        selected_model = state.get("selected_model", "None")
        if selected_model and selected_model != "None":
            display_model = selected_model[:20] + "..." if len(selected_model) > 20 else selected_model
        else:
            display_model = "None"
        create_metric_card("Selected Model", display_model, "🎯")
    
    # Quick refresh button if API key changed
    current_api_key = state.get("api_key", "")
    last_api_key = state.get("_last_api_key", "")
    if current_api_key != last_api_key and state.get("is_valid"):
        st.warning("🔄 **API Key Changed**: Click the 'Refresh Models' button in the Models section to load new models.")


def render_validation_section(state: Dict[str, Any], tester: LLMKeyTester) -> None:
    """Render the API key validation section."""
    st.markdown("## 🔑 API Key Validation")
    
    # API Key input card
    with st.container():
        st.markdown("""
        <div class="card-container">
            <h3>🔐 Enter API Key</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            api_key = st.text_input(
                "API Key",
                value=state.get("api_key") or "",
                type="password",
                placeholder="sk-... or your API key",
                key="api_key_input"
            )
        with col2:
            validate_clicked = st.button("🔍 Validate", type="primary", use_container_width=True)
        
        # Show masked key if exists
        if state.get("api_key"):
            st.caption(f"Current key: {mask_key(state['api_key'])}")

    # Validation logic
    if validate_clicked and api_key:
        state["api_key"] = api_key
        with st.status("Validating key…", expanded=False) as status:
            try:
                prov, ok, msg, info = tester.detect_provider(api_key)
                state["provider"] = prov
                state["is_valid"] = ok
                state["status_msg"] = msg
                
                if ok and prov:
                    status.update(label="✅ API Key Valid", state="complete")
                    add_notification(f"Successfully connected to {provider_badge(prov)}", "success")
                else:
                    status.update(label="❌ Validation Failed", state="error")
                    add_notification(msg or "Invalid or unauthorized key", "error")
            except Exception as e:
                status.update(label="❌ Validation Error", state="error")
                add_notification(f"Validation error: {str(e)}", "error")

    # Status display
    if state.get("is_valid") is True and state.get("provider"):
        # Check if models need to be refreshed
        current_api_key = state.get("api_key", "")
        last_api_key = state.get("_last_api_key", "")
        needs_refresh = current_api_key != last_api_key
        
        if needs_refresh:
            create_status_badge("🔄", f"API Key Valid — Connected to {provider_badge(state['provider'])} (Models need refresh)", "warning")
            st.info("💡 **Tip**: Your API key has changed. Models will be automatically refreshed in the Models section.")
        else:
            create_status_badge("✅", f"API Key Valid — Successfully connected to {provider_badge(state['provider'])}", "success")
    elif state.get("is_valid") is False:
        create_status_badge("❌", state.get("status_msg") or "Invalid or unauthorized key", "error")

    # Provider information
    if state.get("provider"):
        with st.container():
            st.markdown("""
            <div class="card-container">
                <h3>🏢 Provider Information</h3>
            </div>
            """, unsafe_allow_html=True)
            
            provider_info = provider_badge(state["provider"])
            st.markdown(f"""
            <div class="{get_provider_color_class(state['provider'])}">
                {provider_info}
            </div>
            """, unsafe_allow_html=True)


def render_models_section(state: Dict[str, Any], tester: LLMKeyTester) -> None:
    """Render the models listing and selection section."""
    if not (state.get("is_valid") and state.get("provider") and state.get("api_key")):
        return
    
    # Header with refresh button
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.markdown("## 🤖 Available Models")
    with col2:
        if st.button("🔄 Refresh Models", type="secondary", use_container_width=True, key="refresh_models_btn"):
            state["models_payload"] = None
            state["models_table"] = None
            state["selected_model"] = None
            st.rerun()
    
    # Check if API key or provider has changed (need to refresh models)
    current_api_key = state.get("api_key", "")
    current_provider = state.get("provider", "")
    last_api_key = state.get("_last_api_key", "")
    last_provider = state.get("_last_provider", "")
    
    # Clear models if API key or provider changed
    if current_api_key != last_api_key or current_provider != last_provider:
        state["models_payload"] = None
        state["models_table"] = None
        state["selected_model"] = None
        state["_last_api_key"] = current_api_key
        state["_last_provider"] = current_provider
        add_notification(f"API key changed to {provider_badge(current_provider)}. Refreshing models...", "info")
    
    # Fetch models if not already loaded
    if state.get("models_payload") is None:
        # Show loading status
        with st.status("🔄 Fetching models from API...", expanded=True) as status:
            try:
                info = tester.get_detailed_info(state["provider"], state["api_key"])
                if "error" in info:
                    status.update(label="❌ Error fetching models", state="error")
                    st.error(info["error"])
                    add_notification(f"Error fetching models: {info['error']}", "error")
                else:
                    state["account_status"] = info.get("account_status")
                    state["models_payload"] = info.get("model_details")
                    state["models_table"] = normalize_models_for_table(
                        state["provider"], 
                        info.get("model_details") or {}
                    )
                    model_count = len(state["models_table"])
                    status.update(label=f"✅ Successfully loaded {model_count} models", state="complete")
                    add_notification(f"Successfully loaded {model_count} models from {provider_badge(state['provider'])}", "success")
            except Exception as e:
                status.update(label="❌ Error fetching models", state="error")
                st.error(f"Error fetching models: {str(e)}")
                add_notification(f"Error fetching models: {str(e)}", "error")

    # Display models table
    if state.get("models_table") is not None:
        # Extract providers and model types for filters
        df = state["models_table"].copy()
        providers = df["Provider"].unique().tolist() if "Provider" in df.columns else []
        model_types = df["Type"].unique().tolist() if "Type" in df.columns else []
        
        # Advanced filters
        filters = create_advanced_filters(providers, model_types)
        
        # Search functionality
        search_query = st.text_input("🔍 Search models...", key="model_search")
        
        # Filter and display data
        df = state["models_table"].copy()
        
        # Apply search filter
        if search_query:
            mask = df["Model ID"].str.contains(search_query, case=False, na=False)
            df = df[mask]
        
        # Apply provider filter
        if filters["provider"] != "All":
            df = df[df["Provider"] == filters["provider"]]
        
        # Apply type filter
        if filters["model_type"] != "All":
            df = df[df["Type"] == filters["model_type"]]
        
        # Apply context length filter
        if filters["context_min"] > 0:
            df = df[df["Context Length"] >= filters["context_min"]]
        
        # Sort data
        ascending = filters["sort_order"] == "Ascending"
        if filters["sort_by"] == "Name":
            df = df.sort_values("Model ID", ascending=ascending)
        elif filters["sort_by"] == "Type":
            df = df.sort_values("Type", ascending=ascending)
        elif filters["sort_by"] == "Context Length":
            df = df.sort_values("Context Length", ascending=ascending, na_last=True)
        elif filters["sort_by"] == "Created":
            df = df.sort_values("Created", ascending=ascending, na_last=True)
        
        # Display filtered table
        create_data_table(df, "Models", searchable=False)
        
        # Model selection
        if not df.empty:
            model_ids = df["Model ID"].tolist()
            selected_model = st.selectbox(
                "Select a model for details",
                options=["-"] + model_ids,
                index=0,
                key="model_selection"
            )
            
            if selected_model and selected_model != "-":
                state["selected_model"] = selected_model
                render_model_details(state, tester, selected_model)


def render_model_details(state: Dict[str, Any], tester: LLMKeyTester, model_id: str) -> None:
    """Render detailed model information."""
    st.markdown("## 📊 Model Details")
    
    with st.spinner("Fetching model details…"):
        try:
            model_json = tester.testers[state["provider"]].get_model_info(state["api_key"], model_id)
            state["raw_model_json"] = model_json
            
            if model_json:
                create_model_details_panel(model_json, state["provider"])
                
                # Raw JSON toggle
                if st.toggle("Show Raw JSON", value=state.get("show_raw_json", False)):
                    st.json(model_json, expanded=False)
            else:
                st.warning("No detailed information available for this model.")
                
        except Exception as e:
            st.error(f"Error fetching model details: {str(e)}")
            add_notification(f"Error fetching model details: {str(e)}", "error")


def render_insights_section(state: Dict[str, Any], tester: LLMKeyTester) -> None:
    """Render the model insights section."""
    st.markdown("## 📊 Model Insights")
    
    with st.container():
        st.markdown("""
        <div class="card-container">
            <h3>🔍 Model Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Model ID input
        model_id = st.text_input(
            "Model ID", 
            placeholder="gpt-4o, claude-3-5-sonnet-20241022, etc.",
            key="insights_model_id"
        )
        
        # Quick picks
        quick_picks = st.pills(
            "Quick Picks",
            ["gpt-4o", "claude-3-5-sonnet-20241022", "models/gemini-1.5-pro", "llama-3-70b", "grok-beta"],
            selection_mode="single",
            key="quick_picks"
        )
        
        # Use selected quick pick or entered model ID
        chosen_model = model_id or (quick_picks[0] if quick_picks else "")
        
        if st.button("🔍 Analyze", type="primary") and chosen_model:
            try:
                # Analyze model
                prov = tester.guess_provider_from_model_id(chosen_model)
                parts = tester.parse_model_parts(chosen_model)
                
                st.markdown("### 📋 Parsed Model Information")
                
                # Display parsed information in metric cards
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    create_metric_card("Namespace", parts.get("Namespace", "—"), "🏷️")
                with col2:
                    create_metric_card("Family", parts.get("Family", "—"), "👨‍👩‍👧‍👦")
                with col3:
                    create_metric_card("Version", parts.get("Version", "—"), "📌")
                with col4:
                    create_metric_card("Provider", provider_badge(prov), "🏢")
                
                # Provider badge with styling
                st.markdown("### 🏢 Provider Information")
                provider_info = provider_badge(prov)
                st.markdown(f"""
                <div class="{get_provider_color_class(prov)}">
                    {provider_info}
                </div>
                """, unsafe_allow_html=True)
                
                # Reference capabilities
                st.markdown("### 🎯 Reference Capabilities")
                ref = tester.reference_capabilities(prov)
                if ref:
                    st.json(ref, expanded=False)
                else:
                    st.info("No reference capabilities found for this provider.")
                    
                add_notification(f"Successfully analyzed model: {chosen_model}", "success")
                
            except Exception as e:
                st.error(f"Error analyzing model: {str(e)}")
                add_notification(f"Error analyzing model: {str(e)}", "error")


def render_advanced_analysis_section(state: Dict[str, Any], tester: LLMKeyTester) -> None:
    """Render the advanced analysis section."""
    st.markdown("## 🔬 Advanced Analysis")
    
    with st.container():
        st.markdown("""
        <div class="card-container">
            <h3>📈 Performance Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Advanced analysis features
        st.info("🚧 Advanced analysis features coming soon...")
        
        # Placeholder for future features
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Planned Features")
            st.markdown("""
            - **Performance Benchmarking**: Compare model performance
            - **Cost Analysis**: Estimate API usage costs
            - **Capability Mapping**: Visual model capability comparison
            - **Usage Analytics**: Track API usage patterns
            - **Custom Testing**: Create custom model tests
            """)
        
        with col2:
            st.markdown("### Current Status")
            st.markdown("""
            - ✅ API Key Validation
            - ✅ Model Listing
            - ✅ Model Details
            - ✅ Offline Insights
            - 🚧 Advanced Analysis
            - 🚧 Performance Metrics
            - 🚧 Cost Estimation
            """)


def main() -> None:
    """Main application function."""
    # Initialize state
    initialize_state()
    
    # Initialize
    render_modern_header()
    state = get_state()
    tester = LLMKeyTester()
    
    # Sidebar controls
    controls = create_sidebar_controls()
    
    # Main content area
    with st.container():
        # Notification system
        create_notification_system()
        
        # Dashboard metrics
        create_dashboard_metrics(state)
        
        # Quick actions
        create_quick_actions()
        
        # Main content based on mode
        if controls["mode"] == "Validate & List Models":
            render_validation_section(state, tester)
            render_models_section(state, tester)
        elif controls["mode"] == "Model Insights ":
            render_insights_section(state, tester)
        else:
            render_advanced_analysis_section(state, tester)
    
    # Footer
    create_modern_footer()


if __name__ == "__main__":
    main()
