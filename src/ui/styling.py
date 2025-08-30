"""
Modern CSS Styling for LLM API Key Tester & Analyzer

This module contains all custom CSS styles for creating a professional,
modern interface that can compete with React.js applications.
"""

# Custom CSS for modern UI
CUSTOM_CSS = """
<style>
/* UI Fixes for LLM API Key Tester - Frontend Specialist Improvements */

/* Fix 1: Consistent Spacing System */
:root {
    /* Unified spacing scale */
    --space-1: 0.25rem;   /* 4px */
    --space-2: 0.5rem;    /* 8px */
    --space-3: 0.75rem;   /* 12px */
    --space-4: 1rem;      /* 16px */
    --space-5: 1.25rem;   /* 20px */
    --space-6: 1.5rem;    /* 24px */
    --space-8: 2rem;      /* 32px */
    --space-10: 2.5rem;   /* 40px */
    --space-12: 3rem;     /* 48px */
    --space-16: 4rem;     /* 64px */
    
    /* Consistent color palette */
    --primary-50: #eff6ff;
    --primary-100: #dbeafe;
    --primary-500: #3b82f6;
    --primary-600: #2563eb;
    --primary-700: #1d4ed8;
    
    --gray-50: #f9fafb;
    --gray-100: #f3f4f6;
    --gray-200: #e5e7eb;
    --gray-300: #d1d5db;
    --gray-400: #9ca3af;
    --gray-500: #6b7280;
    --gray-600: #4b5563;
    --gray-700: #374151;
    --gray-800: #1f2937;
    --gray-900: #111827;
    
    --success-500: #10b981;
    --error-500: #ef4444;
    --warning-500: #f59e0b;
    
    /* Typography scale */
    --text-xs: 0.75rem;    /* 12px */
    --text-sm: 0.875rem;   /* 14px */
    --text-base: 1rem;     /* 16px */
    --text-lg: 1.125rem;   /* 18px */
    --text-xl: 1.25rem;    /* 20px */
    --text-2xl: 1.5rem;    /* 24px */
    --text-3xl: 1.875rem;  /* 30px */
    --text-4xl: 2.25rem;   /* 36px */
    
    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
    
    /* Border radius */
    --radius-sm: 0.25rem;
    --radius: 0.375rem;
    --radius-md: 0.5rem;
    --radius-lg: 0.75rem;
    --radius-xl: 1rem;
    --radius-2xl: 1.5rem;
}

/* Fix 2: Global Typography Reset */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: var(--gray-800);
    background: var(--gray-50);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* Fix 3: Consistent Header Styling */
.main-header {
    background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 100%);
    padding: var(--space-12) var(--space-4);
    margin: calc(-1 * var(--space-4)) calc(-1 * var(--space-4)) var(--space-8) calc(-1 * var(--space-4));
    border-radius: 0 0 var(--radius-2xl) var(--radius-2xl);
    color: white;
    text-align: center;
    box-shadow: var(--shadow-xl);
}

.main-header h1 {
    font-size: var(--text-4xl);
    font-weight: 800;
    margin-bottom: var(--space-4);
    line-height: 1.2;
    letter-spacing: -0.025em;
}

.main-header p {
    font-size: var(--text-lg);
    opacity: 0.9;
    max-width: 600px;
    margin: 0 auto;
    font-weight: 400;
}

/* Fix 4: Consistent Card Styling */
.card-container {
    background: white;
    border-radius: var(--radius-xl);
    padding: var(--space-6);
    margin-bottom: var(--space-6);
    box-shadow: var(--shadow);
    border: 1px solid var(--gray-200);
    transition: all 0.2s ease;
}

.card-container:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-1px);
}

.card-container h3 {
    font-size: var(--text-xl);
    font-weight: 700;
    color: var(--gray-800);
    margin-bottom: var(--space-4);
    display: flex;
    align-items: center;
    gap: var(--space-2);
    line-height: 1.3;
}

/* Fix 5: Consistent Metric Cards */
.metric-card {
    background: white;
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    box-shadow: var(--shadow);
    border: 1px solid var(--gray-200);
    text-align: center;
    transition: all 0.2s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.metric-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}

.metric-card h4 {
    font-size: var(--text-sm);
    font-weight: 600;
    color: var(--gray-500);
    margin-bottom: var(--space-3);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.metric-card .value {
    font-size: var(--text-3xl);
    font-weight: 800;
    color: var(--gray-800);
    line-height: 1.2;
}

/* Fix 6: Consistent Grid Layout */
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--space-6);
    margin: var(--space-6) 0;
}

/* Fix 7: Consistent Button Styling */
.button-primary {
    background: var(--primary-600);
    color: white;
    border: none;
    padding: var(--space-3) var(--space-6);
    border-radius: var(--radius-lg);
    font-size: var(--text-base);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: var(--shadow-sm);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
}

.button-primary:hover {
    background: var(--primary-700);
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
    color: white;
    text-decoration: none;
}

.button-secondary {
    background: white;
    color: var(--primary-600);
    border: 2px solid var(--primary-600);
    padding: var(--space-3) var(--space-6);
    border-radius: var(--radius-lg);
    font-size: var(--text-base);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: var(--shadow-sm);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
}

.button-secondary:hover {
    background: var(--primary-600);
    color: white;
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
    text-decoration: none;
}

/* Fix 8: Consistent Input Styling */
.search-container input {
    width: 100%;
    padding: var(--space-3) var(--space-4);
    border: 2px solid var(--gray-300);
    border-radius: var(--radius-lg);
    font-size: var(--text-base);
    transition: all 0.2s ease;
    background: white;
    color: var(--gray-800);
}

.search-container input:focus {
    outline: none;
    border-color: var(--primary-500);
    box-shadow: 0 0 0 3px rgb(59 130 246 / 0.1);
}

.search-container input::placeholder {
    color: var(--gray-400);
}

/* Fix 9: Consistent Status Badges */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-2) var(--space-4);
    border-radius: 9999px;
    font-size: var(--text-sm);
    font-weight: 600;
    box-shadow: var(--shadow-sm);
}

.status-badge.success {
    background: var(--success-500);
    color: white;
}

.status-badge.error {
    background: var(--error-500);
    color: white;
}

.status-badge.warning {
    background: var(--warning-500);
    color: white;
}

/* Fix 10: Consistent Provider Badges */
.provider-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-2) var(--space-4);
    border-radius: 9999px;
    font-size: var(--text-sm);
    font-weight: 600;
    background: var(--primary-600);
    color: white;
    box-shadow: var(--shadow-sm);
    transition: all 0.2s ease;
}

.provider-badge:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

/* Fix 11: Consistent Model Cards */
.model-card {
    background: white;
    border-radius: var(--radius-lg);
    padding: var(--space-4);
    margin: var(--space-2) 0;
    border: 1px solid var(--gray-200);
    transition: all 0.2s ease;
    cursor: pointer;
}

.model-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
    border-color: var(--primary-500);
}

.model-card.selected {
    background: var(--primary-600);
    color: white;
    border-color: var(--primary-600);
}

.model-card h4 {
    font-size: var(--text-lg);
    font-weight: 600;
    margin-bottom: var(--space-2);
}

.model-card p {
    font-size: var(--text-sm);
    color: var(--gray-600);
    margin-bottom: var(--space-1);
}

.model-card.selected p {
    color: rgba(255, 255, 255, 0.8);
}

/* Fix 12: Consistent Flex Layout */
.flex-container {
    display: flex;
    gap: var(--space-4);
    align-items: center;
    flex-wrap: wrap;
}

/* Fix 13: Streamlit Specific Overrides */
.stButton > button {
    border-radius: var(--radius-lg) !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-md) !important;
}

.stTextInput > div > div > input {
    border-radius: var(--radius-lg) !important;
    border: 2px solid var(--gray-300) !important;
    transition: all 0.2s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--primary-500) !important;
    box-shadow: 0 0 0 3px rgb(59 130 246 / 0.1) !important;
}

.stSelectbox > div > div > div {
    border-radius: var(--radius-lg) !important;
    border: 2px solid var(--gray-300) !important;
}

.stDataFrame {
    border-radius: var(--radius-lg) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow) !important;
}

/* Fix 14: Consistent Spacing for Streamlit Elements */
.stMarkdown {
    margin-bottom: var(--space-4) !important;
}

.stColumns {
    gap: var(--space-4) !important;
}

/* Fix 15: Main Container Spacing */
.main .block-container {
    padding-top: var(--space-6) !important;
    padding-bottom: var(--space-6) !important;
    max-width: 1200px !important;
}

/* Fix 16: Responsive Design */
@media (max-width: 768px) {
    .main-header h1 {
        font-size: var(--text-3xl);
    }
    
    .main-header p {
        font-size: var(--text-base);
    }
    
    .card-container {
        padding: var(--space-4);
        margin-bottom: var(--space-4);
    }
    
    .grid-container {
        grid-template-columns: 1fr;
        gap: var(--space-4);
    }
    
    .flex-container {
        flex-direction: column;
        gap: var(--space-3);
    }
    
    .metric-card {
        padding: var(--space-4);
    }
    
    .metric-card .value {
        font-size: var(--text-2xl);
    }
    
    .button-primary,
    .button-secondary {
        width: 100%;
        justify-content: center;
    }
}

/* Fix 17: Animation Classes */
.fade-in {
    animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.slide-in-left {
    animation: slideInLeft 0.3s ease-out;
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.bounce-in {
    animation: bounceIn 0.5s ease-out;
}

@keyframes bounceIn {
    0% {
        opacity: 0;
        transform: scale(0.9);
    }
    50% {
        opacity: 1;
        transform: scale(1.05);
    }
    100% {
        opacity: 1;
        transform: scale(1);
    }
}

/* Fix 18: Welcome Screen */
.welcome-screen {
    background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 100%);
    border-radius: var(--radius-xl);
    padding: var(--space-12);
    text-align: center;
    color: white;
    margin: var(--space-6) 0;
    box-shadow: var(--shadow-xl);
}

.welcome-icon {
    font-size: 3rem;
    margin-bottom: var(--space-6);
}

.welcome-content h1 {
    font-size: var(--text-4xl);
    font-weight: 800;
    margin-bottom: var(--space-4);
    line-height: 1.2;
}

.welcome-content p {
    font-size: var(--text-lg);
    opacity: 0.9;
    margin-bottom: var(--space-8);
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

.welcome-features {
    display: flex;
    justify-content: center;
    gap: var(--space-8);
    flex-wrap: wrap;
}

.feature-item {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    font-size: var(--text-base);
}

.feature-icon {
    font-size: var(--text-xl);
}

/* Fix 19: Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--gray-100);
    border-radius: var(--radius-sm);
}

::-webkit-scrollbar-thumb {
    background: var(--gray-400);
    border-radius: var(--radius-sm);
}

::-webkit-scrollbar-thumb:hover {
    background: var(--gray-500);
}
</style>
"""

def inject_custom_css():
    """Inject custom CSS for modern UI styling."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
