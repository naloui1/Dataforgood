"""Map component functionality."""

import folium
from folium import plugins
from streamlit_folium import folium_static
import branca

# Define colors for categories
CATEGORY_COLORS = {
    "patrimoine": "blue",
    "spectacle_vivant": "red"
}

def create_map(data, selected_categories=None, selected_types=None, selected_commune=None):
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
    # Set tighter bounds for France
    sw = [42.333, -4.833]  # Southwest corner - adjusted north
    ne = [51.2, 8.833]     # Northeast corner - adjusted west
    
    center_lat = (sw[0] + ne[0]) / 2
    center_lon = (sw[1] + ne[1]) / 2

    # Create base map with center of France
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=7,  # Increased default zoom
        tiles="CartoDB positron",
        min_zoom=6,    # Increased minimum zoom
        max_zoom=18,
        dragging=True,
        scrollWheelZoom=True,
    )

    # Add strict bounds control using custom JavaScript
    bounds_script = f"""
        var southWest = L.latLng({sw[0]}, {sw[1]});
        var northEast = L.latLng({ne[0]}, {ne[1]});
        var bounds = L.latLngBounds(southWest, northEast);
        
        // Initial setup
        map.setMaxBounds(bounds);
        map.options.minZoom = 6;
        
        // Prevent dragging outside bounds
        map.on('drag', function() {{
            map.panInsideBounds(bounds, {{ animate: true }});
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
                
                map.setView([y, x], map.getZoom());
            }}
        }});
        
        // Enforce minimum zoom
        map.on('zoomend', function() {{
            if (map.getZoom() < 6) {{
                map.setZoom(6);
            }}
        }});
        
        // Additional bounds check on move
        map.on('move', function() {{
            map.panInsideBounds(bounds, {{ animate: true }});
        }});
    """
    
    # Add the bounds control script
    m.get_root().script.add_child(folium.Element(bounds_script))

    # If a commune is selected, zoom to it with a tighter view
    if selected_commune:
        commune_data = data[data["nom_commune"] == selected_commune].iloc[0]
        lat, lon = commune_data["latitude"], commune_data["longitude"]
        
        # Much smaller buffer for closer zoom
        buffer = 0.01  # Reduced from 0.05 to 0.01
        
        # Set view with higher zoom level
        m.fit_bounds(
            [[lat - buffer, lon - buffer],
             [lat + buffer, lon + buffer]],
            max_zoom=16  # Increased from 15 to 16 for closer zoom
        )
        
        # Force a minimum zoom level for communes
        m.zoom_start = 14  # Added explicit zoom level
    else:
        # Set default bounds to France
        m.fit_bounds([sw, ne])

    # Add fullscreen control
    plugins.Fullscreen().add_to(m)

    # Create marker cluster
    marker_cluster = plugins.MarkerCluster().add_to(m)

    # Filter data based on selections
    filtered_data = data.copy()
    if selected_categories:
        filtered_data = filtered_data[filtered_data["categorie"].isin(selected_categories)]
    if selected_types:
        filtered_data = filtered_data[filtered_data["type_infrastructure"].isin(selected_types)]
    if selected_commune:
        filtered_data = filtered_data[filtered_data["nom_commune"] == selected_commune]

    # Add markers
    for _, row in filtered_data.iterrows():
        popup_content = f"""
        <div>
        <b>{row['nom_infrastructure']}</b><br>
        Type: {row['type_infrastructure']}<br>
        Catégorie: {row['categorie']}<br>
        Commune: {row['nom_commune']}<br>
        Code Postal: {row['code_postal']}
        </div>
        """

        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color=CATEGORY_COLORS[row["categorie"]], icon="info-sign"),
        ).add_to(marker_cluster)

    return m
