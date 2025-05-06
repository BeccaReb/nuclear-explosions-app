import streamlit as st
import pandas as pd
import pydeck as pdk

def show_map_page():
    st.title("🌍 Nuclear Explosions Map")
    st.write("Interactive map of nuclear tests 1945-1998")

    @st.cache_data
    def load_data():
        df = pd.read_csv("nuclear_explosions.csv")
        df = df.rename(columns={
            "Location.Cordinates.Latitude": "Latitude",
            "Location.Cordinates.Longitude": "Longitude",
            "Data.Yeild.Upper": "Yield"
        })
        df['Date'] = pd.to_datetime(df[['Date.Year', 'Date.Month', 'Date.Day']]
                                   .rename(columns={
                                       'Date.Year': 'year',
                                       'Date.Month': 'month',
                                       'Date.Day': 'day'
                                   }), errors='coerce')
        df = df.dropna(subset=["Latitude", "Longitude", "Yield"])
        return df

    df = load_data()

    st.sidebar.header("Map Settings")
    min_yield = st.sidebar.slider(
        "Minimum Yield (kilotons)",
        min_value=int(df["Yield"].min()),
        max_value=int(df["Yield"].max()),
        value=100
    )

    circle_scale = st.sidebar.slider(
        "Circle Size Scale",
        min_value=1,
        max_value=100,
        value=30,
        help="Adjust the size of the circles on the map"
    )

    filtered_df = df[df["Yield"] >= min_yield]

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered_df,
        get_position="[Longitude, Latitude]",
        get_color="[255, 100, 100, 180]",
        get_radius=f"Yield * {circle_scale / 50}",
        pickable=True,
        opacity=1,
        stroked=True,
        filled=True,
        radius_min_pixels=2,
        radius_max_pixels=100
    )

    tooltip = {
        "html": """
        <b>Name:</b> {Data.Name}<br/>
        <b>Country:</b> {WEAPON SOURCE COUNTRY}<br/>
        <b>Yield:</b> {Yield} kt<br/>
        <b>Date:</b> {Date:%Y-%m-%d}
        """,
        "style": {
            "backgroundColor": "#333333",
            "color": "white"
        }
    }

    view_state = pdk.ViewState(
        latitude=df["Latitude"].mean(),
        longitude=df["Longitude"].mean(),
        zoom=1
    )

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="mapbox://styles/mapbox/light-v10"
    ))

    st.caption("💡 Tip: Use the slider in the sidebar to adjust circle sizes")

    def show_table_page():
        st.title("Data Table View")

if __name__ == "__main__":
   show_table_page()