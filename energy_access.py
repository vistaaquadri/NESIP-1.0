import streamlit as st
import pandas as pd

# Define the data
headers = ["Aspects", "Tier 0", "Tier 1", "Tier 2", "Tier 3", "Tier 4", "Tier 5"]
data = [
    ["Capacity", "No electricity", "Very low power (> 3W)", "Low power (> 50W)", "Medium power (> 200 W)", "High power (> 800W)", "> 2KW"],
    ["Duration and availability", "< 4 hours", "4-8 hours", "8-16 hours", "16-22 hours", "> 22 hours"],
    ["Reliability", "", "Unreliable supply with frequent outages", "", "Max 14 disruptions per week", "Max 3 disruptions per week"],
    ["Quality", "Poor Quality (Damages or cannot operate appliances)", "", "Quality can support only basic appliances", "Good quality of energy supply, Voltage does not affect use of appliances", ""],
    ["Affordability", "Unaffordable", "", "Cost of standard consumption package is less than 15% of household income per year", "", ""],
    ["Legality", "Illegal connection", "", "Legal connection, with improvements in service quality", "", ""],
    ["Health and Safety", "Serious or fatal accidents due to electricity connection", "", "", "", "Absence of past accidents and perception of high risk in the future"]
]

# Convert to DataFrame
df = pd.DataFrame(data, columns=headers)

# Fill missing values to avoid issues with applying styles
df = df.fillna("")

# Define color mapping for each tier
colors = {
    "Tier 0": "background-color: #d62728; color: white;",  # Red
    "Tier 1": "background-color: #ff9900; color: black;",  # Orange
    "Tier 2": "background-color: #ffcc00; color: black;",  # Yellow
    "Tier 3": "background-color: #a1d99b; color: black;",  # Light green
    "Tier 4": "background-color: #238b45; color: white;",  # Dark green
    "Tier 5": "background-color: #00441b; color: white;"   # Deep green
}

# Function to apply styles based on tier labels
def style_table(val):
    if isinstance(val, str):  # Ensure val is a string before checking
        for tier, style in colors.items():
            if tier in val:
                return style
    return ""

# Streamlit App
st.title("Nigeria’s New Multi-Tiered Electricity Framework")
st.markdown("This table shows the classification of electricity supply in Nigeria based on different tiers.")

# Display styled dataframe
st.dataframe(df.style.applymap(style_table))
