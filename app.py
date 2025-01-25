import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Infrastructure Projects Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the data
@st.cache_data
def load_data():
   
    columns = [
        'S.No.',
        'Project Name',
        'Total Project Cost (In Rs.Crore)',
        'Sector',
        'Sub-Sector',
        'Project Authority',
        'Year',
        'Location',
        'Status',
        'Resource Management',
        'Logistics',
        'Machinery Mobilization',
        'Work Force'
    ]
    
    # Read Excel file with proper column names
    df = pd.read_excel(
        "All Infrastructure Projects.xlsx",
        skiprows=1,  # Skip the header row
        names=columns
    )
    
    return df

# Main function
def main():
    st.title("Infrastructure Projects Analysis Dashboard")
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Add "All" option to each filter
    def get_filter_options(column):
        options = ['All'] + sorted(df[column].unique().tolist())
        return options
    
    # Location filter
    selected_location = st.sidebar.selectbox(
        "Select Location",
        options=get_filter_options('Location'),
        index=0  # Default to "All"
    )
    
    # Status filter
    selected_status = st.sidebar.selectbox(
        "Select Status",
        options=get_filter_options('Status'),
        index=0
    )
    
    # Sector filter
    selected_sector = st.sidebar.selectbox(
        "Select Sector",
        options=get_filter_options('Sector'),
        index=0
    )
    
    # Year filter
    selected_year = st.sidebar.selectbox(
        "Select Year",
        options=get_filter_options('Year'),
        index=0
    )
    
    # Filter the dataframe based on selections
    filtered_df = df.copy()
    
    if selected_location != 'All':
        filtered_df = filtered_df[filtered_df['Location'] == selected_location]
    if selected_status != 'All':
        filtered_df = filtered_df[filtered_df['Status'] == selected_status]
    if selected_sector != 'All':
        filtered_df = filtered_df[filtered_df['Sector'] == selected_sector]
    if selected_year != 'All':
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    
    # Create three columns for key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Projects", len(filtered_df))
    with col2:
        total_cost = filtered_df['Total Project Cost (In Rs.Crore)'].sum()
        st.metric("Total Cost (Rs. Crore)", f"₹{total_cost:,.2f}")
    with col3:
        st.metric("Number of Sectors", len(filtered_df['Sector'].unique()))
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Projects by Sector
        st.subheader("Projects by Sector")
        sector_fig = px.pie(
            filtered_df,
            names='Sector',
            values='Total Project Cost (In Rs.Crore)',
            title='Project Cost Distribution by Sector'
        )
        st.plotly_chart(sector_fig, use_container_width=True)
    
    with col2:
        # Projects by Location
        st.subheader("Projects by Location")
        # Count projects by location
        location_data = (
            filtered_df.groupby('Location').size()  # Count projects
            .sort_values(ascending=False)  # Sort by count
            .reset_index(name='Number of Projects')  # Rename count column
        )
        location_fig = px.bar(
            location_data,
            x='Location',
            y='Number of Projects',
            title='Number of Projects by Location'
        )
        
        # Update layout with better x-axis formatting
        location_fig.update_layout(
            xaxis_tickangle=-45,  # Rotate labels for better readability
            height=400,
            margin=dict(t=30, b=80, l=0, r=0),  # Increased bottom margin for labels
            xaxis=dict(
                tickmode='array',
                ticktext=location_data['Location'],
                tickvals=list(range(len(location_data))),
                tickfont=dict(size=10)
            )
        )
        
        st.plotly_chart(location_fig, use_container_width=True)
    
    # Project Status Analysis
    st.subheader("Project Status Analysis")
    status_fig = px.pie(
        filtered_df.groupby('Status')['Total Project Cost (In Rs.Crore)'].sum().reset_index(),
        names='Status',
        values='Total Project Cost (In Rs.Crore)',
        title='Project Cost Distribution by Status'
    )
    st.plotly_chart(status_fig, use_container_width=True)
    
    # Additional Analysis Section
    st.header("Detailed Resource Analysis")
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["Resource Management", "Logistics", "Machinery", "Workforce"])
    
    with tab1:
        st.subheader("Resource Management Analysis")
        resource_counts = filtered_df['Resource Management'].value_counts()
        resource_fig = px.pie(
            values=resource_counts.values,
            names=resource_counts.index,
            title='Distribution of Resource Management Types'
        )
        st.plotly_chart(resource_fig, use_container_width=True)
        
        # Full width for table
        st.subheader("Resource Requirements by Location")
        resource_location = pd.crosstab(filtered_df['Location'], filtered_df['Resource Management'])
        resource_location['Total Projects'] = resource_location.sum(axis=1)
        resource_location = resource_location.sort_values('Total Projects', ascending=False)
        
        styled_resource = resource_location.style.background_gradient(cmap='Blues', subset=['Total Projects'])
        st.dataframe(styled_resource, use_container_width=True)

    with tab2:
        st.subheader("Logistics Analysis")
        logistics_counts = filtered_df['Logistics'].value_counts()
        logistics_fig = px.pie(
            values=logistics_counts.values,
            names=logistics_counts.index,
            title='Distribution of Logistics Requirements'
        )
        st.plotly_chart(logistics_fig, use_container_width=True)
        
        # Full width for table
        st.subheader("Logistics Requirements by Location")
        logistics_location = pd.crosstab(filtered_df['Location'], filtered_df['Logistics'])
        logistics_location['Total Projects'] = logistics_location.sum(axis=1)
        logistics_location = logistics_location.sort_values('Total Projects', ascending=False)
        
        styled_logistics = logistics_location.style.background_gradient(cmap='Blues', subset=['Total Projects'])
        st.dataframe(styled_logistics, use_container_width=True)

    with tab3:
        st.subheader("Machinery Mobilization Analysis")
        machinery_counts = filtered_df['Machinery Mobilization'].value_counts()
        machinery_fig = px.pie(
            values=machinery_counts.values,
            names=machinery_counts.index,
            title='Distribution of Machinery Requirements'
        )
        st.plotly_chart(machinery_fig, use_container_width=True)
        
        # Full width for table
        st.subheader("Machinery Requirements by Location")
        machinery_location = pd.crosstab(filtered_df['Location'], filtered_df['Machinery Mobilization'])
        machinery_location['Total Projects'] = machinery_location.sum(axis=1)
        machinery_location = machinery_location.sort_values('Total Projects', ascending=False)
        
        styled_machinery = machinery_location.style.background_gradient(cmap='Blues', subset=['Total Projects'])
        st.dataframe(styled_machinery, use_container_width=True)

    with tab4:
        st.subheader("Workforce Analysis")
        workforce_counts = filtered_df['Work Force'].value_counts()
        workforce_fig = px.pie(
            values=workforce_counts.values,
            names=workforce_counts.index,
            title='Distribution of Workforce Requirements'
        )
        st.plotly_chart(workforce_fig, use_container_width=True)
        
        # Full width for table
        st.subheader("Workforce Requirements by Location")
        workforce_location = pd.crosstab(filtered_df['Location'], filtered_df['Work Force'])
        workforce_location['Total Projects'] = workforce_location.sum(axis=1)
        workforce_location = workforce_location.sort_values('Total Projects', ascending=False)
        
        styled_wf = workforce_location.style.background_gradient(cmap='Blues', subset=['Total Projects'])
        st.dataframe(styled_wf, use_container_width=True)

    # Show detailed data table
    st.header("Detailed Project Data")
    st.dataframe(
        filtered_df.style.format({
            'Total Project Cost (In Rs.Crore)': '{:,.2f}'
        }),
        use_container_width=True
    )

if __name__ == "__main__":
    main() 