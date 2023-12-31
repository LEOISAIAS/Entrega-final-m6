# -*- coding: utf-8 -*-
"""ActiIntegradoraA01275327BIEN

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j9o4KG4moDyGtwpKKpbCoQTs3hIBFeUf
"""

from pandas._libs.tslibs import Resolution
import streamlit as st
import pandas as pd
import numpy as np
import plotly as px
import plotly.figure_factory as ff
from bokeh.plotting import figure
import matplotlib.pyplot as plt

st.title('Creative Police Incident Reports')
st.markdown(
    """
    <style>
    .big-font {
        font-size: 24px !important;
    }
    .colorful-text {
        color: #FF5733 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    '<p class="big-font colorful-text">Police Incident Reports from 2018 to 2020 in San Francisco</p>',
    unsafe_allow_html=True
)

df = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")

st.markdown(
    """
    The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location, and resolution.
    """
)

mapa = pd.DataFrame()
mapa['Date'] = df['Incident Date']
mapa['Day'] = df['Incident Day of Week']
mapa['Police District'] = df['Police District']
mapa['Neighborhood'] = df['Analysis Neighborhood']
mapa['Incident Category'] = df['Incident Category']
mapa['Incident Subcategory'] = df['Incident Subcategory']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']
mapa = mapa.dropna()

subset_data2 = mapa
police_district_input = st.sidebar.multiselect(
    'Police District',
    mapa.groupby('Police District').count().reset_index()['Police District'].tolist()
)
if len(police_district_input) > 0:
    subset_data2 = mapa[mapa['Police District'].isin(police_district_input)]

subset_data1 = subset_data2
neighborhood_input = st.sidebar.multiselect(
    'Neighborhood',
    subset_data2.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist()
)
if len(neighborhood_input) > 0:
    subset_data1 = subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]

subset_data = subset_data1
incident_input = st.sidebar.multiselect(
    'Incident Category',
    subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist()
)
if len(incident_input) > 0:
    subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]

subset_data

st.markdown('It is important to mention that any police district can answer to any incident, the neighborhood in which it happened is not related to the police district.')

# Mapa de ubicación de los crímenes
st.markdown('<p class="big-font colorful-text">Crime locations in San Francisco</p>', unsafe_allow_html=True)
st.map(subset_data)

# Gráfico de barras de crímenes por día de la semana
st.markdown('<p class="big-font colorful-text">Crimes occurred per day of the week</p>', unsafe_allow_html=True)
st.bar_chart(subset_data['Day'].value_counts())

# Gráfico de líneas de crímenes por fecha
st.markdown('<p class="big-font colorful-text">Crimes occurred per date</p>', unsafe_allow_html=True)
st.line_chart(subset_data['Date'].value_counts())
st.markdown('Type of crimes committed')
st.bar_chart(subset_data['Incident Category'].value_counts())

agree = st.button('Click to see Incident Subcategories')
if agree:
    st.markdown('Subtype of crimes committed')
    st.bar_chart(subset_data['Incident Subcategory'].value_counts())

# Gráfico de pastel del estado de resolución
st.markdown('<p class="big-font colorful-text">Resolution status</p>', unsafe_allow_html=True)
fig1, ax1 = plt.subplots()
labels = subset_data['Resolution'].unique()
ax1.pie(subset_data['Resolution'].value_counts(), labels=labels, autopct='%1.1f%%', startangle=20)
st.pyplot(fig1)

# Gráfico de barras de cantidad de incidentes por categoría
st.markdown('<p class="big-font colorful-text">Cantidad de Incidentes por Categoría</p>', unsafe_allow_html=True)
incident_counts = df['Incident Category'].value_counts()
plt.barh(incident_counts.index, incident_counts.values, color='#FF5733')
plt.title('Cantidad de Incidentes por Categoría')
plt.xlabel('Cantidad de Incidentes')
plt.ylabel('Categoría')
st.pyplot(plt)

# Gráfico de pastel de porcentaje de incidentes por categoría
st.markdown('<p class="big-font colorful-text">% de Incidentes por Categoría</p>', unsafe_allow_html=True)
incident_counts = df['Incident Category'].value_counts()
plt.pie(incident_counts.values, labels=incident_counts.index, autopct='%1.1f%%', colors=['#FF5733', '#FFC300', '#C70039'])
plt.title('Porcentaje de Incidentes por Categoría')
st.pyplot(plt)