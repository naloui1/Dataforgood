"""Core functionality for the cultural map application."""

import pandas as pd
import streamlit as st
from .components.ui import setup_page, create_sidebar, show_map
from .components.map import create_map
from .components.chat import process_chat_input


@st.cache_data(show_spinner="Loading cultural data...")
def load_data():
    """Load the preprocessed cultural data."""
    return pd.read_pickle("data/cultural_data.pkl")


@st.cache_data(show_spinner=False)
def filter_data(
    data, selected_categories=None, selected_types=None, selected_commune=None
):
    """Filter data based on selections with caching."""
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
    return filtered_data


def main():
    """Main function to run the application."""
    # Setup the page
    setup_page()

    # Load preprocessed data
    data = load_data()

    # Create sidebar with filters and chat
    selected_categories, selected_types, selected_commune = create_sidebar(
        data,
        lambda prompt: process_chat_input(
            prompt, data, None
        ),  # Pass None since we don't need the map object for chat
    )

    # Filter data with caching
    filtered_data = filter_data(
        data, selected_categories, selected_types, selected_commune
    )

    # Create map with filtered data
    filtered_map = create_map(
        data=filtered_data,
        selected_categories=selected_categories,
        selected_types=selected_types,
        selected_commune=selected_commune,
    )

    # Show the map in the main area
    show_map(filtered_map)


if __name__ == "__main__":
    main()
