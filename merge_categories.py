import pandas as pd

# Read the CSV files
communes_df = pd.read_csv('./data/20230823-communes-departement-region.csv', dtype={'code_commune_INSEE': str})
categories_df = pd.read_csv('./data/nbre_categorie_parcommuneetcodepostal.csv', delimiter='\t', dtype={'code_insee': str})

# Clean up the code_insee
categories_df['code_insee'] = categories_df['code_insee'].str.strip()

# Create a pivot table to get categories and counts side by side
categories_pivot = categories_df.pivot_table(
    index='code_insee',
    columns='categorie',
    values='Nombre d\'éléments',
    aggfunc='sum',
    fill_value=0
).reset_index()

# Rename columns to be more descriptive
for col in categories_pivot.columns:
    if col != 'code_insee':
        categories_pivot.rename(columns={col: f'nombre_{col}'}, inplace=True)

# Merge with the communes file
result = communes_df.merge(
    categories_pivot,
    left_on='code_commune_INSEE',
    right_on='code_insee',
    how='inner'  # Changed from 'left' to 'inner' to keep only matching communes
)

# Drop the redundant code_insee column
result = result.drop('code_insee', axis=1)

# Save the result
result.to_csv('./data/communes_with_categories.csv', index=False)
