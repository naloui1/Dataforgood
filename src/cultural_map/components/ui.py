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
        /* Reset base styles */
        .stApp {
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
        }

        /* Sidebar styles */
        [data-testid="stSidebar"] {
            position: fixed !important;
            left: 0 !important;
            top: 0 !important;
            height: 100vh !important;
            width: 860px !important;
            transition: transform 0.3s ease-in-out !important;
            background-color: rgb(240, 242, 246) !important;
        }

        [data-testid="stSidebar"] > div {
            height: 100vh !important;
            width: 860px !important;
            padding: 2rem !important;
            background-color: rgb(240, 242, 246) !important;
        }

        /* Collapsed sidebar */
        [data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(-860px) !important;
        }

        /* Main content area */
        .main .block-container {
            margin: 0 !important;
            padding: 0 !important;
            max-width: none !important;
            width: calc(100% - 860px) !important;
            margin-left: 860px !important;
            transition: margin-left 0.3s ease-in-out, width 0.3s ease-in-out !important;
            height: 100vh !important;
            overflow: hidden !important;
        }

        /* Main content when sidebar is collapsed */
        [data-testid="stSidebar"][aria-expanded="false"] + .main .block-container {
            margin-left: 0 !important;
            width: 100% !important;
        }

        /* Map container */
        div.element-container:has(iframe) {
            height: 100vh !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Map iframe */
        iframe {
            width: 100% !important;
            height: 100% !important;
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Sidebar components */
        .stSelectbox, .stMultiSelect {
            max-width: 780px !important;
            margin: 0 auto !important;
        }

        .stChatMessage {
            max-width: 780px !important;
            margin: 0 30px !important;
        }

        .stChatInputContainer {
            max-width: 780px !important;
            padding: 0 30px !important;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Fix stApp container */
        .stApp > header {
            position: fixed !important;
            top: 0 !important;
            right: 0 !important;
            left: 0 !important;
            height: 0 !important;
            background: transparent !important;
            z-index: 999999 !important;
        }

        .stApp > .main {
            margin-top: 0 !important;
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
            # Categories filter
            categories = sorted(data["categorie"].unique())
            selected_categories = st.multiselect(
                "Catégories",
                options=categories,
                default=categories,
            )

        with col2:
            # Types filter
            types = sorted(data["type_infrastructure"].unique())
            selected_types = st.multiselect(
                "Types d'infrastructure",
                options=types,
                default=types,
            )

        # Commune filter (full width)
        communes = sorted(data["nom_commune"].unique())
        selected_commune = st.selectbox(
            "Commune",
            options=[""] + communes,
            format_func=lambda x: "Toutes les communes" if x == "" else x,
        )

        # Add some space before the chat interface
        st.markdown("---")
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

        return selected_categories, selected_types, selected_commune


def show_map(map_object):
    """Display the map in the main area."""
    # Display the map with dynamic height calculation
    folium_static(map_object, width=1920, height=1080)
