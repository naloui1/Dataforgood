import pandas as pd
import numpy as np

def convert_coordinates():
    # Read the CSV file with semicolon separator and low_memory=False to avoid dtype warnings
    df = pd.read_csv('/home/didamer/Projects/Campus/Dataforgood/data/results/Equipements_Communes.csv', 
                     sep=';',
                     low_memory=False)
    
    # Function to safely convert to float
    def safe_float_convert(x):
        try:
            return float(str(x).replace(',', '.'))
        except (ValueError, TypeError):
            return np.nan
    
    # Convert coordinates and count invalid values
    df['Equipement_latitude'] = df['Equipement_latitude'].apply(safe_float_convert)
    df['Equipement_longitude'] = df['Equipement_longitude'].apply(safe_float_convert)
    
    # Report invalid coordinates
    invalid_coords = df[df['Equipement_latitude'].isna() | df['Equipement_longitude'].isna()]
    print(f"\nFound {len(invalid_coords)} rows with invalid coordinates")
    if len(invalid_coords) > 0:
        print("\nSample of rows with invalid coordinates:")
        print(invalid_coords[['Nom_commune', 'Type', 'Nom_equipement', 'Equipement_latitude', 'Equipement_longitude']].head())
    
    # Save the modified DataFrame back to CSV
    df.to_csv('/home/didamer/Projects/Campus/Dataforgood/data/results/Equipements_Communes.csv', 
              sep=';', 
              index=False)
    
    print("\nFile has been updated successfully!")

if __name__ == "__main__":
    convert_coordinates()
