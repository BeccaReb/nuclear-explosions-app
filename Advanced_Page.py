import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static
import plotly.express as px
import requests


def load_data():
    df = pd.read_csv("nuclear_explosions.csv")
    df['Average Yield'] = (df['Data.Yeild.Lower'] + df['Data.Yeild.Upper']) / 2
    df['WEAPON SOURCE COUNTRY'] = df['WEAPON SOURCE COUNTRY'].str.strip()
    df = df.rename(columns={
        "Location.Cordinates.Latitude": "Latitude",
        "Location.Cordinates.Longitude": "Longitude"
    })
    return df


def show_advanced_page():
    st.title("📊 Advanced Yield Visualizations")
    st.write("Nuclear yield measures the explosive power of a nuclear detonation in kilotons (kt) of TNT equivalent.")

    df = load_data()

    # [EXTRA][DA6] Pivot table analysis
    st.subheader("Pivot Table Analysis")
    st.write("Average yield by country and year")
    pivot = pd.pivot_table(df, values='Average Yield',
                           index='WEAPON SOURCE COUNTRY',
                           columns='Date.Year',
                           aggfunc='mean')
    st.dataframe(pivot.style.background_gradient(cmap='Blues'))

    # [SEA1] Seaborn line plot
    st.subheader("Yield Trends Over Time")
    yearly_data = df.groupby('Date.Year')['Average Yield'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=yearly_data, x='Date.Year', y='Average Yield',
                 marker='o', color='red', ax=ax)
    ax.set_title('Average Nuclear Yield Over Time (1945-1998)')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Yield (kilotons)')
    ax.grid(True)
    st.pyplot(fig)

    # [SEA2] Seaborn boxplot
    st.subheader("Yield Distribution by Country")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df, x='WEAPON SOURCE COUNTRY', y='Average Yield',
                palette='viridis', ax=ax)
    ax.set_title('Nuclear Yield Distribution by Country')
    ax.set_xlabel('Country')
    ax.set_ylabel('Yield (kilotons)')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # [FOLIUM1] Marker map
    st.subheader("Nuclear Test Locations (Folium)")
    m1 = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=2)

    for idx, row in df.iterrows():
        folium.Marker(
            [row['Latitude'], row['Longitude']],
            popup=f"{row['Data.Name']} ({row['Date.Year']})",
            tooltip=f"Yield: {row['Average Yield']:.1f} kt"
        ).add_to(m1)

    folium_static(m1)

    # [EXTRA][PACKAGE] Plotly interactive chart
    st.subheader("Interactive Yield Visualization")
    fig = px.scatter(df, x='Date.Year', y='Average Yield',
                     color='WEAPON SOURCE COUNTRY',
                     size='Average Yield',
                     hover_data=['Data.Name', 'Location.Cordinates.Depth'],
                     title='Nuclear Test Yields Over Time')
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    show_advanced_page()