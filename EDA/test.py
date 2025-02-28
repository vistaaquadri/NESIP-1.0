import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set page layout
st.set_page_config(layout="wide")

# Title
st.title("Data Collection Dashboard")

# Summary Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="States Interviewed", value="7 out of 37", delta="+10.80%")

with col2:
    st.metric(label="Questionnaire Filed", value="3 out of 37", delta="+10.80%")

with col3:
    st.metric(label="Desktop Data", value="30 out of 37", delta="+10.80%")

# Progress Bar
st.subheader("Progress Bar")
progress_value = 49
st.progress(progress_value / 100)
st.write(f"**{progress_value}%** - February 28th, 2025")

# Geospatial Heatmap
st.subheader("Geospatial Heatmap")
# Generate random latitude and longitude data for demo purposes
latitudes = np.random.uniform(4.0, 14.0, 10)
longitudes = np.random.uniform(3.0, 15.0, 10)
df_map = pd.DataFrame({'Latitude': latitudes, 'Longitude': longitudes})

fig = px.scatter_mapbox(df_map, lat="Latitude", lon="Longitude", zoom=5, height=400)
fig.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig)

# First Table: Data Collection Status
st.subheader("Data Collection Status")

data_collection = pd.DataFrame({
    "State": ["Lagos", "Ogun", "Enugu", "Delta", "Kano", "Bauchi"],
    "Region": ["South West", "South West", "South East", "South South", "North West", "North Central"],
    "Interviewed": ["Yes"] * 6,
    "Questionnaire Filed": ["Yes", "In progress", "In progress", "In progress", "Yes", "Yes"],
    "Desktop Data": ["Yes"] * 6
})

st.dataframe(data_collection.style.applymap(lambda x: "background-color: yellow" if x == "In progress" else "background-color: lightgreen"))

# Second Table: Policy & Infrastructure Assessment
st.subheader("Policy & Infrastructure Assessment")

policy_data = pd.DataFrame({
    "State": ["Lagos", "Ogun", "Enugu", "Delta", "Kano", "Bauchi"],
    "Region": ["South West", "South West", "South East", "South South", "North West", "North Central"],
    "Policy": ["Yes"] * 6,
    "Infrastructure": ["Yes", "In progress", "In progress", "In progress", "Yes", "Yes"],
    "Capacity": ["In progress", "In progress", "In progress", "In progress", "Yes", "Yes"],
    "Funding & Investment": ["Yes"] * 6,
    "Data": ["Yes"] * 6
})

st.dataframe(policy_data.style.applymap(lambda x: "background-color: yellow" if x == "In progress" else "background-color: lightgreen"))
