"""Core functionality for the cultural map application."""

import pandas as pd
from .components.ui import setup_page, create_sidebar, show_map
from .components.map import create_map
from .components.chat import process_chat_input

def main():
    """Main function to run the application."""
    # Setup the page
    setup_page()
    
    # Load and prepare data
    data = pd.read_csv("data/mock_cultural_data.csv")
    
    # Create map object
    map_obj = create_map(
        data=data,
        selected_categories=None,
        selected_types=None,
        selected_commune=None
    )
    
    # Create sidebar with filters and chat
    selected_categories, selected_types, selected_commune = create_sidebar(
        data,
        lambda prompt: process_chat_input(prompt, data, map_obj)
    )
    
    # Update map based on filters
    filtered_map = create_map(
        data=data,
        selected_categories=selected_categories,
        selected_types=selected_types,
        selected_commune=selected_commune
    )
    
    # Show the map in the main area
    show_map(filtered_map)

if __name__ == "__main__":
    main()
