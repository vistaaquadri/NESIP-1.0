import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder
from datetime import datetime
from PIL import Image


# Set page configuration
st.set_page_config(page_title="NESIP", layout="wide")

# Create two columns: one for the logo, one for the title
col1, col2 = st.columns([0.5, 6])  # Adjust column width ratio as needed

# Add logo to the left column
with col1:
    st.image("https://www.vista-advisory.com/wp-content/uploads/2024/07/image-18.png", width=100)

# Add title and motto to the right column
with col2:
    st.markdown("""
        <h3 style='margin-bottom: 0px;'>National Electrification Strategy And Implementation Plan</h3>
        <hr style='border:1px solid #ddd; margin: 5px 0;'>
        <p style='font-size: 14px; color: #555;'>Data collection Tracking Dashboard</p>
    """, unsafe_allow_html=True)


#read data 
dashboard_single_data = pd.read_csv('data/dashboard_data/dashboard_single_df.csv')
data_quality_summary_data = pd.read_csv('data/dashboard_data/data_quality_summary.csv')
expander_data = pd.read_csv('data/dashboard_data/expander_df.csv')
geospatial_data = pd.read_csv('data/dashboard_data/geospatial_df.csv')
state_lga_completion_data = pd.read_csv('data/dashboard_data/state_lga_completion_data.csv')
bad_data_trend_pivot = pd.read_csv('data/dashboard_data/bad_data_trend_pivot.csv')


best_performing_state = pd.read_csv('data/dashboard_data/top_5_states.csv')
least_performing_state = pd.read_csv('data/dashboard_data/BOTTOM_5_states.csv')
best_performing_enumerators = pd.read_csv('data/dashboard_data/top_enumerators.csv')
least_performing_enumerators = pd.read_csv('data/dashboard_data/bottom_enumerators.csv')

#state_collection_progress = pd.read_csv('data/dashboard_data/state_collection_progress.csv')
#state_readiness_progress = pd.read_csv('data/dashboard_data/state_readiness_progress.csv')


# Tabs for state and vendor
tab1, tab2 = st.tabs(["Energy Access", "State Readiness"])

# Custom CSS to style the tabs
st.markdown(
    """
    <style>
    div.stTabs [data-baseweb="tab-list"] {
        background-color: #1a3665;
        border-radius: 10px;
        padding: 5px;
    }
    div.stTabs [data-baseweb="tab"] {
        color: white;
        font-weight: bold;
    }
    div.stTabs [aria-selected="true"] {
        background-color: #1f5c94 !important;
        border-radius: 10px;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Ensure correct data type conversion
states_done = int(dashboard_single_data['states_done'][0])#updated
total_states = int(dashboard_single_data['total_states'][0])
states_visited = str(dashboard_single_data['states_visited'][0])
total_target = int(dashboard_single_data['total_target'][0])
current_total = int(dashboard_single_data['current_total'][0])
daily_avg_combined = int(dashboard_single_data['daily_avg_combined'][0])
perc_inc_dec_avg_col = int(dashboard_single_data['perc_inc_dec_avg_col'][0])
expected_completion_date = str(dashboard_single_data['expected_completion_date'][0])  # If it's a date, format it properly
completion_date_text = str(dashboard_single_data['completion_date_text'][0])
overall_completion = int(dashboard_single_data['overall_completion'][0])
perc_deficit = int(dashboard_single_data['perc_deficit'][0])

Daily_avg_expected = int(dashboard_single_data['Daily_avg_expected'])
perc_in_dec_collection = int(dashboard_single_data['perc_in_dec_collection'])


total_clean_records = int(dashboard_single_data['total_clean_records'][0])
total_bad_records = int(dashboard_single_data['total_bad_records'][0])

last_collection_count = int(dashboard_single_data['last_collection_count'][0])



with tab1:
    # Overview Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("States Completed", f"{states_done} of {total_states}", states_visited)


    #col1.metric("States Completed", f"0 of {total_states}", "12 States Visited")
    col2.metric("Data Collection", f"{total_target} Expected", f"{current_total} Collected")
    col3.metric("Avg. Daily Collection", f"{Daily_avg_expected} Expected per day", f"{daily_avg_combined} Avg Daily collection ({perc_in_dec_collection} %)")

    col4.metric("Expected completion day", f"{expected_completion_date}", f"{completion_date_text}")

    # Map View and Progress Bar
    col1, col2 = st.columns([1, 2])

    with col1:
    # State Dropdown

        st.subheader("Collection Progess")




    with col2:       


        st.subheader("Geospatial Spread")

        col1A, col2A = st.columns(2)     

        with col1A:
            selected_state = st.selectbox("Select State", options=["All"] + sorted(geospatial_data['State'].unique()))

        with col2A:

            # LGA Dropdown (depends on State)
            if selected_state == "All":
                lga_options = ["All"] + sorted(geospatial_data['LGA'].unique())
            else:
                lga_options = ["All"] + sorted(geospatial_data[geospatial_data['State'] == selected_state]['LGA'].unique())

            selected_lga = st.selectbox("Select LGA", options=lga_options) 
            # Filter Data
            filtered_data = geospatial_data.copy()

            if selected_state != "All":
                filtered_data = filtered_data[filtered_data['State'] == selected_state]

            if selected_lga != "All":
                filtered_data = filtered_data[filtered_data['LGA'] == selected_lga]

    with col1:
    # State Dropdown

        fig_progress = go.Figure(go.Pie(values=[f"{overall_completion}", f"{perc_deficit}"], labels=["Completed", "Remaining"],
                                        hole=0.6, marker_colors=["#1a3665", "lightgrey"]))
        fig_progress.update_traces(textinfo='none')
        fig_progress.update_layout(showlegend=False, annotations=[dict(text= f"{overall_completion:.2f}%" , x=0.5, y=0.5, font_size=20, showarrow=False)], width=600, height=600 )
        st.plotly_chart(fig_progress, use_container_width=True)

    with col2:
    # State Dropdown

        # Plot Map
        st.map(filtered_data[['lat', 'lon']])



    # Plotly bar chart showing progress
    fig = go.Figure()

    for index, row in state_lga_completion_data.iterrows():
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
            marker_color='#1a3665',
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
            marker_color='#6599cd',
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
        fig_quality = px.bar(data_quality_summary_data, x="State", y=["Clean Data",  "Inconsistent Data"], 
                            barmode="stack", title="Data Quality Analysis", color_discrete_map={
                                "Clean Data": "#1a3665", "Inconsistent Data": "#6599cd"
                            })
        st.plotly_chart(fig_quality, use_container_width=True)

    with colC:

        colC.metric("Total clean data (Collected vs sampling)", f"{total_clean_records} ({current_total})")
        colC.metric("Total Inconsistent data", f"{total_bad_records}")

        # Create Matplotlib figure
        fig, ax = plt.subplots(figsize=(8, 4))

        # Plotting
        ax.plot(bad_data_trend_pivot['Date'], bad_data_trend_pivot['Dropped Data'], marker='o', linestyle='-', color='black', linewidth=2)

        # Formatting Fixes
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Dropped Data", fontsize=12)
        ax.set_xticks(bad_data_trend_pivot['Date'])  
        ax.set_xticklabels(bad_data_trend_pivot['Date'].astype(str), rotation=45, ha="right")  
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Show plot in Streamlit
        st.pyplot(fig)


    # Alternatively, you can use st.container() if you need more complex layout or control
    with st.container():
        with st.expander('State and Enumerator Performance (Data Quality)', expanded=False):
            colA, colB, colC, colD = st.columns([2,2,2,2])
            
            with colA:
                st.write("Best Performing States")
                st.markdown(best_performing_state.to_html(escape=False, index=False), unsafe_allow_html=True)
    
            with colB:
                st.write("Least Performing States")
                st.markdown(least_performing_state.to_html(escape=False, index=False), unsafe_allow_html=True)

            with colC:
                st.write("Best Performing Enumerators")
                st.markdown(best_performing_enumerators.to_html(escape=False, index=False), unsafe_allow_html=True) 

            with colD:
                st.write("Least Performing Enumerators")
                st.markdown(least_performing_enumerators.to_html(escape=False, index=False), unsafe_allow_html=True)



    # Alternatively, you can use st.container() if you need more complex layout or control
    with st.container():
        with st.expander('Sampling Methodology Tracker', expanded=False):
            # Dropdown for state selection
            expander_data.columns = expander_data.columns.str.strip()
            state_options = expander_data["State"].unique().tolist()
            selected_state = st.selectbox("Select State(s)", ["All"] + state_options)

            # Filter LGA options based on selected state
            if selected_state == "All":
                lga_options = expander_data["LGA"].unique().tolist()
            else:
                lga_options = expander_data[expander_data["State"] == selected_state]["LGA"].unique().tolist()

            selected_lga = st.selectbox("Select LGA(s)", ["All"] + lga_options)

            # Filter dataframe based on selections
            filtered_df_summary = expander_data.copy()

            if selected_state != "All":
                filtered_df_summary = filtered_df_summary[filtered_df_summary["State"] == selected_state]

            if selected_lga != "All":
                filtered_df_summary = filtered_df_summary[filtered_df_summary["LGA"] == selected_lga]


                
            st.markdown(filtered_df_summary.to_html(escape=False, index=False), unsafe_allow_html=True)

            # Convert DataFrame to CSV
            csv = filtered_df_summary.to_csv(index=False).encode('utf-8')

            # Create a Download Button
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="progress.csv",
                mime="text/csv",
                key="download-csv"
            )




with tab2:
    st.write("State Readiness")

    ###################


