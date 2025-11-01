import streamlit as st

def apply_custom_css():
    """Applies a professional dark theme to the Streamlit app."""
    st.markdown("""
        <style>
            /* Base font and background for dark theme */
            html, body, [class*="st-"] {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
                color: #EAEAEA; /* Light gray text for readability */
            }
            .stApp {
                background-color: #1E1E1E; /* Dark background */
            }

            /* Main content area styling */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                padding-left: 3rem;
                padding-right: 3rem;
            }

            /* Card effect for containers in dark mode */
            [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] > [data-testid="stVerticalBlock"] {
                background-color: #2D2D2D; /* Slightly lighter dark for cards */
                border: 1px solid #444444;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.2);
            }

            /* Styling for headers and subheaders */
            h1, h2, h3 {
                color: #FFFFFF; /* White for main headers */
            }

            /* Button styling for dark mode */
            .stButton > button {
                border-radius: 8px;
                border: none;
                padding: 0.8em 1.5em;
                font-size: 1em;
                font-weight: 600;
                color: #FFFFFF;
                background-color: #007AFF; /* Apple's vibrant blue */
                transition: all 0.2s ease-in-out;
            }
            .stButton > button:hover {
                background-color: #0056B3; /* Darker blue on hover */
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 122, 255, 0.4);
            }
            .stButton > button:disabled {
                background-color: #444444;
                color: #AAAAAA;
                opacity: 0.7;
                cursor: not-allowed;
            }
            
            /* Ensure dividers are visible */
            hr {
                background-color: #444444 !important;
            }
        </style>
    """, unsafe_allow_html=True)

def show_header():
    """Displays a professional header optimized for dark mode."""
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 style="font-size: 2.5rem;"><span style="font-size: 3.5rem;">🎓</span> Smart Learn</h1>
            <p style="font-size: 1.2rem; color: #AAAAAA; font-weight: 500;">Your personal AI tutor for mastering complex subjects</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.divider()