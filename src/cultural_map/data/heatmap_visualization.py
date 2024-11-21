import pandas as pd
import numpy as np
import plotly.express as px

# path to the file
path_data='../../../data/results/'
name_file_lieux_equipements_culturels = 'Heatmap_Culture.csv'


# load data
df_synthese=pd.read_csv(path_data+name_file_lieux_equipements_culturels, sep='\t', on_bad_lines='skip' ,encoding='utf-8',low_memory=False)
df_synthese.head()

# variables
Nbre_habitants = 1000# nbre de habitant par commune pour le calcul du score
seuil = 10

# calcul de score
# somme du nbre de culturel par commune ((nbre patrimoine+nbre vivant)=sum(count par commune))
nbre_culturel = df_synthese.groupby(['code_insee','Commune','Region','latitude','longitude','Population_Totale','Num_Region','Num_Dep'])['Nombre_categorie'].sum() # create Série avec MultiIndex
# Convertir la Série avec MultiIndex en DataFrame
df_nbre_culturel = nbre_culturel.reset_index(name='nbr_total_culturel')

# Calcul du score par commune = (nbre patrimoine+ nbre vivant)/population
# score par commune pour 50 habitants = score par commune * 50
df_nbre_culturel['Nbre_culturels_N_habitants'] = (df_nbre_culturel['nbr_total_culturel'] / df_nbre_culturel['Population_Totale'])*Nbre_habitants


# seuillage du score, nécessaire pour l'affichage: si le score>1, score=1
df_nbre_culturel['Nbre_culturels_N_habitants_seuillee'] = df_nbre_culturel['Nbre_culturels_N_habitants'] 
df_nbre_culturel.loc[df_nbre_culturel['Nbre_culturels_N_habitants_seuillee']>seuil,'Nbre_culturels_N_habitants_seuillee']=seuil


# suprimer les score=Inf dues à une population=0
# Remplacer les valeurs Inf par NaN
df_nbre_culturel.replace([np.inf, -np.inf], np.nan, inplace=True)
# Supprimer les lignes contenant des NaN
df_nbre_culturel = df_nbre_culturel.dropna()

# heatmap visu
# rename column for visu
df_nbre_culturel = df_nbre_culturel.rename(columns={'Nbre_culturels_N_habitants_seuillee':'Nbre culturels pour'+str(Nbre_habitants)+' habitants'})
df_nbre_culturel.head()

fig = px.scatter_map(df_nbre_culturel, lat="latitude", lon="longitude", color='Nbre culturels pour'+str(Nbre_habitants)+' habitants', size="nbr_total_culturel",
                 # color_continuous_scale=px.colors.cyclical.IceFire,
                  color_discrete_sequence=px.colors.qualitative.Pastel,
                  #px.colors.cyclical.IceFire, #'PuBu',#
                    size_max=15, zoom=10,
                  map_style="carto-positron")
fig.show()

# save to cv files
df_nbre_culturel.to_csv(path_data+'Heatmap_Culture_with_score.csv', sep='\t', index=False)  