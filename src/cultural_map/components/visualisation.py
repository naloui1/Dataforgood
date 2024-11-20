import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def creating_vusualisation(data: pd.DataFrame, nom_commune: str) -> go.Figure:
    df = data[
        data["Commune"] == nom_commune
    ]  # Using 'Commune' as per the CSV structure

    # Sunburst Chart
    fig_sunburst = px.sunburst(
        data_frame=df,
        path=["categorie", "Type équipement ou lieu"],
        values=(df["count"] / df["count"].sum()) * 100,
        color="Type équipement ou lieu",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hover_data={"count": False},
    )

    fig_sunburst.update_traces(texttemplate="%{label}<br>%{value:,.1f}%")

    # Bar Chart
    fig_bar = px.bar(
        df.sort_values(by=["count", "categorie"], ascending=[False, True]),
        x="Type équipement ou lieu",
        y="count",
        color="categorie",
        labels={"count": "Event Count", "Type équipement ou lieu": "Equipment Type"},
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )

    fig_bar.update_traces(
        text=df.sort_values(by=["count", "categorie"], ascending=[False, True])[
            "count"
        ],
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

    # Add sunburst and bar chart traces to the subplot
    for trace in fig_sunburst["data"]:
        fig.add_trace(trace, row=1, col=1)

    for trace in fig_bar["data"]:
        fig.add_trace(trace, row=2, col=1)

    # Add Commune title annotation
    commune_title = f"<b>Commune:</b> {df['Commune'].iloc[0]}"  # Using 'Commune' as per the CSV structure
    fig.add_annotation(
        text=commune_title,
        x=0.5,
        y=1.15,
        showarrow=False,
        font=dict(size=22, color="black", family="Arial"),
        align="center",
        xref="paper",
        yref="paper",
    )

    # Add Population annotation below the Commune title
    population_number = int(df["PTOT"].iloc[0])
    fig.add_annotation(
        text=f"<b>Population:</b> {population_number:,}",
        x=0.5,
        y=1.09,
        showarrow=False,
        font=dict(size=22, color="black", family="Arial"),
        align="center",
        xref="paper",
        yref="paper",
    )

    # Update layout for the entire figure
    fig.update_layout(
        margin=dict(t=80, l=50, r=50, b=50),
        title_font=dict(family="Arial, sans-serif", size=22, color="black"),
        font=dict(family="Arial, sans-serif", size=14, color="black"),
        height=600,
        width=500,
        showlegend=True,
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
    )

    return fig
