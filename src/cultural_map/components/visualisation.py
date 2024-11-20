import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def creating_visualisation(data: pd.DataFrame, nom_commune: str) -> go.Figure:
    # Prepare data for visualization
    df = data[data["nom_commune"] == nom_commune].copy()
    
    # Create a summary dataframe for visualization
    viz_data = df.groupby(['categorie', 'type_infrastructure']).size().reset_index(name='count')
    
    # Sunburst Chart
    fig_sunburst = px.sunburst(
        data_frame=viz_data,
        path=["categorie", "type_infrastructure"],
        values="count",
        color="type_infrastructure",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hover_data={"count": True},
    )

    fig_sunburst.update_traces(texttemplate="%{label}<br>%{value:,.0f}")

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

    # Update layout
    fig.update_layout(
        height=800,
        showlegend=False,
        title=f"Distribution des équipements culturels à {nom_commune}",
        title_x=0.5,
    )

    return fig
