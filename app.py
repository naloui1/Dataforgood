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
    initial_sidebar_state="expanded"
)

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def process_chat_input(user_input, df, map_obj):
    """
    Process the chat input and return a response
    Args:
        user_input: str - The user's message
        df: pandas DataFrame - The data
        map_obj: folium.Map - The current map object
    Returns:
        str - The response message
    """
    if not st.session_state.get('openai_api_key'):
        return "Please enter your OpenAI API key in the configuration menu (⚙️) to use the chatbot."
    
    try:
        # Here we'll later implement the actual OpenAI chat logic
        # For now, return a placeholder response
        return f"You asked about: {user_input}"
    except Exception as e:
        return f"Error processing your request: {str(e)}"

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
):
    # Set bounds for France
    sw = [41.333, -4.833]  # Southwest corner
    ne = [51.2, 9.833]     # Northeast corner

    # If a commune is selected, center on it, otherwise center on France
    if selected_commune:
        commune_data = data[data["nom_commune"] == selected_commune].iloc[0]
        center_lat, center_lon = commune_data["latitude"], commune_data["longitude"]
        zoom_start = 13
    else:
        center_lat, center_lon = 46.603354, 1.888334  # Center of France
        zoom_start = 6

    # Create the base map with zoom restrictions
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles="CartoDB positron",
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

    # Define colors for categories
    category_colors = {
        "patrimoine": "blue",
        "spectacle_vivant": "red"
    }

    # Create a marker cluster
    marker_cluster = plugins.MarkerCluster().add_to(m)

    # Filter data based on selections
    filtered_data = data.copy()
    if selected_categories:
        filtered_data = filtered_data[filtered_data["categorie"].isin(selected_categories)]
    if selected_types:
        filtered_data = filtered_data[filtered_data["type_infrastructure"].isin(selected_types)]
    if selected_commune:
        filtered_data = filtered_data[filtered_data["nom_commune"] == selected_commune]

    # Add markers for each point
    for idx, row in filtered_data.iterrows():
        # Create popup content
        popup_content = f"""
        <div>
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
        st.title("🎭 Carte des Infrastructures Culturelles en France")

    # Load data
    df = load_data()

    # Sidebar filters
    st.sidebar.header("Filtres")

    # Configuration section in sidebar
    st.sidebar.markdown("---")  # Add a separator
    with st.sidebar.expander("⚙️ Configuration"):
        api_key = st.text_input("OpenAI API Key", type="password", key="openai_api_key")
        if api_key:
            import os
            os.environ["OPENAI_API_KEY"] = api_key

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
    )
    folium_static(map_obj, width=1200, height=600)
    
    # Add chat interface
    st.markdown("---")
    st.subheader("💬 Assistant Culturel")
    st.markdown("""
    Posez vos questions sur les infrastructures culturelles. Par exemple:
    - Montrez-moi tous les théâtres à Paris
    - Quelles sont les communes avec le plus de musées?
    - Filtrer les sites par type de spectacle vivant
    """)
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Posez votre question ici..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get and display assistant response
        response = process_chat_input(prompt, df, map_obj)
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response)
            
        # Rerun to update the chat display
        st.rerun()

if __name__ == "__main__":
    main()
