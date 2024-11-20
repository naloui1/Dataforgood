"""Map component functionality."""

import folium
from folium import plugins
from streamlit_folium import folium_static
import branca
import numpy as np
import pandas as pd

# Define type-specific colors and icons with larger radius
TYPE_STYLES = {
    "Monument": {"color": "#e41a1c", "radius": 8},  # Red
    "Musée": {"color": "#377eb8", "radius": 8},  # Blue
    "Bibliothèque": {"color": "#4daf4a", "radius": 8},  # Green
    "Théâtre": {"color": "#984ea3", "radius": 8},  # Purple
    "Cinéma": {"color": "#ff7f00", "radius": 8},  # Orange
    "Conservatoire": {"color": "#ffff33", "radius": 8},  # Yellow
    "Scène": {"color": "#a65628", "radius": 8},  # Brown
    "Musique": {"color": "#f781bf", "radius": 8},  # Pink
    "Lieu archéologique": {"color": "#999999", "radius": 8},  # Gray
    "Service d'archives": {"color": "#a6cee3", "radius": 8},  # Light blue
    "Parc et jardin": {"color": "#b2df8a", "radius": 8},  # Light green
    "Espace protégé": {"color": "#fb9a99", "radius": 8},  # Light red
    "Spectacle vivant": {"color": "#fdbf6f", "radius": 8},  # Light orange
    "Pluridisciplinaire": {"color": "#cab2d6", "radius": 8},  # Light purple
    "Cinéma, audiovisuel": {"color": "#ff7f00", "radius": 8},  # Orange
    "Livre, littérature": {"color": "#4daf4a", "radius": 8},  # Green
}

# Default style for unknown types
DEFAULT_STYLE = {"color": "#808080", "radius": 6}  # Gray


def sample_data_by_zoom(data, zoom_level):
    """Sample data based on zoom level to reduce markers."""
    # Progressive sampling rates from country to city level
    if zoom_level >= 13:  # City level
        return data  # 100%
    elif zoom_level >= 11:  # Metropolitan area
        return data.sample(frac=0.8, random_state=42)  # 80%
    elif zoom_level >= 9:  # Department level
        return data.sample(frac=0.6, random_state=42)  # 60%
    elif zoom_level >= 7:  # Regional level
        return data.sample(frac=0.4, random_state=42)  # 40%
    elif zoom_level >= 6:  # Multi-region level
        return data.sample(frac=0.2, random_state=42)  # 20%
    else:  # Country level (zoom 5 and below)
        return data.sample(frac=0.1, random_state=42)  # 10%


def create_map(
    data, selected_categories=None, selected_types=None, selected_commune=None
):
    """
    Create an interactive map with cultural infrastructure markers.

    Args:
        data (pd.DataFrame): DataFrame containing cultural infrastructure data
        selected_categories (list): List of selected categories
        selected_types (list): List of selected infrastructure types
        selected_commune (str): Selected commune name

    Returns:
        folium.Map: The created map object
    """
    # Set bounds for France
    sw = [41.333, -4.833]  # Southwest corner (adjusted for Corsica)
    ne = [51.2, 8.833]  # Northeast corner

    # Determine initial view and zoom
    if selected_commune:
        commune_data = data[data["nom_commune"] == selected_commune].iloc[0]
        initial_location = [commune_data["latitude"], commune_data["longitude"]]
        initial_zoom = 13
    else:
        initial_location = [(sw[0] + ne[0]) / 2, (sw[1] + ne[1]) / 2]
        initial_zoom = 6

    # Create base map with optimized settings
    m = folium.Map(
        location=initial_location,
        zoom_start=initial_zoom,
        tiles="CartoDB positron",
        min_zoom=5,
        max_zoom=18,
        dragging=True,
        scrollWheelZoom=True,
        control_scale=True,
        zoomControl=True,
        prefer_canvas=True,
    )

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

    # Sample data based on initial zoom level
    sampled_data = sample_data_by_zoom(filtered_data, initial_zoom)

    # Create marker cluster
    marker_cluster = plugins.MarkerCluster(
        name="Clusters", overlay=True, control=True, icon_create_function=None
    )

    # Add markers with type-specific styling and hover tooltips
    for _, row in sampled_data.iterrows():
        style = TYPE_STYLES.get(row["type_infrastructure"], DEFAULT_STYLE)

        # Create tooltip content
        tooltip_content = f"""
        <div style="text-align: center;">
            <strong>{row['nom_infrastructure']}</strong><br>
            Type: {row['type_infrastructure']}<br>
            Commune: {row['nom_commune']}<br>
            Code Postal: {row['code_postal']}
        </div>
        """

        # Create circle marker
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=style["radius"],
            color=style["color"],
            fill=True,
            fillColor=style["color"],
            fillOpacity=0.6,
            weight=1,
            opacity=0.8,
            tooltip=tooltip_content,
        ).add_to(marker_cluster)

    marker_cluster.add_to(m)

    # Add legend with larger dots
    legend_html = """
        <div style="position: fixed; bottom: 50px; right: 50px; z-index: 1000; background-color: white; 
                    padding: 10px; border-radius: 5px; border: 2px solid rgba(0,0,0,0.2); max-height: 300px; 
                    overflow-y: auto;">
            <h4 style="margin-bottom: 10px;">Types d'infrastructure</h4>
    """
    for type_name, style in TYPE_STYLES.items():
        legend_html += f"""
            <div style="margin-bottom: 5px;">
                <span style="display: inline-block; width: 16px; height: 16px; border-radius: 50%; 
                           background-color: {style['color']}; margin-right: 5px;"></span>
                {type_name}
            </div>
        """
    legend_html += "</div>"
    m.get_root().html.add_child(folium.Element(legend_html))

    # Add bounds control
    bounds_script = f"""
        var southWest = L.latLng({sw[0]}, {sw[1]});
        var northEast = L.latLng({ne[0]}, {ne[1]});
        var bounds = L.latLngBounds(southWest, northEast);
        
        map.setMaxBounds(bounds);
        
        map.on('drag', function() {{
            map.panInsideBounds(bounds, {{ animate: false }});
        }});
        
        map.on('moveend', function() {{
            if (!bounds.contains(map.getCenter())) {{
                var c = map.getCenter();
                var x = c.lng;
                var y = c.lat;
                
                var maxX = bounds.getEast();
                var maxY = bounds.getNorth();
                var minX = bounds.getWest();
                var minY = bounds.getSouth();
                
                if (x < minX) x = minX;
                if (x > maxX) x = maxX;
                if (y < minY) y = minY;
                if (y > maxY) y = maxY;
                
                map.setView([y, x], map.getZoom(), {{animate: false}});
            }}
        }});
        
        map.on('zoomend', function() {{
            if (map.getZoom() < 5) {{
                map.setZoom(5);
            }}
        }});

        if ({selected_commune is not None}) {{
            map.setZoom(13);
        }}
    """
    m.get_root().script.add_child(folium.Element(bounds_script))

    return m
