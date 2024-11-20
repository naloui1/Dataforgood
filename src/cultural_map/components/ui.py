"""UI components for the cultural map application."""

import streamlit as st
from streamlit_folium import folium_static
import plotly.graph_objects as go


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
            width: 100vw !important;
            height: 100vh !important;
        }

        /* Sidebar styles */
        .stSidebar.st-emotion-cache-a27nlo.eczjsme18 {
            position: relative !important;
            user-select: auto !important;
            min-width: 800px !important;
            max-width: 95vw !important;
            height: auto !important;
            box-sizing: border-box !important;
            flex-shrink: 0 !important;
            resize: horizontal !important;
            overflow-x: auto !important;
        }

        /* Ensure parent containers don't restrict width */
        .st-emotion-cache-ue6h4q, 
        .st-emotion-cache-r421ms,
        .st-emotion-cache-10trblm,
        .st-emotion-cache-1dp5vir {
            min-width: 800px !important;
            max-width: 95vw !important;
        }

        [data-testid="stSidebar"] {
            position: fixed !important;
            left: 0 !important;
            top: 0 !important;
            height: 100vh !important;
            min-width: 800px !important;
            max-width: 95vw !important;
            transform: none !important;
            transition: width 0.3s ease-in-out !important;
            background-color: rgb(240, 242, 246) !important;
            z-index: 1000 !important;
            overflow-y: auto !important;
            resize: horizontal !important;
            overflow-x: auto !important;
        }

        /* Target the actual content container */
        [data-testid="stSidebar"] .block-container {
            min-width: 800px !important;
            width: 100% !important;
            margin: 0 auto !important;
        }

        [data-testid="stSidebar"] > div {
            height: auto !important;
            min-height: 100vh !important;
            width: 100% !important;
            padding: 2rem !important;
            background-color: rgb(240, 242, 246) !important;
        }

        /* Remove any width restrictions from Streamlit's default classes */
        div[data-testid="stSidebarUserContent"],
        div.st-emotion-cache-10trblm,
        div.st-emotion-cache-16idsys,
        div.st-emotion-cache-1outpf3 {
            width: auto !important;
        }

        /* Allow sidebar content to expand */
        .element-container, .stMarkdown {
            width: auto !important;
        }

        /* Hide all buttons in the sidebar */
        [data-testid="stSidebar"] button {
            display: none !important;
        }

        /* Show only the main collapse button */
        [data-testid="stSidebar"] > button[kind="secondary"] {
            display: flex !important;
            position: absolute !important;
            right: 0 !important;
            top: 0 !important;
            border-top-left-radius: 0 !important;
            border-bottom-left-radius: 0 !important;
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

        /* Main content area */
        .main .block-container {
            position: fixed !important;
            inset: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            max-width: none !important;
            width: 100% !important;
            height: 100vh !important;
            transition: margin-left 0.3s ease-in-out !important;
        }

        /* Main content when sidebar is expanded */
        [data-testid="stSidebar"][aria-expanded="true"] + .main .block-container {
            margin-left: var(--sidebar-width, 800px) !important;
            width: calc(100vw - var(--sidebar-width, 800px)) !important;
        }

        /* Ensure map container takes full space */
        .stApp > .main .block-container [data-testid="stVerticalBlock"] {
            height: 100vh !important;
            width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        .element-container:has(.stFolium) {
            height: 100vh !important;
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        .stFolium {
            height: 100vh !important;
            width: 100% !important;
        }

        /* Improved Sidebar Components Styling */
        .stSelectbox, .stMultiSelect {
            width: 100% !important;
            max-width: calc(100% - 40px) !important;
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

        /* Visualization container */
        .visualization-container {
            width: 100% !important;
            max-width: calc(100% - 40px) !important;
            margin: 20px auto !important;
            padding: 15px !important;
            background: white !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
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


def create_sidebar(
    data, chat_placeholder, data_calculated_events=None, visualization_func=None
):
    """Create the sidebar with filters and visualization."""
    with st.sidebar:
        st.title("Filtres")

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

        # Add visualization if a commune is selected
        if (
            selected_commune
            and data_calculated_events is not None
            and visualization_func is not None
        ):
            st.markdown(
                """<hr style='margin: 30px 0 !important;'>""", unsafe_allow_html=True
            )
            st.subheader("Visualisation de la Commune")

            # Create visualization container
            st.markdown('<div class="visualization-container">', unsafe_allow_html=True)

            # Generate and display the visualization
            fig = visualization_func(data_calculated_events, selected_commune)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

        return selected_categories, selected_types, selected_commune


def show_map(map_object):
    """Display the map in the main area."""
    # Display the map with fixed dimensions
    folium_static(map_object, width=1920, height=1080)
