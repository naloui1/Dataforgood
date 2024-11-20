from setuptools import setup, find_packages

setup(
    name="cultural_map",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "streamlit",
        "folium",
        "pandas",
        "streamlit-folium"
    ],
)
