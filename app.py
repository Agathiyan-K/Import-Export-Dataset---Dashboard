import pandas as pd
import plotly.express as px
import streamlit as st

# Load the CSV file from Google Drive
file_id = '1-nKxWsR4Yc8cI7W3jeYwh0Ef1zq9tvIQ'
file_path = f'https://drive.google.com/uc?id={file_id}'
df_import_export = pd.read_csv(file_path)
df_import_export['Date'] = pd.to_datetime(df_import_export['Date'], dayfirst=True)
df_import_export['Year'] = df_import_export['Date'].dt.year
df_import_export['Month'] = df_import_export['Date'].dt.month
df_import_export['Day'] = df_import_export['Date'].dt.day

st.title("Import/Export Dashboard")

# 1. Time Period & Country Comparison
st.header("Time Period & Country Comparison")

# Dropdown for selecting Import or Export
import_export_selection = st.multiselect("Select Import or Export", ['Import', 'Export'])

# Dropdown for selecting Year, Month, or Day
time_period = st.selectbox("Select Time Period", ['Year', 'Month', 'Day'])

# Dropdown for selecting Quantity or Value
quantity_value = st.selectbox("Select Quantity or Value", ['Quantity', 'Value'])

if import_export_selection and time_period and quantity_value:
    x_axis = time_period
    filtered_df = df_import_export[df_import_export['Import_Export'].isin(import_export_selection)]
    grouped_df = filtered_df.groupby([x_axis, 'Import_Export'], as_index=False).agg({quantity_value: 'sum'})

    fig = px.bar(
        grouped_df,
        x=x_axis,
        y=quantity_value,
        color='Import_Export',
        title=f"{quantity_value} by {time_period}",
        labels={quantity_value: quantity_value, x_axis: time_period},
        color_discrete_map={'Import': 'blue', 'Export': 'orange'}
    )
    st.plotly_chart(fig)

st.write("---")

# 2. Country Comparison for Import/Export and Categories
st.header("Country Comparison Dashboard")

# Country selection for comparison
selected_countries = st.multiselect("Select up to 3 countries for comparison", df_import_export['Country'].unique())

# Import/Export selection for comparison
selected_import_export = st.selectbox("Select Import, Export, or Both", ['Import', 'Export', 'Both'])

if selected_countries and selected_import_export:
    if len(selected_countries) > 3:
        selected_countries = selected_countries[:3]

    filtered_df = df_import_export[
        (df_import_export['Country'].isin(selected_countries)) & 
        ((df_import_export['Import_Export'] == selected_import_export) if selected_import_export != 'Both' else True)
    ]

    # Import/Export Count by Country
    import_export_fig = px.bar(
        filtered_df.groupby(['Country', 'Import_Export']).size().reset_index(name='Count'),
        x='Country', y='Count', color='Import_Export',
        title='Import/Export Count by Country',
        barmode='group',
        color_discrete_sequence=['blue', 'green']
    )
    st.plotly_chart(import_export_fig)

    # Category Count by Country
    category_fig = px.bar(
        filtered_df.groupby(['Country', 'Category']).size().reset_index(name='Count'),
        x='Country', y='Count', color='Category',
        title='Count of Categories by Country',
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(category_fig)

    # Shipping Method Count by Country
    shipping_method_fig = px.bar(
        filtered_df.groupby(['Country', 'Shipping_Method']).size().reset_index(name='Count'),
        x='Country', y='Count', color='Shipping_Method',
        title='Count of Shipping Methods by Country',
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(shipping_method_fig)

st.write("---")

# 3. Ports Comparison and Ports Table
st.header("Ports Comparison & Ports Table")

# Country selection for Ports Comparison
country_for_chart = st.selectbox("Select a country for ports comparison chart", df_import_export['Country'].unique())
selected_ports = st.multiselect("Select up to 2 ports for comparison", df_import_export[df_import_export['Country'] == country_for_chart]['Port'].unique())

if country_for_chart and selected_ports and len(selected_ports) <= 2:
    filtered_df = df_import_export[(df_import_export['Country'] == country_for_chart) & (df_import_export['Port'].isin(selected_ports))]

    # Ports Comparison Chart
    port_chart = px.bar(
        filtered_df,
        x='Port',
        y='Value',
        color='Import_Export',
        title='Import and Export Values by Port',
        barmode='group',
        color_discrete_sequence=['blue', 'green']
    )
    st.plotly_chart(port_chart)

    # Shipping Methods Pie Chart
    shipping_pie = px.pie(
        filtered_df,
        names='Shipping_Method',
        values='Value',
        title=f'Shipping Methods for Ports: {", ".join(selected_ports)}',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(shipping_pie)

    # Payment Terms Pie Chart
    payment_pie = px.pie(
        filtered_df,
        names='Payment_Terms',
        values='Value',
        title=f'Payment Terms for Ports: {", ".join(selected_ports)}',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(payment_pie)

# Country selection for Ports Table
country_for_table = st.selectbox("Select a country for ports table", df_import_export['Country'].unique(), key='country_for_table')

# Additional Filters for Ports Table
import_export_table = st.selectbox("Import, Export, or Both", ['Import', 'Export', 'Both'])
category_table = st.selectbox("Select Category", df_import_export['Category'].unique())
shipping_method_table = st.selectbox("Select Shipping Method", df_import_export['Shipping_Method'].unique())
payment_terms_table = st.selectbox("Select Payment Terms", df_import_export['Payment_Terms'].unique())

# Filter data based on table selections
filtered_table_df = df_import_export[
    (df_import_export['Country'] == country_for_table) &
    ((df_import_export['Import_Export'] == import_export_table) if import_export_table != 'Both' else True) &
    (df_import_export['Category'] == category_table) &
    (df_import_export['Shipping_Method'] == shipping_method_table) &
    (df_import_export['Payment_Terms'] == payment_terms_table)
]

# Calculate average quantity and value by Port
table_data = filtered_table_df.groupby('Port').agg(
    Average_Quantity=('Quantity', 'mean'),
    Average_Value=('Value', 'mean')
).reset_index()

st.dataframe(table_data)
