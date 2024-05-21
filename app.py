import pandas as pd
import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components

# Load the data from the CSV file
df = pd.read_csv('employees.csv')

# Convert staff numbers to strings to avoid type issues
df['employee_staff_number'] = df['employee_staff_number'].astype(str)
df['manager_staff_number'] = df['manager_staff_number'].astype(str)

# List of professions in the dataset
professions = df['profession'].unique()

# Streamlit sidebar for selecting professions
st.sidebar.title("Select Professions to Display")
selected_professions = st.sidebar.multiselect("Professions", professions, default=professions)

# Filter the DataFrame based on selected professions
filtered_df = df[df['profession'].isin(selected_professions)]

# Initialize a Pyvis network
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

# Add nodes and edges to the network
# Specify edge colour so it can be seen on black background
for idx, row in filtered_df.iterrows():
    label = f"{row['employee_name']}\n{row['job_title']}\n{row['profession']}"
    net.add_node(row['employee_staff_number'], label=label, title=label, color='lightblue')
    if pd.notna(row['manager_staff_number']) and row['manager_staff_number'] in filtered_df['employee_staff_number'].values:
        net.add_edge(row['manager_staff_number'], row['employee_staff_number'], color='white')

# Enable physics for a force-directed layout
net.force_atlas_2based()

# Generate network visualization HTML
html_content = net.generate_html()

# Display the interactive network graph in the Streamlit app
components.html(html_content, height=800)
