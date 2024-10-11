import streamlit as st
import pandas as pd
import plotly.express as px

# Load the CSV file
file_id = '1-nKxWsR4Yc8cI7W3jeYwh0Ef1zq9tvIQ'
file_path = f'https://drive.google.com/uc?id={file_id}'
df_import_export = pd.read_csv(file_path)
df_import_export['Date'] = pd.to_datetime(df_import_export['Date'], dayfirst=True)
df_import_export['Year'] = df_import_export['Date'].dt.year
df_import_export['Month'] = df_import_export['Date'].dt.month
df_import_export['Day'] = df_import_export['Date'].dt.day

st.title("Import/Export Dashboard")

# Ports Comparison Section
st.header("Ports Comparison")
selected_country_chart = st.selectbox("Select a country for Ports Comparison", df_import_export['Country'].unique())
selected_ports_chart = st.multiselect("Select up to 2 ports for comparison", 
                                      df_import_export[df_import_export['Country'] == selected_country_chart]['Port'].unique())

if selected_ports_chart and len(selected_ports_chart) <= 2:
    filtered_df_chart = df_import_export[(df_import_export['Country'] == selected_country_chart) &
                                         (df_import_export['Port'].isin(selected_ports_chart))]
    
    # Bar chart for port comparison
    bar_chart = px.bar(
        filtered_df_chart,
        x='Port',
        y='Value',
        color='Import_Export',
        title='Import and Export Values by Port',
        barmode='group',
        color_discrete_sequence=['blue', 'green']
    )
    st.plotly_chart(bar_chart)

    # Pie chart for Shipping Methods
    shipping_pie = px.pie(
        filtered_df_chart,
        names='Shipping_Method',
        values='Value',
        title=f'Shipping Methods Distribution for {selected_ports_chart}',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(shipping_pie)

    # Pie chart for Payment Terms
    payment_pie = px.pie(
        filtered_df_chart,
        names='Payment_Terms',
        values='Value',
        title=f'Payment Terms Distribution for {selected_ports_chart}',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(payment_pie)

# Ports Table Section
st.header("Ports Table")
selected_country_table = st.selectbox("Select a country for Ports Table", df_import_export['Country'].unique(), key="table_country")
selected_import_export = st.selectbox("Select Import, Export, or Both", ['Import', 'Export', 'Both'], key="table_import_export")
selected_category = st.selectbox("Select Category", df_import_export['Category'].unique(), key="table_category")
selected_shipping_method = st.selectbox("Select Shipping Method", df_import_export['Shipping_Method'].unique(), key="table_shipping_method")
selected_payment_terms = st.selectbox("Select Payment Terms", df_import_export['Payment_Terms'].unique(), key="table_payment_terms")

# Filter the data based on the selected filters
filtered_df_table = df_import_export[df_import_export['Country'] == selected_country_table]
if selected_import_export != 'Both':
    filtered_df_table = filtered_df_table[filtered_df_table['Import_Export'] == selected_import_export]
if selected_category:
    filtered_df_table = filtered_df_table[filtered_df_table['Category'] == selected_category]
if selected_shipping_method:
    filtered_df_table = filtered_df_table[filtered_df_table['Shipping_Method'] == selected_shipping_method]
if selected_payment_terms:
    filtered_df_table = filtered_df_table[filtered_df_table['Payment_Terms'] == selected_payment_terms]

# Display the table with average quantity and value by port
if not filtered_df_table.empty:
    ports_table = filtered_df_table.groupby('Port').agg(
        Average_Quantity=('Quantity', 'mean'),
        Average_Value=('Value', 'mean')
    ).reset_index()
    st.write("Filtered Ports Table")
    st.dataframe(ports_table)
else:
    st.write("No data available for the selected filters.")
