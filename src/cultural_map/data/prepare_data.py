"""Script to prepare and save the cultural data in CSV format."""

import pandas as pd


def transform_data():
    """Transform the CSV data and save as CSV."""
    # Load the CSV files
    print("Loading CSV files...")
    equipements = pd.read_csv(
        "data/results/Equipements_Communes.csv",
        sep=";",  # Semicolon separated
        encoding="utf-8",
        dtype={
            "Nom_commune": str,
            "Code_insee": str,
            "Type": str,
            "Nom_equipement": str,
            "Population_totale": float,
            "Commune_latitude": float,
            "Commune_longitude": float,
            "Equipement_latitude": float,
            "Equipement_longitude": float,
            "Categorie": str,
        },
    )

    heatmap = pd.read_csv(
        "data/results/Heatmap_Culture.csv",
        sep="\t",  # Tab separated
        encoding="utf-8",
        dtype={
            "Commune": str,
            "code_insee": str,
            "Type_equipement": str,
            "Population_Totale": float,
            "latitude": float,
            "longitude": float,
            "Nombre_categorie": int,
            "categorie": str,
        },
    )

    print("Transforming data...")

    # Calculate cultural density per commune from heatmap data
    commune_stats = (
        heatmap.groupby("Commune")
        .agg(
            {
                "Nombre_categorie": "sum",  # Total cultural structures
                "Population_Totale": "first",  # Population
                "latitude": "first",  # Coordinates
                "longitude": "first",
            }
        )
        .reset_index()
    )

    # Calculate cultural density (structures per 1000 inhabitants)
    commune_stats["cultural_density"] = (commune_stats["Nombre_categorie"] * 1000) / commune_stats[
        "Population_Totale"
    ]

    # Create main DataFrame with required structure from equipements data
    transformed_data = pd.DataFrame(
        {
            "nom_commune": equipements["Nom_commune"].astype(str),
            "code_postal": equipements["Code_insee"].astype(str),
            "type_infrastructure": equipements["Type"].astype(str),
            "nom_infrastructure": equipements["Nom_equipement"].astype(str),
            "latitude": pd.to_numeric(equipements["Equipement_latitude"], errors="coerce"),
            "longitude": pd.to_numeric(equipements["Equipement_longitude"], errors="coerce"),
            "population": pd.to_numeric(equipements["Population_totale"], errors="coerce"),
            "categorie": equipements["Categorie"].astype(str),
        }
    )

    # Merge cultural density data
    transformed_data = transformed_data.merge(
        commune_stats[["Commune", "cultural_density"]],
        left_on="nom_commune",
        right_on="Commune",
        how="left"
    ).drop("Commune", axis=1)

    # Drop rows with missing coordinates
    transformed_data = transformed_data.dropna(subset=["latitude", "longitude"])

    # Fill any remaining NaN values
    transformed_data["population"] = transformed_data["population"].fillna(0)
    transformed_data["cultural_density"] = transformed_data["cultural_density"].fillna(0)

    # Create a separate DataFrame for heatmap data
    heatmap_data = commune_stats[["latitude", "longitude", "cultural_density"]].copy()
    heatmap_data = heatmap_data.dropna(
        subset=["latitude", "longitude", "cultural_density"]
    )

    print("Saving CSV files...")
    # Save both DataFrames as CSV
    transformed_data.to_csv("data/cultural_data.csv", index=False, encoding="utf-8")
    heatmap_data.to_csv("data/heatmap_data.csv", index=False, encoding="utf-8")
    print("Done! Data saved to data/cultural_data.csv and data/heatmap_data.csv")


if __name__ == "__main__":
    transform_data()
