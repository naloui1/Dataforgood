"""UI components for the cultural map application."""

import streamlit as st
from streamlit_folium import folium_static


def setup_page():
    """Setup the page configuration."""
    st.set_page_config(layout="wide", page_title="Carte Culturelle")

    # Custom CSS to adjust the layout
    st.markdown(
        """
        <style>
        /* Remove ALL possible padding and margins */
        * {
            margin: 0 !important;
            padding: 0 !important;
            box-sizing: border-box !important;
        }

        /* Remove header completely */
        header {display: none !important;}
        
        /* Reset base styles */
        .stApp {
            position: absolute !important;
            inset: 0 !important;
            overflow: hidden !important;
        }

        /* Sidebar styles */
        [data-testid="stSidebar"] {
            position: fixed !important;
            left: 0 !important;
            top: 0 !important;
            height: 100vh !important;
            width: 860px !important;
            transform: none !important;
            transition: transform 0.3s ease-in-out !important;
            background-color: rgb(240, 242, 246) !important;
            z-index: 1000 !important;
        }

        [data-testid="stSidebar"] > div {
            height: 100vh !important;
            width: 860px !important;
            padding: 2rem !important;
            background-color: rgb(240, 242, 246) !important;
        }

        /* Hide all buttons in the sidebar */
        [data-testid="stSidebar"] button {
            display: none !important;
        }

        /* Show only the main collapse button */
        [data-testid="stSidebar"] > button[kind="secondary"] {
            display: flex !important;
            position: absolute !important;
            left: 860px !important;
            top: 0 !important;
            border-top-left-radius: 0 !important;
            border-bottom-left-radius: 0 !important;
        }

        /* Hide navigation section */
        section[data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* Collapsed sidebar */
        [data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(-860px) !important;
        }

        /* Main content area */
        .main .block-container {
            position: fixed !important;
            inset: 0 !important;
            margin: 0 !important;
            max-width: none !important;
            width: 100vw !important;
            transition: margin-left 0.3s ease-in-out !important;
        }

        /* Main content when sidebar is expanded */
        [data-testid="stSidebar"][aria-expanded="true"] + .main .block-container {
            margin-left: 860px !important;
            width: calc(100vw - 860px) !important;
        }

        /* Map container */
        div.element-container:has(iframe) {
            position: absolute !important;
            inset: 0 !important;
            height: 100vh !important;
            width: 100% !important;
        }

        /* Map iframe */
        iframe {
            position: absolute !important;
            inset: 0 !important;
            width: 100% !important;
            height: 100% !important;
            border: none !important;
            display: block !important;
        }

        /* Improved Sidebar Components Styling */
        .stSelectbox, .stMultiSelect {
            max-width: 780px !important;
            margin: 20px auto !important;
            padding: 10px !important;
            background: white !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }

        /* Center labels and add spacing */
        .stSelectbox label, .stMultiSelect label {
            text-align: center !important;
            display: block !important;
            margin-bottom: 12px !important;
            font-weight: 700 !important;
            font-size: 1.2em !important;
            color: #1f2937 !important;
        }

        /* Style multiselect options - Categories */
        .categories-filter [data-baseweb="tag"] {
            background-color: #3b82f6 !important;
            border-radius: 4px !important;
            margin: 2px !important;
            padding: 2px 8px !important;
        }

        /* Style multiselect options - Types */
        .types-filter [data-baseweb="tag"] {
            background-color: #10b981 !important;
            border-radius: 4px !important;
            margin: 2px !important;
            padding: 2px 8px !important;
        }

        /* Style commune select */
        .commune-filter .stSelectbox {
            border: 2px solid #8b5cf6 !important;
        }

        /* Chat message styling */
        .stChatMessage {
            max-width: 780px !important;
            margin: 10px 30px !important;
            padding: 15px !important;
            border-radius: 8px !important;
            background: white !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }

        /* Chat input container */
        .stChatInputContainer {
            max-width: 780px !important;
            padding: 15px 30px !important;
            background: white !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
            margin: 20px auto !important;
        }

        /* Configuration expander styling */
        .streamlit-expanderHeader {
            background-color: #f3f4f6 !important;
            border-radius: 8px !important;
            padding: 10px 15px !important;
            margin: 10px 0 !important;
            font-weight: 600 !important;
        }

        /* Title styling */
        .sidebar .stTitle {
            text-align: center !important;
            color: #1f2937 !important;
            font-size: 28px !important;
            font-weight: 700 !important;
            margin: 20px 0 !important;
            padding: 10px !important;
        }

        /* Subheader styling */
        .sidebar .stSubheader {
            text-align: center !important;
            color: #4b5563 !important;
            font-size: 20px !important;
            font-weight: 600 !important;
            margin: 15px 0 !important;
            padding: 5px !important;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Remove ALL possible padding */
        .main > div:first-child,
        .main > div > div:first-child,
        .element-container,
        .stMarkdown,
        .stMarkdown > div:first-child {
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Force full viewport usage */
        html, body {
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            width: 100vw !important;
            height: 100vh !important;
        }

        /* Override Streamlit's default padding */
        .css-1d391kg, .css-1a1fmpi {
            padding: 0 !important;
        }

        /* Ensure map container takes full size */
        .element-container div[data-testid="column"] {
            width: 100% !important;
            padding: 0 !important;
        }

        /* Remove any potential gaps */
        .stApp > .main {
            gap: 0 !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )


def create_sidebar(data, chat_placeholder):
    """Create the sidebar with filters and chat interface."""
    with st.sidebar:
        st.title("Filtres & Chat")

        # Create two columns for filters
        col1, col2 = st.columns(2)

        selected_categories = None
        selected_types = None
        selected_commune = None

        with col1:
            # Categories filter with color coding
            st.markdown('<div class="categories-filter">', unsafe_allow_html=True)
            categories = sorted(data["categorie"].unique())
            selected_categories = st.multiselect(
                "Catégories",
                options=categories,
                default=categories,
                help="Sélectionnez une ou plusieurs catégories",
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            # Types filter with color coding
            st.markdown('<div class="types-filter">', unsafe_allow_html=True)
            types = sorted(data["type_infrastructure"].unique())
            selected_types = st.multiselect(
                "Types d'infrastructure",
                options=types,
                default=types,
                help="Sélectionnez un ou plusieurs types",
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # Commune filter (full width)
        st.markdown('<div class="commune-filter">', unsafe_allow_html=True)
        communes = sorted(data["nom_commune"].unique())
        selected_commune = st.selectbox(
            "Commune",
            options=[""] + communes,
            format_func=lambda x: "Toutes les communes" if x == "" else x,
            help="Sélectionnez une commune spécifique",
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Add some space before the chat interface
        st.markdown(
            """<hr style='margin: 30px 0 !important;'>""", unsafe_allow_html=True
        )
        st.subheader("Chat Assistant")

        # Move chat interface to sidebar
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Posez votre question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Assistant response
            with st.chat_message("assistant"):
                message = chat_placeholder(prompt)
                st.session_state.messages.append(
                    {"role": "assistant", "content": message}
                )
                st.markdown(message)

        # Configuration expander at the bottom
        st.markdown(
            """<hr style='margin: 30px 0 !important;'>""", unsafe_allow_html=True
        )
        with st.expander("⚙️ Configuration"):
            api_key = st.text_input(
                "OpenAI API Key", type="password", key="openai_api_key"
            )
            if api_key:
                st.success("API Key configured successfully!")

        return selected_categories, selected_types, selected_commune


def show_map(map_object):
    """Display the map in the main area."""
    # Display the map with fixed dimensions
    folium_static(map_object, width=1920, height=1080)
