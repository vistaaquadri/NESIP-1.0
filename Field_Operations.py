import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go
import gspread
from google.oauth2.service_account import Credentials

# Set page configuration
st.set_page_config(page_title="NESIP", layout="wide")


# Hide Streamlit footer and menu
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("")
st.sidebar.image("https://www.vista-advisory.com/wp-content/uploads/2024/07/image-18.png", width=150)


# Set up Google Sheets credentials
#def get_google_sheet(sheet_url, sheet_name):
#    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
#    credentials = Credentials.from_service_account_file("data/nesip-451109-d25b71f62e3b.json", scopes=scope)
#    client = gspread.authorize(credentials)

#    # Open Google Sheet by URL or Sheet name
#    spreadsheet = client.open_by_url(sheet_url)
#    worksheet = spreadsheet.worksheet(sheet_name)

    # Convert sheet to DataFrame
#    data = worksheet.get_all_records()
#    df = pd.DataFrame(data)
#    return df

# Streamlit app
st.title("NESIP")

#sheet_url = "https://docs.google.com/spreadsheets/d/1gCwYBWV_v0Ajuwfcive6yuqWcio_Ta0Bbad4IXzMz8w/edit#gid=0"
#sheet_ea_day = "0. Energy Access(LP)"
#sheet_ea_dump = "1. Energy Access Dump"
#sheet_ea_passed = "2. Energy Access(Passed)"
#sheet_ea_bad = "3. Energy Access(Bad)"

#energy_access_day = get_google_sheet(sheet_url, sheet_ea_day)
#ea_dump = get_google_sheet(sheet_url, sheet_ea_dump)
#ea_passed = get_google_sheet(sheet_url, sheet_ea_passed)
#ea_bad = get_google_sheet(sheet_url, sheet_ea_bad)

sheet_url = "data/data.xlsx"
sheet_ea_day = "0. Energy Access(LP)"
sheet_ea_dump = "1. Energy Access Dump"
sheet_ea_passed = "2. Energy Access(Passed)"
sheet_ea_bad = "3. Energy Access(Bad)"

energy_access_day = pd.read_excel(sheet_url, sheet_ea_day)
ea_dump = pd.read_excel(sheet_url, sheet_ea_dump)
ea_passed = pd.read_excel(sheet_url, sheet_ea_passed)
ea_bad = pd.read_excel(sheet_url, sheet_ea_bad)


#sampling_numbers 
sampling_sheet = "Sampling Numbers"
sampling_numbers = pd.read_excel(sheet_url, sampling_sheet)

##### data collection progress

# Create Urban_Collected and Rural_Collected based on "Area Description"
ea_passed["Urban_Collected"] = (ea_passed["Area Description"] == "Urban").astype(int)
ea_passed["Rural_Collected"] = (ea_passed["Area Description"] == "Rural").astype(int)

ea_passed = pd.DataFrame(ea_passed)

# Group by State and LGA, sum Urban and Rural collected
summary_collected = ea_passed.groupby(["State", "LGA"])[["Urban_Collected", "Rural_Collected"]].sum().reset_index()

	
# Outer Join on 'LGA'
merged_collection_summ = pd.merge(sampling_numbers, summary_collected, on=['State', 'LGA'] , how='outer')

merged_collection_summ.fillna(0, inplace=True)

# Calculate Completion Percentage per LGA
merged_collection_summ["Urban_Completion"] = (merged_collection_summ["Urban_Collected"] / merged_collection_summ["Urban_Target"]) * 100
merged_collection_summ["Rural_Completion"] = (merged_collection_summ["Rural_Collected"] / merged_collection_summ["Rural_Target"]) * 100

# Aggregate to State Level
state_completion = merged_collection_summ.groupby("State").agg(
    Urban_Completion=("Urban_Completion", "mean"),
    Rural_Completion=("Rural_Completion", "mean")
).reset_index()

# Calculate Overall Completion per State
state_completion["Overall_Completion"] = round((state_completion["Urban_Completion"] + state_completion["Rural_Completion"]) / 2,0)

state_data = state_completion.copy()

#### deficit to calculate percentage completion

# Calculate the Deficit (Data not yet collected)
merged_collection_summ["Urban_Deficit"] = merged_collection_summ["Urban_Target"] - merged_collection_summ["Urban_Collected"]
merged_collection_summ["Rural_Deficit"] = merged_collection_summ["Rural_Target"] - merged_collection_summ["Rural_Collected"]

# If collected >= target, set deficit to 0 (i.e., already completed)
merged_collection_summ["Urban_Deficit"] = merged_collection_summ["Urban_Deficit"].apply(lambda x: x if x > 0 else 0)
merged_collection_summ["Rural_Deficit"] = merged_collection_summ["Rural_Deficit"].apply(lambda x: x if x > 0 else 0)

# Sum the deficits and targets across all states and LGAs
total_urban_deficit = merged_collection_summ["Urban_Deficit"].sum()
total_rural_deficit = merged_collection_summ["Rural_Deficit"].sum()

total_urban_target = merged_collection_summ["Urban_Target"].sum()
total_rural_target = merged_collection_summ["Rural_Target"].sum()

# Total Deficit (Urban + Rural)
total_deficit = total_urban_deficit + total_rural_deficit

# Total Target (Urban + Rural)
total_target = total_urban_target + total_rural_target

# Overall Percentage Completion
overall_completion = round((1 - (total_deficit / total_target)) * 100,2)
perc_deficit =  round((100  - overall_completion), 2)

############################################################################
# completion date
urban_target = sampling_numbers['Urban_Target'].sum()
rural_target = sampling_numbers['Rural_Target'].sum()

total_target = urban_target + rural_target 

current_total  = ea_passed.shape[0]
# Assuming ea_passed is your DataFrame
ea_passed['Timestamp'] = pd.to_datetime(ea_passed['Timestamp'], format='%m/%d/%Y %H:%M:%S')
ea_passed['date'] = ea_passed['Timestamp'].dt.date

# Daily collection count
daily_collection_combined = ea_passed.groupby('date').size()

# Average daily collection
daily_avg_combined = daily_collection_combined.mean()

# Exclude the latest date
latest_date = daily_collection_combined.index.max()
daily_collection_excluding_latest = daily_collection_combined[daily_collection_combined.index != latest_date]

# Average daily collection (excluding the latest date)
prev_daily_avg_combined = daily_collection_excluding_latest.mean()

perc_inc_dec_avg_col = round((daily_avg_combined - prev_daily_avg_combined)/prev_daily_avg_combined * 100, 0)

# Remaining surveys to be collected
remaining_total = max(total_target - current_total, 0)

# Calculate estimated completion time
days_to_complete = remaining_total / daily_avg_combined  # if daily_avg_combined > 0 else float('inf')

# Estimated completion date
today = datetime.date.today()
completion_date = today + datetime.timedelta(days=round(days_to_complete))

completion_date_text = completion_date.strftime('%Y-%m-%d')




# Tabs for state and vendor
tab1, tab2 = st.tabs(["Energy Access", "State Readiness"])


## GET ALL METRICS
total_states = 37
states_done = len(state_data[state_data['Overall_Completion'] >= 100])
state_per_cmptd = round((states_done/total_states) *100, 2)
states_visited = f"{ea_passed['State'].nunique()} states visited"




# GOOD AND BAD DATA SUMMARY
good_bad_summary = ea_dump.pivot_table(
    index="State",
    columns="vista_remark",
    aggfunc="size",
    fill_value=0
).reset_index()

# Ensure "Good" and "Bad" columns are present even if some are missing
if "Good" not in good_bad_summary.columns:
    good_bad_summary["Good"] = 0
if "Bad" not in good_bad_summary.columns:
    good_bad_summary["Bad"] = 0

# Reorder columns for readability
good_bad_summary = good_bad_summary[['State', 'Good', 'Bad']]
good_bad_summary.rename(columns={"Good": "Clean Data", "Bad": "Inconsistent Data"}, inplace=True)

total_clean_records = good_bad_summary["Clean Data"].sum()
total_bad_records = good_bad_summary["Inconsistent Data"].sum()


with tab1:
    # Overview Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("States Completed", f"{states_done} of {total_states}", states_visited)
    col2.metric("Data Collected", f"{total_target} ({current_total})", "")
    col3.metric("Avg. Daily Collection", f"{daily_avg_combined} per day", f"{perc_inc_dec_avg_col} %")
    col4.metric("Expected completion day", f"{completion_date_text}", "")

    # Map View and Progress Bar
    col1, col2 = st.columns([1, 2])


    # Ensure Geolocation is string and split into lat/lon
    ea_passed['Geolocation'] = ea_passed['Geolocation'].astype(str)
    ea_passed[['lat', 'lon']] = ea_passed['Geolocation'].str.split(',', expand=True)
    ea_passed['lat'] = pd.to_numeric(ea_passed['lat'], errors='coerce')
    ea_passed['lon'] = pd.to_numeric(ea_passed['lon'], errors='coerce')
    ea_passed = ea_passed.dropna(subset=['lat', 'lon'])

 

    with col1:
    # State Dropdown

        st.subheader("Progress Bar")




    with col2:       


        st.subheader("Map View")

        col1A, col2A = st.columns(2)     

        with col1A:
            selected_state = st.selectbox("Select State", options=["All"] + sorted(ea_passed['State'].unique()))

        with col2A:

            # LGA Dropdown (depends on State)
            if selected_state == "All":
                lga_options = ["All"] + sorted(ea_passed['LGA'].unique())
            else:
                lga_options = ["All"] + sorted(ea_passed[ea_passed['State'] == selected_state]['LGA'].unique())

            selected_lga = st.selectbox("Select LGA", options=lga_options) 
            # Filter Data
            filtered_data = ea_passed.copy()

            if selected_state != "All":
                filtered_data = filtered_data[filtered_data['State'] == selected_state]

            if selected_lga != "All":
                filtered_data = filtered_data[filtered_data['LGA'] == selected_lga]

    with col1:
    # State Dropdown

        fig_progress = go.Figure(go.Pie(values=[f"{overall_completion}", f"{perc_deficit}"], labels=["Completed", "Remaining"],
                                        hole=0.6, marker_colors=["blue", "lightgrey"]))
        fig_progress.update_traces(textinfo='none')
        fig_progress.update_layout(showlegend=False, annotations=[dict(text= f"{overall_completion:.2f}%" , x=0.5, y=0.5, font_size=20, showarrow=False)], width=600, height=600 )
        st.plotly_chart(fig_progress, use_container_width=True)

    with col2:
    # State Dropdown

        # Plot Map
        st.map(filtered_data[['lat', 'lon']])







    # Plotly bar chart showing progress
    fig = go.Figure()

    import plotly.graph_objects as go
    import streamlit as st

    fig = go.Figure()

    for index, row in state_data.iterrows():
        fig.add_trace(go.Bar(
            x=[row['State']],
            y=[100],
            name='(Target)',
            marker_color='lightgrey',
            width=0.4,
            offset=-0.2,
            showlegend=(index == 0)  # Show legend only once
        ))
        fig.add_trace(go.Bar(
            x=[row['State']],
            y=[row['Urban_Completion']],
            name='Urban (Collected)',
            marker_color='blue',
            width=0.4,
            offset=-0.2,
            showlegend=(index == 0)
        ))

        fig.add_trace(go.Bar(
            x=[row['State']],
            y=[100],
            name='(Target)',
            marker_color='lightgrey',
            width=0.4,
            offset=0.2,
            showlegend=False  # Hide because same as urban target
        ))
        fig.add_trace(go.Bar(
            x=[row['State']],
            y=[row['Rural_Completion']],
            name='Rural (Collected)',
            marker_color='green',
            width=0.4,
            offset=0.2,
            showlegend=(index == 0)
        ))

    fig.update_layout(
        barmode='overlay',
        title="Completion Percentage by State",
        xaxis_title="State",
        yaxis_title="Completion Percentage",
        yaxis=dict(range=[0, 100]),
        legend_title="Legend"
    )

    st.plotly_chart(fig)



#################################


    # Data Summary
    colA,  colC = st.columns([2.5, 0.5])


    with colA:
        # Data Quality Analysis
        data_quality = {
            "Week": ["Week 1", "Week 2", "Week 3"],
            "Clean data": [59, 70, 96],
            "Bad data": [45, 89, 84]
        }
        
        df_quality = pd.DataFrame(data_quality)
        fig_quality = px.bar(good_bad_summary, x="State", y=["Clean Data",  "Inconsistent Data"], 
                            barmode="stack", title="Data Quality Analysis", color_discrete_map={
                                "Clean Data": "blue", "Inconsistent DataBad data": "red"
                            })
        st.plotly_chart(fig_quality, use_container_width=True)

    with colC:

        colC.metric("Total clean data", f"{total_clean_records}")
        colC.metric("Total Inconsistent data", f"{total_bad_records}")




with tab2:
    st.write("State Readiness Data summary would be published soon")




