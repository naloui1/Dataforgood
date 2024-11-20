"""Script to prepare and save the cultural data in pickle format."""

import pandas as pd


def transform_data():
    """Transform the CSV data and save as pickle."""
    # Load the CSV file
    print("Loading CSV file...")
    data = pd.read_csv(
        "data/results/nbre_equipement_parcommuneetcodepostal_ET_LatitudeLongitude_ET_POPULATION.csv",
        sep="\t",  # Tab separated
        encoding="utf-8",
        dtype={
            "Commune": str,
            "code_insee": str,
            "Type équipement ou lieu": str,
            "categorie": str,
            "count": int,
            "PTOT": float,
            "latitude": float,
            "longitude": float,
        },
    )

    print("Transforming data...")

    # Calculate cultural density per commune
    commune_stats = (
        data.groupby("Commune")
        .agg(
            {
                "count": "sum",  # Total cultural structures
                "PTOT": "first",  # Population (same for all rows of a commune)
                "latitude": "first",  # Coordinates (same for all rows of a commune)
                "longitude": "first",
            }
        )
        .reset_index()
    )

    # Calculate cultural density (structures per 1000 inhabitants)
    commune_stats["cultural_density"] = (commune_stats["count"] * 1000) / commune_stats[
        "PTOT"
    ]

    # Create main DataFrame with required structure
    transformed_data = pd.DataFrame(
        {
            "nom_commune": data["Commune"].astype(str),
            "code_postal": data["code_insee"].astype(str),
            "type_infrastructure": data["Type équipement ou lieu"].astype(str),
            "nom_infrastructure": data["Type équipement ou lieu"].astype(str),
            "latitude": pd.to_numeric(data["latitude"], errors="coerce"),
            "longitude": pd.to_numeric(data["longitude"], errors="coerce"),
            "population": pd.to_numeric(data["PTOT"], errors="coerce"),
            "count": pd.to_numeric(data["count"], errors="coerce"),
            "categorie": data["categorie"].astype(str),
        }
    )

    # Merge cultural density data
    transformed_data = transformed_data.merge(
        commune_stats[["Commune", "cultural_density"]],
        left_on="nom_commune",
        right_on="Commune",
    ).drop("Commune", axis=1)

    # Drop rows with missing coordinates
    transformed_data = transformed_data.dropna(subset=["latitude", "longitude"])

    # Fill any remaining NaN values
    transformed_data["population"] = transformed_data["population"].fillna(0)
    transformed_data["count"] = transformed_data["count"].fillna(1)
    transformed_data["cultural_density"] = transformed_data["cultural_density"].fillna(
        0
    )

    # Create a separate DataFrame for heatmap data
    heatmap_data = commune_stats[["latitude", "longitude", "cultural_density"]].copy()
    heatmap_data = heatmap_data.dropna(
        subset=["latitude", "longitude", "cultural_density"]
    )

    print("Saving pickle files...")
    # Save both DataFrames
    transformed_data.to_pickle("data/cultural_data.pkl")
    heatmap_data.to_pickle("data/heatmap_data.pkl")
    print("Done! Data saved to data/cultural_data.pkl and data/heatmap_data.pkl")


if __name__ == "__main__":
    transform_data()
