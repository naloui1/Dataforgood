"""Data loading and processing functionality."""

import pandas as pd
import streamlit as st

@st.cache_data
def load_cultural_data():
    """Load and cache the cultural infrastructure data."""
    return pd.read_csv("data/cultural_data.csv")

@st.cache_data
def load_heatmap_data():
    """Load and cache the heatmap data."""
    return pd.read_csv("data/heatmap_data.csv")

def filter_data(df, selected_categories=None, selected_types=None, selected_commune=None):
    """
    Filter the dataframe based on selected criteria.
    
    Args:
        df (pd.DataFrame): The input dataframe
        selected_categories (list): List of selected categories
        selected_types (list): List of selected infrastructure types
        selected_commune (str): Selected commune name
        
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    filtered_df = df.copy()
    
    if selected_categories:
        filtered_df = filtered_df[filtered_df["categorie"].isin(selected_categories)]
    if selected_types:
        filtered_df = filtered_df[filtered_df["type_infrastructure"].isin(selected_types)]
    if selected_commune:
        filtered_df = filtered_df[filtered_df["nom_commune"] == selected_commune]
        
    return filtered_df

def get_unique_values(df):
    """Get unique values for filtering options."""
    return {
        "communes": sorted(df["nom_commune"].unique()),
        "categories": sorted(df["categorie"].unique()),
        "types": sorted(df["type_infrastructure"].unique())
    }
