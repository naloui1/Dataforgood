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
        /* Make sidebar wider with transition */
        [data-testid="stSidebar"] {
            width: 860px !important;
            transition: width 0.3s ease-in-out, margin-left 0.3s ease-in-out !important;
        }
        
        /* Ensure sidebar content width */
        [data-testid="stSidebar"] > div {
            width: 860px !important;
            transition: width 0.3s ease-in-out !important;
        }

        /* When sidebar is collapsed */
        [data-testid="stSidebar"][aria-expanded="false"] {
            margin-left: -860px !important;
        }
        
        /* Adjust main content area */
        .main .block-container {
            max-width: calc(100% - 860px) !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            transition: max-width 0.3s ease-in-out !important;
        }

        /* Adjust main content when sidebar is collapsed */
        [data-testid="stSidebar"][aria-expanded="false"] + .main .block-container {
            max-width: 100% !important;
        }
        
        /* Keep components properly sized for wider sidebar */
        .stSelectbox, .stMultiSelect {
            min-width: 320px !important;
            max-width: 780px !important;
            margin: 0 auto !important;
        }
        
        /* Make chat messages fit in sidebar */
        .stChatMessage {
            max-width: 780px !important;
            margin-right: 30px !important;
            margin-left: 30px !important;
        }
        
        /* Ensure chat input fits */
        .stChatInputContainer {
            max-width: 780px !important;
            padding-right: 30px !important;
            padding-left: 30px !important;
        }
        
        /* Ensure buttons fit */
        .stButton button {
            width: 100%;
            max-width: 320px !important;
            margin: 0 auto !important;
        }

        /* Add some padding to sidebar content */
        .stSidebar .block-container {
            padding: 1.5rem !important;
            width: 860px !important;
            background-color: rgb(240, 242, 246) !important;
        }

        /* Ensure no horizontal overflow */
        .stSidebar [data-testid="stVerticalBlock"] {
            padding-left: 0 !important;
            padding-right: 0 !important;
            width: 100% !important;
        }

        /* Adjust column gaps */
        .row-widget.stRow {
            gap: 1.5rem !important;
        }

        /* Make sidebar collapse button more visible */
        button[kind="header"] {
            background-color: rgb(240, 242, 246) !important;
            transition: background-color 0.3s ease !important;
        }
        button[kind="header"]:hover {
            background-color: rgb(220, 222, 226) !important;
        }

        /* Fix tag container width */
        div[data-testid="stHorizontalBlock"] {
            width: 820px !important;
            flex-wrap: wrap !important;
            gap: 6px !important;
            padding: 0 20px !important;
            margin: 0 auto !important;
        }

        /* Style individual tags */
        div[data-testid="stHorizontalBlock"] > div {
            flex: 0 1 auto !important;
            white-space: nowrap !important;
            margin: 2px !important;
        }

        /* Ensure tag buttons don't overflow */
        div[data-testid="stHorizontalBlock"] button {
            padding: 4px 8px !important;
            font-size: 0.9em !important;
        }

        /* Container for multiselect dropdowns */
        div.stMultiSelect > div {
            max-width: 820px !important;
            margin: 0 auto !important;
        }

        /* Ensure sidebar background extends fully */
        section[data-testid="stSidebar"] > div {
            background-color: rgb(240, 242, 246) !important;
        }

        /* Ensure consistent background color */
        .stSidebar > div:first-child {
            background-color: rgb(240, 242, 246) !important;
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
    # The map will now take the full main area
    st.markdown(
        """
        <style>
        iframe {
            width: 100%;
            min-height: 800px;
            height: calc(100vh - 100px);
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("## Carte des Infrastructures Culturelles")
    st.components.v1.html(map_object._repr_html_(), height=800)
