import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def creating_visualisation(data: pd.DataFrame, nom_commune: str = None) -> go.Figure:
    
    # Define the TYPE_STYLES
    TYPE_STYLES = {
        "Monument": {"color": "#e41a1c", "radius": 8},  # Red
        "Musée": {"color": "#377eb8", "radius": 8},  # Blue
        "Bibliothèque": {"color": "#4daf4a", "radius": 8},  # Green
        "Théâtre": {"color": "#984ea3", "radius": 8},  # Purple
        "Cinéma": {"color": "#ff7f00", "radius": 8},  # Orange
        "Conservatoire": {"color": "#ffff33", "radius": 8},  # Yellow
        "Scène": {"color": "#a65628", "radius": 8},  # Brown
        "Musique": {"color": "#f781bf", "radius": 8},  # Pink
        "Lieu archéologique": {"color": "#999999", "radius": 8},  # Gray
        "Service d'archives": {"color": "#a6cee3", "radius": 8},  # Light blue
        "Parc et jardin": {"color": "#b2df8a", "radius": 8},  # Light green
        "Espace protégé": {"color": "#fb9a99", "radius": 8},  # Light red
        "Spectacle vivant": {"color": "#fdbf6f", "radius": 8},  # Light orange
        "Pluridisciplinaire": {"color": "#cab2d6", "radius": 8},  # Light purple
        "Cinéma, audiovisuel": {"color": "#ff7f00", "radius": 8},  # Orange
        "Livre, littérature": {"color": "#4daf4a", "radius": 8},  # Green
    }
    
    # Prepare data for visualization
    if nom_commune:
        df = data[data["nom_commune"] == nom_commune].copy()
    else:
        df = data.copy()  # Use all data if no commune is selected
    
    # Create a summary dataframe for visualization
    viz_data = df.groupby(['categorie', 'type_infrastructure']).size().reset_index(name='count')
    
    type_colors = {key: TYPE_STYLES[key]["color"] for key in TYPE_STYLES}
    viz_data['color'] = viz_data['type_infrastructure'].map(type_colors)

    # Sunburst Chart
    fig_sunburst = px.sunburst(
        data_frame=viz_data,
        path=["categorie", "type_infrastructure"],
        values=(viz_data['count'] / viz_data['count'].sum()) * 100,
        color="type_infrastructure",
        color_discrete_map=type_colors,
        hover_data={"count": True},
    )

    fig_sunburst.update_traces(
        texttemplate="%{label}<br>%{value:,.1f}%"
    )

    # If a commune is selected, add a bar chart and detailed information
    if nom_commune:
        # Bar Chart
        fig_bar = px.bar(
            viz_data.sort_values(by=["count", "categorie"], ascending=[False, True]),
            x="type_infrastructure",
            y="count",
            color="categorie",
            labels={"count": "Nombre d'équipements", "type_infrastructure": "Type d'équipement"},
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )

        fig_bar.update_traces(
            text=viz_data.sort_values(by=["count", "categorie"], ascending=[False, True])["count"],
            textposition="outside",
            insidetextfont=dict(size=20),
        )

        # Create a subplot with two rows and one column
        fig = make_subplots(
            rows=2,
            cols=1,
            row_heights=[0.7, 0.3],  # Adjust size ratio for sunburst and bar chart
            shared_xaxes=True,
            vertical_spacing=0.1,
            specs=[[{"type": "sunburst"}], [{"type": "bar"}]],
        )

        # Add traces to the subplots
        for trace in fig_sunburst.data:
            fig.add_trace(trace, row=1, col=1)
        for trace in fig_bar.data:
            fig.add_trace(trace, row=2, col=1)

        # Add Commune title annotation
        commune_title = f"<b>Commune:</b> {df['nom_commune'].iloc[0]}"
        fig.add_annotation(
            text=commune_title,  
            x=0.5,  
            y=1.15,  
            showarrow=False,
            font=dict(size=22, color="black", family="Arial"), 
            align="center", 
            xref="paper", 
            yref="paper"  
        )

        # Add Population annotation below the Commune title
        population_number = int(df['population'].iloc[0]) 
        fig.add_annotation(
            text=f"<b>Population:</b> {population_number:,}",  
            x=0.5,  
            y=1.09,  
            showarrow=False,
            font=dict(size=22, color="black", family="Arial"), 
            align="center", 
            xref="paper", 
            yref="paper"  
        )
    
    # If no specific commune is selected, show only the sunburst and summary for all communes
    elif nom_commune == 'Toutes les communes':
        fig = make_subplots(
            rows=1,
            cols=1,
            row_heights=[1],  
            vertical_spacing=0.1,
            specs=[[{"type": "sunburst"}]],
        )

        # Add Sunburst trace
        for trace in fig_sunburst.data:
            fig.add_trace(trace, row=1, col=1)

        # Add title for "Toute la France"
        fig.add_annotation(
            text="<b>Commune:</b> Toute la France",
            x=0.5,
            y=1.15,
            showarrow=False,
            font=dict(size=22, color="black", family="Arial"),
            align="center",
            xref="paper",
            yref="paper"
        )

        # Sum the population across all communes
        df_grouped = df.groupby('code_postal')['population'].unique().reset_index()
        total_population = int(df_grouped['population'].apply(lambda x: x[0]).sum())

        fig.add_annotation(
            text=f"<b>Population:</b> {total_population:,}",  
            x=0.5,  
            y=1.09,  
            showarrow=False,
            font=dict(size=22, color="black", family="Arial"), 
            align="center", 
            xref="paper", 
            yref="paper"  
        )
    
    else:
        fig = make_subplots(
            rows=1,
            cols=1,
            row_heights=[1],  
            vertical_spacing=0.1,
            specs=[[{"type": "sunburst"}]],
        )

        # Add Sunburst trace
        for trace in fig_sunburst.data:
            fig.add_trace(trace, row=1, col=1)

        # Add title for "Toute la France"
        fig.add_annotation(
            text="<b>Commune:</b> Toute la France",
            x=0.5,
            y=1.15,
            showarrow=False,
            font=dict(size=22, color="black", family="Arial"),
            align="center",
            xref="paper",
            yref="paper"
        )

        # Sum the population across all communes
        df_grouped = df.groupby('code_postal')['population'].unique().reset_index()
        total_population = int(df_grouped['population'].apply(lambda x: x[0]).sum())

        fig.add_annotation(
            text=f"<b>Population:</b> {total_population:,}",  
            x=0.5,  
            y=1.09,  
            showarrow=False,
            font=dict(size=22, color="black", family="Arial"), 
            align="center", 
            xref="paper", 
            yref="paper"  
        )

    # Update layout for the entire figure
    fig.update_layout(
        title="",
        margin=dict(t=80, l=50, r=50, b=50),
        title_font=dict(
            family="Arial, sans-serif",  
            size=22,  
            color="black"  
        ),
        font=dict(
            family="Arial, sans-serif",  
            size=14,  
            color="black" 
        ),
        height=600,
        width=500, 
        showlegend=True, 
        legend=dict(
            orientation="h",  
            yanchor="top",  
            y=-0.2,  
            xanchor="center", 
            x=0.5 
        )
    )

    return fig