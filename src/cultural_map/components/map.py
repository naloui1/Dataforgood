"""Map component functionality."""

import folium
from folium import plugins
from streamlit_folium import folium_static
import branca

# Define colors for categories
CATEGORY_COLORS = {
    "patrimoine": "blue",  # Cultural heritage sites
    "spectacle_vivant": "red",  # Live performances and cultural activities
}


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

    # Determine initial view
    if selected_commune:
        commune_data = data[data["nom_commune"] == selected_commune].iloc[0]
        initial_location = [commune_data["latitude"], commune_data["longitude"]]
        initial_zoom = 13  # Adjusted for better commune view
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

    # Add bounds control
    bounds_script = f"""
        var southWest = L.latLng({sw[0]}, {sw[1]});
        var northEast = L.latLng({ne[0]}, {ne[1]});
        var bounds = L.latLngBounds(southWest, northEast);
        
        // Set bounds
        map.setMaxBounds(bounds);
        
        // Prevent dragging outside bounds
        map.on('drag', function() {{
            map.panInsideBounds(bounds, {{ animate: false }});
        }});
        
        // Force bounds check on any view change
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
        
        // Enforce minimum zoom
        map.on('zoomend', function() {{
            if (map.getZoom() < 5) {{
                map.setZoom(5);
            }}
        }});

        // If a commune is selected, ensure we're at the correct zoom level
        if ({selected_commune is not None}) {{
            map.setZoom(13);
        }}
    """

    # Add the bounds control script
    m.get_root().script.add_child(folium.Element(bounds_script))

    # Create optimized marker cluster
    marker_cluster = plugins.MarkerCluster(
        options={
            "maxClusterRadius": 50,  # Smaller radius for more granular clusters
            "disableClusteringAtZoom": 12,  # Stop clustering at zoom level 12
            "spiderfyOnMaxZoom": True,  # Enable spiderfy for overlapping markers
            "showCoverageOnHover": False,  # Disable coverage display for performance
            "zoomToBoundsOnClick": True,  # Zoom to bounds when clicking cluster
            "removeOutsideVisibleBounds": True,  # Remove markers outside view
            "animate": False,  # Disable animations for better performance
        }
    ).add_to(m)

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

    # Add markers with optimized popup content
    for _, row in filtered_data.iterrows():
        popup_content = f"""
        <div style='font-family: Arial, sans-serif; min-width: 200px;'>
            <h4 style='margin-bottom: 10px;'>{row['nom_infrastructure']}</h4>
            <p><b>Type:</b> {row['type_infrastructure']}<br>
            <b>Catégorie:</b> {row['categorie']}<br>
            <b>Commune:</b> {row['nom_commune']}<br>
            <b>Code Postal:</b> {row['code_postal']}</p>
        </div>
        """

        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color=CATEGORY_COLORS[row["categorie"]], icon="info-sign"),
        ).add_to(marker_cluster)

    return m
