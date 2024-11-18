import streamlit as st
import folium
from folium import plugins
import pandas as pd
from streamlit_folium import folium_static

# Set page config
st.set_page_config(
    page_title="Carte Culturelle de France",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Theme handling
if "dark_theme" not in st.session_state:
    st.session_state.dark_theme = False

# Custom CSS for the theme toggle
st.markdown(
    """
    <style>
        /* Hide the default checkbox */
        .stCheckbox {
            display: none;
        }
        
        /* Custom theme toggle button */
        .theme-toggle {
            cursor: pointer;
            padding: 10px 15px;
            border-radius: 20px;
            display: inline-flex;
            align-items: center;
            background: #f0f2f6;
            margin-bottom: 20px;
        }
        
        .theme-toggle.dark {
            background: #262730;
        }
        
        /* Position the theme toggle button */
        [data-testid="stToolbar"] {
            right: 2rem;
        }
        
        /* Right align the button container */
        div.theme-toggle-container {
            position: fixed;
            right: 2rem;
            top: 0.5rem;
            z-index: 1000;
        }
        
        /* Style the button */
        .stButton > button {
            border-radius: 50%;
            padding: 0.5rem;
            aspect-ratio: 1;
            line-height: 1;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Update the theme
if st.session_state.dark_theme:
    st.markdown(
        """
        <style>
            /* Main app background */
            .stApp, .stSidebar, [data-testid="stHeader"] {
                background-color: #0E1117;
                color: #FAFAFA;
            }
            
            /* Buttons */
            .stButton button {
                background-color: #262730;
                color: #FAFAFA;
                border: 1px solid #4B4B4B;
            }
            
            /* Data elements */
            .stDataFrame div[role="cell"] {
                background-color: #262730 !important;
                color: #FAFAFA !important;
            }
            
            .stDataFrame div[role="columnheader"] {
                background-color: #262730 !important;
                color: #FAFAFA !important;
            }
            
            /* Metrics */
            div[data-testid="stMetricValue"] {
                color: #FAFAFA;
            }
            
            /* Select boxes and dropdowns */
            div[data-baseweb="select"] {
                background-color: #262730 !important;
            }
            
            div[data-baseweb="select"] * {
                background-color: #262730 !important;
                color: #FAFAFA !important;
            }
            
            /* Dropdown menu */
            div[data-baseweb="popover"] * {
                background-color: #262730 !important;
                color: #FAFAFA !important;
            }
            
            div[data-baseweb="popover"] div[role="listbox"] {
                background-color: #262730 !important;
            }
            
            div[data-baseweb="popover"] li:hover {
                background-color: #404040 !important;
            }
            
            /* Selected options in multiselect */
            div[data-baseweb="tag"] {
                background-color: #404040 !important;
            }
            
            div[data-baseweb="tag"] * {
                background-color: #404040 !important;
                color: #FAFAFA !important;
            }
            
            /* Top header bar */
            section[data-testid="stSidebar"] > div {
                background-color: #0E1117;
            }
            
            /* Headers and text */
            h1, h2, h3, h4, h5, h6, p {
                color: #FAFAFA !important;
            }
            
            /* Sidebar text */
            .stSidebar .stMarkdown {
                color: #FAFAFA;
            }
            
            /* Text input */
            .stTextInput > div > div {
                background-color: #262730;
                color: #FAFAFA;
            }
            
            /* Scrollbars */
            ::-webkit-scrollbar-track {
                background-color: #0E1117;
            }
            
            ::-webkit-scrollbar-thumb {
                background-color: #4B4B4B;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )


# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("data/mock_cultural_data.csv")
    return df


# Create the map
def create_map(
    data,
    selected_categories=None,
    selected_types=None,
    selected_commune=None,
    dark_mode=False,
):
    # Set bounds for France
    sw = [41.333, -4.833]  # Southwest corner
    ne = [51.2, 9.833]  # Northeast corner

    # If a commune is selected, center on it, otherwise center on France
    if selected_commune:
        commune_data = data[data["nom_commune"] == selected_commune].iloc[0]
        center_lat, center_lon = commune_data["latitude"], commune_data["longitude"]
        zoom_start = 13
    else:
        center_lat, center_lon = 46.603354, 1.888334  # Center of France
        zoom_start = 6

    # Select map tiles based on theme
    tiles = "CartoDB dark_matter" if dark_mode else "CartoDB positron"

    # Create the base map with zoom restrictions
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles=tiles,
        min_zoom=6,  # Restrict zoom out to France level
        max_zoom=18,  # Maximum zoom in level
    )

    # Add zoom control
    folium.plugins.Fullscreen().add_to(m)

    # Set initial bounds
    if not selected_commune:
        m.fit_bounds([sw, ne])

    # Add bounds control to restrict panning
    script = f"""
        var bounds = L.latLngBounds(
            L.latLng({sw[0]}, {sw[1]}),
            L.latLng({ne[0]}, {ne[1]})
        );
        map.setMaxBounds(bounds);
        map.on('drag', function() {{
            map.panInsideBounds(bounds, {{ animate: false }});
        }});
    """
    m.get_root().script.add_child(folium.Element(script))

    # Define colors for categories based on theme
    category_colors = {
        "patrimoine": "lightblue" if dark_mode else "blue",
        "spectacle_vivant": "orange" if dark_mode else "red",
    }

    # Create a marker cluster
    marker_cluster = plugins.MarkerCluster().add_to(m)

    # Filter data based on selections
    filtered_data = data.copy()
    if selected_categories:
        filtered_data = filtered_data[
            filtered_data["categorie"].isin(selected_categories)
        ]
    if selected_types:
        filtered_data = filtered_data[
            filtered_data["type_infrastructure"].isin(selected_types)
        ]
    if selected_commune:
        filtered_data = filtered_data[filtered_data["nom_commune"] == selected_commune]

    # Add markers for each point
    for idx, row in filtered_data.iterrows():
        # Create popup content with themed styling
        popup_style = "color: white;" if dark_mode else "color: black;"
        popup_content = f"""
        <div style="{popup_style}">
        <b>{row['nom_infrastructure']}</b><br>
        Type: {row['type_infrastructure']}<br>
        Catégorie: {row['categorie']}<br>
        Commune: {row['nom_commune']}<br>
        Code Postal: {row['code_postal']}
        </div>
        """

        # Create marker
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color=category_colors[row["categorie"]], icon="info-sign"),
        ).add_to(marker_cluster)

    return m


def main():
    # Create a layout with two columns
    left_col, right_col = st.columns([11, 1])

    with left_col:
        st.title("🎭 Carte de la culture dans les petites villes de France")

    with right_col:
        if st.session_state.dark_theme:
            if st.button("🌙"):
                st.session_state.dark_theme = False
                st.rerun()
        else:
            if st.button("☀️"):
                st.session_state.dark_theme = True
                st.rerun()

    # Load data
    df = load_data()

    # Sidebar filters
    st.sidebar.header("Filtres")

    # Commune search with autocomplete
    communes = sorted(df["nom_commune"].unique())
    selected_commune = st.sidebar.selectbox(
        "Rechercher une commune",
        [""] + communes,
        format_func=lambda x: "Toutes les communes" if x == "" else x,
    )

    # Category filter
    categories = sorted(df["categorie"].unique())
    selected_categories = st.sidebar.multiselect(
        "Catégories", categories, default=categories
    )

    # Type filter
    types = sorted(df["type_infrastructure"].unique())
    selected_types = st.sidebar.multiselect(
        "Types d'infrastructure", types, default=types
    )

    # Display some statistics
    col1, col2, col3 = st.columns(3)

    filtered_df = df.copy()
    if selected_categories:
        filtered_df = filtered_df[filtered_df["categorie"].isin(selected_categories)]
    if selected_types:
        filtered_df = filtered_df[
            filtered_df["type_infrastructure"].isin(selected_types)
        ]
    if selected_commune:
        filtered_df = filtered_df[filtered_df["nom_commune"] == selected_commune]

    with col1:
        st.metric("Nombre de sites", len(filtered_df))
    with col2:
        st.metric("Nombre de communes", len(filtered_df["nom_commune"].unique()))
    with col3:
        st.metric(
            "Types d'infrastructures", len(filtered_df["type_infrastructure"].unique())
        )

    # Create and display map
    st.subheader("Carte Interactive")
    map_obj = create_map(
        df,
        selected_categories,
        selected_types,
        selected_commune,
        st.session_state.dark_theme,
    )
    folium_static(map_obj, width=1200, height=600)


if __name__ == "__main__":
    main()
