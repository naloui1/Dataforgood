"""Core functionality for the cultural map application."""

import pandas as pd
import streamlit as st
from .components.ui import setup_page, create_sidebar, show_map
from .components.map import create_map
from .components.chat import process_chat_input


def main():
    """Main function to run the application."""
    # Setup the page
    setup_page()

    # Load and prepare data
    data = pd.read_csv("data/mock_cultural_data.csv")

    # Create sidebar with filters and chat
    selected_categories, selected_types, selected_commune = create_sidebar(
        data,
        lambda prompt: process_chat_input(
            prompt, data, None
        ),  # Pass None since we don't need the map object for chat
    )

    # Create map with filters
    filtered_map = create_map(
        data=data,
        selected_categories=selected_categories,
        selected_types=selected_types,
        selected_commune=selected_commune,
    )

    # Show the map in the main area
    show_map(filtered_map)


if __name__ == "__main__":
    main()
