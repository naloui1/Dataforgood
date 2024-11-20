"""Core functionality for the cultural map application."""

import pandas as pd
import streamlit as st
from .components.ui import setup_page, create_sidebar, show_map
from .components.map import create_map
from .components.visualisation import creating_vusualisation


@st.cache_data(show_spinner="Loading cultural data...")
def load_data():
    """Load the preprocessed cultural data."""
    return pd.read_pickle("data/cultural_data.pkl")


@st.cache_data
def load_calculated_events_data():
    """Load and cache the calculated events data."""
    return pd.read_csv(
        "data/results/nbre_equipement_parcommuneetcodepostal_ET_LatitudeLongitude_ET_POPULATION.csv",
        sep="\t",
    )


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
    data = load_data()  ## pickle for the map
    data_calculated_events = load_calculated_events_data()  ## csv for the visualisation

    # Create sidebar with filters and visualization
    selected_categories, selected_types, selected_commune = create_sidebar(
        data,
        None,  # Placeholder parameter to maintain function signature
        data_calculated_events,  # Pass the visualization data
        creating_vusualisation,  # Pass the visualization function
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
