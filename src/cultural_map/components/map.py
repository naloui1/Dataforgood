"""Map component functionality."""

import folium
from folium import plugins
from streamlit_folium import folium_static
import branca

# Define colors for categories
CATEGORY_COLORS = {"patrimoine": "blue", "spectacle_vivant": "red"}


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
    # Set tighter bounds for France
    sw = [42.333, -4.833]  # Southwest corner - adjusted north
    ne = [51.2, 8.833]  # Northeast corner - adjusted west

    center_lat = (sw[0] + ne[0]) / 2
    center_lon = (sw[1] + ne[1]) / 2

    # Create base map with center of France
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=7,
        tiles="CartoDB positron",
        min_zoom=6,
        max_zoom=18,
        dragging=True,
        scrollWheelZoom=True,
        control_scale=True,
        zoomControl=False,  # Disable zoom control completely
    )

    # Add strict bounds control and sidebar offset handling using custom JavaScript
    bounds_script = f"""
        var southWest = L.latLng({sw[0]}, {sw[1]});
        var northEast = L.latLng({ne[0]}, {ne[1]});
        var bounds = L.latLngBounds(southWest, northEast);
        var sidebarWidth = 860;
        
        // Initial setup
        map.setMaxBounds(bounds);
        map.options.minZoom = 6;
        
        // Function to calculate the offset based on sidebar state
        function calculateOffset() {{
            var sidebar = document.querySelector('[data-testid="stSidebar"]');
            var isExpanded = sidebar.getAttribute('aria-expanded') !== 'false';
            // When expanded, offset by 430px (half of sidebar width)
            return isExpanded ? 430 : 0;
        }}
        
        // Function to adjust center based on sidebar state
        function adjustCenter(animate = true) {{
            var offset = calculateOffset();
            var mapWidth = map.getContainer().clientWidth;
            var center = map.getCenter();
            
            // Convert center to pixels
            var centerPoint = map.latLngToContainerPoint(center);
            
            // Calculate new center point with offset
            var newCenterPoint = L.point(
                centerPoint.x + offset,
                centerPoint.y
            );
            
            // Convert back to LatLng
            var newCenter = map.containerPointToLatLng(newCenterPoint);
            
            if (animate) {{
                map.panTo(newCenter, {{animate: true, duration: 0.3}});
            }} else {{
                map.setView(newCenter, map.getZoom(), {{animate: false}});
            }}
        }}
        
        // Watch for sidebar collapse/expand
        var observer = new MutationObserver(function(mutations) {{
            mutations.forEach(function(mutation) {{
                if (mutation.target.getAttribute('aria-expanded') !== null) {{
                    setTimeout(function() {{
                        adjustCenter(true);
                    }}, 50);
                }}
            }});
        }});
        
        // Start observing the sidebar
        var sidebar = document.querySelector('[data-testid="stSidebar"]');
        observer.observe(sidebar, {{ attributes: true, attributeFilter: ['aria-expanded'] }});
        
        // Prevent dragging outside bounds
        map.on('drag', function() {{
            map.panInsideBounds(bounds, {{ animate: false }});
        }});
        
        // Force bounds check and adjust center on any view change
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
            if (map.getZoom() < 6) {{
                map.setZoom(6);
            }}
        }});
        
        // Initial center adjustment (delayed to ensure DOM is ready)
        setTimeout(function() {{
            adjustCenter(false);
        }}, 300);
        
        // Adjust center when window is resized
        window.addEventListener('resize', function() {{
            setTimeout(function() {{
                adjustCenter(false);
            }}, 100);
        }});

        // Custom function to center on a point with offset
        window.centerMapOnPoint = function(lat, lng, zoom) {{
            // Get map dimensions
            var mapHeight = map.getContainer().clientHeight;
            var mapWidth = map.getContainer().clientWidth;
            
            // Calculate offsets
            var horizontalOffset = calculateOffset();
            var verticalOffset = mapHeight * 0.4; // Move point up by 40% of map height
            
            // Project the target point
            var targetPoint = map.project([lat, lng], zoom);
            
            // Apply offsets
            targetPoint.x = targetPoint.x - horizontalOffset;
            targetPoint.y = targetPoint.y - verticalOffset;
            
            // Convert back to LatLng and set view
            var targetLatLng = map.unproject(targetPoint, zoom);
            map.setView(targetLatLng, zoom, {{animate: true, duration: 0.5}});
        }};
    """

    # Add the bounds control script
    m.get_root().script.add_child(folium.Element(bounds_script))

    # If a commune is selected, zoom to it with a tighter view
    if selected_commune:
        commune_data = data[data["nom_commune"] == selected_commune].iloc[0]
        lat, lon = commune_data["latitude"], commune_data["longitude"]

        # Add JavaScript to center on the selected commune with offset
        center_script = f"""
            setTimeout(function() {{
                window.centerMapOnPoint({lat}, {lon}, 17);
            }}, 400);
        """
        m.get_root().script.add_child(folium.Element(center_script))

    else:
        # Set default bounds to France
        m.fit_bounds([sw, ne])

    # Create marker cluster
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
