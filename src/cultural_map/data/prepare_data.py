"""Script to prepare and save the cultural data in pickle format."""

import pandas as pd


def transform_data():
    """Transform the CSV data and save as pickle."""
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

    # Load the CSV file
    print("Loading CSV file...")
    data = pd.read_csv(
        "data/results/_WITH_data_union_AS_SELECT_libelle_geographique_AS_Nom_commune_p_202411201007.csv",
        sep=";",
        encoding="utf-8",
        dtype={
            "Nom commune principale": str,
            "Code Postal": str,
            "Type": str,
            "Nom d'evenement": str,
            "etb_latitude": str,
            "etb_longtitude": str,
        },
        low_memory=False,
    )

    print("Transforming data...")
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
        )
    )

    # Drop rows with missing coordinates
    transformed_data = transformed_data.dropna(subset=["latitude", "longitude"])

    print("Saving pickle file...")
    # Save as pickle
    transformed_data.to_pickle("data/cultural_data.pkl")
    print("Done! Data saved to data/cultural_data.pkl")


if __name__ == "__main__":
    transform_data()
