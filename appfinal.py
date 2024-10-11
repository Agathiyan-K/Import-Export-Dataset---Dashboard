import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
file_id = '1-nKxWsR4Yc8cI7W3jeYwh0Ef1zq9tvIQ'
file_path = f'https://drive.google.com/uc?id={file_id}'
df_import_export = pd.read_csv(file_path)
df_import_export['Date'] = pd.to_datetime(df_import_export['Date'], dayfirst=True)
df_import_export['Year'] = df_import_export['Date'].dt.year
df_import_export['Month'] = df_import_export['Date'].dt.month
df_import_export['Day'] = df_import_export['Date'].dt.day

st.title("Import/Export Dataset Dashboard")

# Section 1: Time-based Import/Export Graph
st.header("Time-Based Import/Export Analysis")
import_export_selection = st.multiselect("Select Import or Export", options=['Import', 'Export'])
time_period = st.selectbox("Select Time Period", options=['Year', 'Month', 'Day'])
quantity_value = st.selectbox("Select Quantity or Value", options=['Quantity', 'Value'])

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
    st.plotly_chart(fig, use_container_width=True)

# Section 2: Country Comparison Charts
st.header("Country Comparison Analysis")
selected_countries = st.multiselect("Select up to 3 countries for comparison", options=df_import_export['Country'].unique(), max_selections=3)
selected_import_export = st.selectbox("Select Import, Export, or Both", options=['Import', 'Export', 'Both'])

if selected_countries and selected_import_export:
    if selected_import_export != 'Both':
        filtered_df = df_import_export[(df_import_export['Country'].isin(selected_countries)) & (df_import_export['Import_Export'] == selected_import_export)]
    else:
        filtered_df = df_import_export[df_import_export['Country'].isin(selected_countries)]

    import_export_fig = px.bar(
        filtered_df.groupby(['Country', 'Import_Export']).size().reset_index(name='Count'),
        x='Country', y='Count', color='Import_Export',
        title='Import/Export Count by Country',
        barmode='group',
        color_discrete_sequence=['blue', 'green']
    )
    st.plotly_chart(import_export_fig, use_container_width=True)

    category_fig = px.bar(
        filtered_df.groupby(['Country', 'Category']).size().reset_index(name='Count'),
        x='Country', y='Count', color='Category',
        title='Count of Categories by Country',
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(category_fig, use_container_width=True)

    shipping_method_fig = px.bar(
        filtered_df.groupby(['Country', 'Shipping_Method']).size().reset_index(name='Count'),
        x='Country', y='Count', color='Shipping_Method',
        title='Count of Shipping Methods by Country',
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(shipping_method_fig, use_container_width=True)

# Section 3: Ports Comparison
st.header("Ports Comparison")
country_selection_chart = st.selectbox("Select Country for Ports Comparison Chart", options=df_import_export['Country'].unique())
selected_ports = st.multiselect("Select up to 2 Ports", options=df_import_export[df_import_export['Country'] == country_selection_chart]['Port'].unique(), max_selections=2)

if country_selection_chart and selected_ports:
    filtered_df = df_import_export[(df_import_export['Country'] == country_selection_chart) & (df_import_export['Port'].isin(selected_ports))]

    port_chart = px.bar(
        filtered_df,
        x='Port',
        y='Value',
        color='Import_Export',
        title='Import and Export Values by Port',
        barmode='group',
        color_discrete_sequence=['blue', 'green']
    )
    st.plotly_chart(port_chart, use_container_width=True)

    shipping_pie_chart = px.pie(
        filtered_df,
        names='Shipping_Method',
        values='Value',
        title=f'Shipping Methods Distribution for Ports: {", ".join(selected_ports)}',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(shipping_pie_chart, use_container_width=True)

    payment_terms_pie_chart = px.pie(
        filtered_df,
        names='Payment_Terms',
        values='Value',
        title=f'Payment Terms Distribution for Ports: {", ".join(selected_ports)}',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(payment_terms_pie_chart, use_container_width=True)

# Section 4: Ports Table
st.header("Ports Table")
country_selection_table = st.selectbox("Select Country for Ports Table", options=df_import_export['Country'].unique())
import_export_filter = st.selectbox("Select Import, Export, or Both", options=['Import', 'Export', 'Both'])
category_filter = st.selectbox("Select Category", options=['All'] + list(df_import_export['Category'].unique()))
shipping_method_filter = st.selectbox("Select Shipping Method", options=['All'] + list(df_import_export['Shipping_Method'].unique()))
payment_terms_filter = st.selectbox("Select Payment Terms", options=['All'] + list(df_import_export['Payment_Terms'].unique()))

filtered_table_df = df_import_export[df_import_export['Country'] == country_selection_table]

if import_export_filter != 'Both':
    filtered_table_df = filtered_table_df[filtered_table_df['Import_Export'] == import_export_filter]
if category_filter != 'All':
    filtered_table_df = filtered_table_df[filtered_table_df['Category'] == category_filter]
if shipping_method_filter != 'All':
    filtered_table_df = filtered_table_df[filtered_table_df['Shipping_Method'] == shipping_method_filter]
if payment_terms_filter != 'All':
    filtered_table_df = filtered_table_df[filtered_table_df['Payment_Terms'] == payment_terms_filter]

if not filtered_table_df.empty:
    ports_table = filtered_table_df.groupby('Port').agg(
        Average_Quantity=('Quantity', 'mean'),
        Average_Value=('Value', 'mean')
    ).reset_index()
    st.write(ports_table)
else:
    st.write("No data available for the selected filters.")
