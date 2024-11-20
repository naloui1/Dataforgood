"""Core functionality for the cultural map application."""

import pandas as pd
import streamlit as st
from .components.ui import setup_page, create_sidebar, show_map
from .components.map import create_map
from .components.chat import process_chat_input


@st.cache_data
def load_and_prepare_data():
    """Load and prepare the cultural data with caching."""
    # Load the new CSV file with specified dtypes
    dtypes = {
        "Nom commune principale": str,
        "Code Postal": str,
        "Type": str,
        "Nom d'evenement": str,
        "etb_latitude": str,  # Will be converted to float later
        "etb_longtitude": str,  # Will be converted to float later
    }

    data = pd.read_csv(
        "data/results/_WITH_data_union_AS_SELECT_libelle_geographique_AS_Nom_commune_p_202411201007.csv",
        sep=";",
        encoding="utf-8",
        dtype=dtypes,
        low_memory=False,
    )

    # Define type mappings to categories
    patrimoine_types = [
        "Monument",
        "Musée",
        "Lieu archéologique",
        "Service d'archives",
        "Parc et jardin",
        "Espace protégé",
    ]

    spectacle_vivant_types = [
        "Théâtre",
        "Cinéma",
        "Bibliothèque",
        "Conservatoire",
        "Scène",
        "Musique",
        "Spectacle vivant",
        "Pluridisciplinaire",
        "Cinéma, audiovisuel",
        "Livre, littérature",
    ]

    # Create DataFrame with required structure
    transformed_data = pd.DataFrame(
        {
            "nom_commune": data["Nom commune principale"],
            "code_postal": data["Code Postal"],
            "type_infrastructure": data["Type"],
            "nom_infrastructure": data["Nom d'evenement"],
            "latitude": pd.to_numeric(
                data["etb_latitude"].str.replace(",", "."), errors="coerce"
            ),
            "longitude": pd.to_numeric(
                data["etb_longtitude"].str.replace(",", "."), errors="coerce"
            ),
        }
    )

    # Map types to categories
    transformed_data["categorie"] = transformed_data["type_infrastructure"].apply(
        lambda x: (
            "patrimoine"
            if x in patrimoine_types
            else "spectacle_vivant" if x in spectacle_vivant_types else "patrimoine"
        )  # Default to patrimoine for unknown types
    )

    # Drop rows with missing coordinates
    transformed_data = transformed_data.dropna(subset=["latitude", "longitude"])

    return transformed_data


def main():
    """Main function to run the application."""
    # Setup the page
    setup_page()

    # Load and prepare data (now cached)
    data = load_and_prepare_data()

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
