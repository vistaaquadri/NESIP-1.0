import streamlit as st
import base64
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import pi
import plotly.express as px


# Function to load and display the logo with text
def render_logo():
    logo_path = "logo.png"  # Update this path to the correct logo file
    with open(logo_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    return f'<div style="display: flex; align-items: center;">' \
           f'<img src="data:image/png;base64,{encoded}" style="height:40px; margin-right:10px;">' \
           f'<span style="font-size: 18px; font-weight: bold; color: #06266E;">Vista | Advisory | Partners</span>' \
           f'</div>'


# Function to encode image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()





# Get base64-encoded image
nigeria_map = get_base64_image("nigeria_map.png")

# Encode each image
coat_of_arm = get_base64_image("nigeria_coat_of_arm.png")
ministry_of_power = get_base64_image("ministry_of_power.png")
rea = get_base64_image("rea.png")
world_bank = get_base64_image("world_bank.png")
vista_logo  = get_base64_image("vista_image.png")

# Function to create Radar Chart
def create_radar_chart(categories, values, max_value):
    num_vars = len(categories)
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]
    values += values[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Category Labels (adjusted to prevent overlap inside)
    for i, (angle, label, value) in enumerate(zip(angles[:-1], categories, values[:-1])):
        ha = "left" if angle < pi else "right"
        ax.text(angle, max_value + 0.5, f"{label} ({value})", horizontalalignment=ha, fontsize=9, fontweight="bold")

    ax.set_rlabel_position(0)
    plt.yticks(range(1, max_value+1), ["1", "2", "3", "4", "5"], color="grey", size=10)
    plt.ylim(0, max_value)

    # Plot radar chart with semi-transparent fill
    ax.plot(angles, values, linewidth=2, linestyle='solid', color='#1E3A8A')
    ax.fill(angles, values, color='#1E3A8A', alpha=0.3)  # Adjusted transparency

    # Legend with box format
    legend_labels = {
        "0": "Not Initiated",
        "1": "Early Stage",
        "2": "Developing",
        "3": "Progressing",
        "4": "Advanced",
        "5": "Optimized"
    }

    # Creating custom legend handles with styled boxes
    legend_handles = [plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#1E3A8A', markersize=6, label=f"  {k}  {v}  ") for k, v in legend_labels.items()]
    
    # Adjust legend styling to match the desired layout
    ax.legend(handles=legend_handles, loc='upper center', bbox_to_anchor=(0.5, -0.2), fontsize=9, title=None, ncol=3, frameon=False, handletextpad=2)

    return fig



# Example usage
categories = ["Policy", "Infrastructure", "Funding", "Capacity", "Data"]
values = [2, 3, 3, 2, 0]
max_value = 5

create_radar_chart(categories, values, max_value)
plt.show()


# Custom CSS to style the UI
def set_custom_css():
    st.markdown(
        """
        <style>
            .navbar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 20px;
                background-color: white;
                border-bottom: 1px solid #ddd;
            }
            .divider {
                border-bottom: 1px solid #ddd;                
            }
            .nav-items a {
                margin-left: 20px;
                text-decoration: none;
                color: #3A5894;
                font-weight: bold;
                font-size: 16px;
            }
            .content {
                text-align: left;
                padding: 50px;
                max-width: 800px;
            }
            .content h1 {
                color: #06266E;
                font-size: 32px;
                font-weight: bold;
            }
            .content p {
                color: #555;
                font-size: 16px;
                line-height: 1.6;
            }
            .stakeholder-container {
                text-align: center;
                font-size: 20px;
                font-weight: bold;
                color: #06266E;
                margin-top: 30px;
            }
            .stakeholder-box {
                display: inline-block;
                background: #F8F9FA;
                padding: 20px;
                margin: 10px;
                border-radius: 10px;
                width: 200px;
                text-align: center;
            }
            .logo-container {
                display: flex;
                justify-content: center;
                margin-top: 30px;
            }
            .logo-container img {
                height: 50px;
                margin: 0 15px;
            }

            .logo-container_1 {
                display: flex;
                justify-content: center;
                margin-top: 10px;
            }
            .logo-container_1 img {
                height: 50px;
                margin: 0 15px;
            }
            ############################################
            .stakeholder-container {
                text-align: center;
                font-size: 20px;
                font-weight: bold;
                color: #06266E;
                margin-top: 30px;
            }
            .stakeholder-count {
                text-align: center;
                font-size: 80px;
                font-weight: bold;
                color: #06266E;
            }
            .stakeholder-box {
                background: #f3f9ff;
                padding: 20px;
                margin: 10px auto;
                border-radius: 10px;
                text-align: center;
                width: 180px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            }
            .connector {
                border-top: 2px dotted #06266E;
                width: 50px;
                height: 20px;
                margin: auto;
            }
            .map-container {
                text-align: center;
            }

        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    st.set_page_config(page_title="NESIP Dashboard", layout="wide")
    set_custom_css()
    
    # Navbar layout
    st.markdown(
        f"""
        <div class='navbar'>
            <div>{render_logo()}</div>
            <div class='nav-items'>
                <a href='#'>Stakeholders</a>
                <a href='#'>Readiness</a>
                <a href='#'>Access</a>
                <a href='#'>About</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Main content
    st.markdown(
        """
        <div class='content'>
            <h1>National Electrification Strategy and Implementation Plan (NESIP)</h1>
            <p>The NESIP project develops Nigeria electrification strategy assessing sub-national implementation 
            of the Electricity Act of 2023 through stakeholders engagement to evaluate policy, funding, 
            infrastructure, capacity and data readiness as well as energy access for residential households across 
            all 36 states and the FCT.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    

    # Two-column Layout (Stakeholder Summary + Map)
    col1, col2 = st.columns([1, 1])  # Equal width columns

    with col1:
        st.markdown("<div class='stakeholder-container'>Total number of Stakeholders</div>", unsafe_allow_html=True)
        st.markdown("<div class='stakeholder-count'>146</div>", unsafe_allow_html=True)

        # Stakeholder Categories
        st.markdown("<div class='connector'></div>", unsafe_allow_html=True)
        colA, colB, colC = st.columns(3)

        with colA:
            st.markdown("<div class='stakeholder-box'><div>Total number of Stakeholder (Federal)</div><h2>32</h2></div>", unsafe_allow_html=True)
        with colB:
            st.markdown("<div class='stakeholder-box'><div>Total number of Stakeholder (State)</div><h2>73</h2></div>", unsafe_allow_html=True)
        with colC:
            st.markdown("<div class='stakeholder-box'><div>Total number of Stakeholder (Others)</div><h2>6</h2></div>", unsafe_allow_html=True)
        

        # Partner Logos
        st.markdown(
            f"""
            <div class='logo-container' style="display: flex; justify-content: center; gap: 20px;">
                <img src="data:image/png;base64,{coat_of_arm}" style="width: 50px; border-radius: 10px;">
                <img src="data:image/png;base64,{ministry_of_power}" style="width: 50px; border-radius: 10px;">
                <img src="data:image/png;base64,{rea}" style="width: 50px; border-radius: 10px;">
                <img src="data:image/png;base64,{world_bank}" style="width: 50px; border-radius: 10px;">
            </div>
            """,
            unsafe_allow_html=True
        )



    # Map on the Right
    with col2:
        st.markdown("<div class='map-container'><h3>Stakeholder Engagement Across Nigeria</h3></div>", unsafe_allow_html=True)
        
        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{nigeria_map}" alt="Engagement Status Across States"
                    style="width: 90%; max-width: 500px; border-radius: 10px;">
                <p style="font-size: 14px; color: #555;">Engagement Status Across States</p>
            </div>
            """,
            unsafe_allow_html=True
        )

       # Main content
    st.markdown(
        """
        <div class='divider'>
        </div>
        """,
        unsafe_allow_html=True
    )
    


####

    # Two-column Layout (Stakeholder Summary + Map)
    col1, col2 = st.columns([1, 1])  # Equal width columns

    with col1:
            
        # Readiness Section
        st.markdown("### Readiness", unsafe_allow_html=True)
        categories = ['Policy', 'Infrastructure', 'Funding', 'Capacity', 'Data']
        values = [2, 3, 3, 2, 0]  # Example readiness scores
        max_value = 5
        fig = create_radar_chart(categories, values, max_value)
        st.pyplot(fig)
        


    with col2:
        # Readiness Assessments
        st.markdown("""
        <style>
        .readiness-box { display: flex; align-items: center; background-color: #F8F9FC;
            padding: 15px; border-radius: 10px; margin-bottom: 10px; }
        .readiness-icon { width: 15px; height: 15px; margin-right: 15px; }
        .readiness-text { flex: 1; }
        </style>
        """, unsafe_allow_html=True)


        assessments = {
            "Policy Assessment": "Assesses the degree to which the state's policies are ready to support the implementation of the Electricity Act.",
            "Energy Access Assessment": "Seeks to understand the availability, duration, and affordability of electricity in the States.",
            "Funding and Investment Assessment": "Evaluates the state's commitment to funding electrification projects and securing private sector participation.",
            "Infrastructure Readiness Assessment": "Assesses the current state of physical infrastructure and readiness to integrate new technologies.",
            "Capacity Readiness Assessment": "Evaluates the state's ability to develop electrification projects.",
            "Data Readiness Assessment": "Evaluates the availability and quality of data for informed decision-making at a state level."
        }

        for title, description in assessments.items():
            st.markdown(f"""
            <div class='readiness-box'>
                <img class='readiness-icon' src='https://img.icons8.com/ios-filled/50/1E3A8A/info.png'/>
                <div class='readiness-text'><b>{title}</b><br>{description}</div>
            </div>
            """, unsafe_allow_html=True)

    ####


       # Main content
    st.markdown(
        """
        <div class='divider'>
        </div>
        """,
        unsafe_allow_html=True
    )
    




# energy access

    # Custom CSS for styling the metric cards
    st.markdown("""
        <style>
            .metric-card {
                padding: 20px;
                border-radius: 10px;
                color: white;
                margin: 20px;
                text-align: left;
                font-weight: bold;
                font-size: 20px;
            }
            .green {background-color: #6fcf97;}
            .blue {background-color: #6c80ff;}
            .orange {background-color: #f4a261;}
            .dark-blue {background-color: #142850;}
        </style>
    """, unsafe_allow_html=True)

    # Dashboard Title
    st.markdown("## Energy Access")


    # Metrics Row
    col1, col2 = st.columns(2)

    with col1:
        colA, colB = st.columns(2)

        with colA:

           st.markdown('<div class="metric-card green"> <p>49%<br><span style="font-size:14px;">Electrification Rate</span></p></div>', unsafe_allow_html=True)

           st.markdown('<div class="metric-card orange"> <p>N 2,000<br><span style="font-size:14px;">Average monthly Spend per household</span></p></div>', unsafe_allow_html=True)
        
        with colB:
           st.markdown('<div class="metric-card blue"> <p>290 kW<br><span style="font-size:14px;">Average capacity per household</span></p></div>', unsafe_allow_html=True)
           
           st.markdown('<div class="metric-card dark-blue"> <p>3 Hrs<br><span style="font-size:14px;">Disruption per week</span></p></div>', unsafe_allow_html=True)
        
    with col2:
        # Bar Chart Data
        data = {
            "Tier": ["Tier 0", "Tier 1", "Tier 2", "Tier 3", "Tier 4", "Tier 5"],
            "Percentage": [17, 20, 76, 40, 60, 36],
            "Color": ["#d9534f", "#f4a261", "#f4b661", "#fae28c", "#8fcf97", "#317873"]
        }
        df = pd.DataFrame(data)

        # Create Bar Chart
        fig = px.bar(df, x="Tier", y="Percentage", text="Percentage", color="Tier",
                    color_discrete_map={t: c for t, c in zip(df["Tier"], df["Color"])},
                    labels={"Percentage": "% of Households"})
        fig.update_traces(textposition="outside", showlegend=False)  # Remove legend
        fig.update_layout(yaxis=dict(title="% of Households"))

        # Display Bar Chart
        st.plotly_chart(fig, use_container_width=True)

        # Explanatory Text
        st.markdown("""
        ###### Percentage of households represented in each Tier of energy access across the country
        The World Bank’s Multi-Tier Framework (MTF) for Energy Access is a comprehensive approach to measuring energy access beyond a simple “yes” or “no” binary. It categorizes access into five tiers (Tier 0 to Tier 5) based on attributes like capacity, duration, reliability, affordability, legality, quality, and safety. Lower tiers (0-2) indicate limited access, such as solar lanterns or intermittent grid supply, while higher tiers (3-5) represent reliable, affordable, and high-capacity electricity for productive use.
        """)


       # Main content
    st.markdown(
        """
        <div class='divider'>
        </div>
        """,
        unsafe_allow_html=True
    )


    # Footer with logo

    st.markdown(
        f"""
        <div class='logo-container_1' style="display: flex; justify-content: center; gap: 5px;">
            <img src="data:image/png;base64,{vista_logo}" style="width: 250px; height: 65px; border-radius: 10px;">
        </div>
        """,
        unsafe_allow_html=True
    )



if __name__ == "__main__":
    main()




