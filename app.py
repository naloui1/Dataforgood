"""Main entry point for the Cultural Map application."""

import sys
from pathlib import Path
import streamlit as st
import folium
from folium import plugins
import pandas as pd
from streamlit_folium import folium_static

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

# Now we can import our module
from cultural_map.core import main

if __name__ == "__main__":
    main()
