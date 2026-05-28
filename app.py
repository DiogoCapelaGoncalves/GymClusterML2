import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PHASE 1: APP CONFIG & DATA LOADING
# ==========================================
st.set_page_config(page_title="Gym Admin Insights", layout="wide", page_icon="🏋️‍♂️")

@st.cache_data
def load_data():
    # Make sure this matches the filename where you saved your final labeled dataset
    return pd.read_csv("gym_members_with_clusters.csv")

df = load_data()

# Mapping the cluster integers to your official custom names
cluster_names = {
    0: "Cluster 0 - The Studio Enthusiasts",
    1: "Cluster 1 - The Floor Casuals",
    2: "Cluster 2 - The Heavy Lifters"
}
df['Cluster_Name'] = df['Gym_Cluster'].map(cluster_names)

# ==========================================
# PHASE 2: APP HEADER & HIGH-LEVEL METRICS
# ==========================================
st.title("🏋️‍♂️ Gym Admin Dashboard")
st.markdown("Translate unsupervised machine learning segments into real-world business actions.")
st.write("---")

# Layout the 3 Core Tabs
tab1, tab2, tab3 = st.tabs(["📊 Gym Overview", "🎯 Persona Explorer", "🚀 Marketing Action"])

# ==========================================
# TAB 1: GLOBAL OVERVIEW
# ==========================================
with tab1:
    st.subheader("Current Facility Metrics")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Members Analyzed", f"{len(df):,}")
    col2.metric("Drink Subscription Rate", f"{(df['drink_abo'].mean() * 100):.1f}%")
    col3.metric("Sauna Utilization Rate", f"{(df['uses_sauna'].mean() * 100):.1f}%")
    
    st.write("---")
    
    # Plotly Distribution Chart
    st.subheader("Member Base Distribution")
    cluster_counts = df['Cluster_Name'].value_counts().reset_index()
    cluster_counts.columns = ['Persona', 'Count']
    
    fig = px.bar(cluster_counts, x='Persona', y='Count', 
                 color='Persona', title="Distribution of Personas Across the Gym",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 2: PERSONA EXPLORER
# ==========================================
with tab2:
    st.subheader("Explore Member Habits")
    selected_persona = st.selectbox("Select a Member Persona to Analyze:", options=list(cluster_names.values()))
    
    # Filter dataset for the selected cluster
    persona_df = df[df['Cluster_Name'] == selected_persona]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"### 📋 Profile Summary")
        if "Studio Enthusiasts" in selected_persona:
            st.markdown("""
            * **Training Habits:** Mostly attend Cardio and Mind/Body group classes. Prefer weekdays.
            * **Sauna Habits:** Standard facility usage (~50.8%).
            * **Retail Flavor Match:** Highly prefer **Orange** flavors.
            """)
        elif "Floor Casuals" in selected_persona:
            st.markdown("""
            * **Training Habits:** Your independent floor trainers. Do not attend group classes at all.
            * **Sauna Habits:** Lowest facility usage (~47.5%).
            * **Retail Flavor Match:** Higher affinity for **Coconut Pineapple**.
            """)
        elif "Heavy Lifters" in selected_persona:
            st.markdown("""
            * **Training Habits:** Dedicated strength trainers. Frequently visit during weekends.
            * **Sauna Habits:** Highest facility usage (~53.7%) for post-workout recovery.
            * **Retail Flavor Match:** Driven by **Orange** and **Lemon**.
            """)
            
    with col2:
        st.markdown("### 📊 Key Performance Metrics for this Persona")
        # Example dynamic metric comparison chart
        fig_metrics = px.histogram(persona_df, x="visit_per_week", 
                                   title=f"Weekly Visit Frequency Distribution for {selected_persona}",
                                   color_discrete_sequence=['#4C6EF5'])
        st.plotly_chart(fig_metrics, use_container_width=True)

# ==========================================
# TAB 3: MARKETING ACTION TOOL
# ==========================================
with tab3:
    st.subheader("Generate Automated Marketing Campaigns")
    st.write("Target specific member sub-segments with promotions based on their behavioral needs.")
    
    campaign_target = st.selectbox("Select Target Cluster for Campaign:", options=list(cluster_names.values()))
    target_df = df[df['Cluster_Name'] == campaign_target]
    
    # Add a practical business use-case filter
    if "Floor Casuals" in campaign_target:
        st.info("💡 **Strategy Recommendation:** Send these members an email offer for a free group fitness class pass to help boost engagement and reduce churn.")
    elif "Heavy Lifters" in campaign_target:
        st.info("💡 **Strategy Recommendation:** Target these members with promotions for post-workout recovery packages, premium protein shakes, or weekend personal training sessions.")
        
    # Display the targeted audience
    st.dataframe(target_df[['gender', 'abonoment_type', 'visit_per_week', 'fav_drink']].head(10))
    
    # Convert data for download button
    csv_data = target_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Download Targeted Member List ({len(target_df)} rows)",
        data=csv_data,
        file_name=f"{campaign_target.lower().replace(' ', '_')}_target_list.csv",
        mime='text/csv'
    )

