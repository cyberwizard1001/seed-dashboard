import json
import time
import base64
import requests
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.set_option('deprecation.showPyplotGlobalUse', False)

def fetch_FoodGroups():
    url = 'http://115.243.144.151/seed/fetchAllFood.php'
    data_fetched = json.loads(requests.post(url).text)
    data_dict = data_fetched['datalist']
    food_df = pd.DataFrame.from_dict(data_dict)
    food_df.to_csv('data/FoodGroups.csv', index=False,
                   header=['Aadhaar', 'Date', 'Grains', 'Pulses', 'otherFruits', 'leafy_Vegetables','other_veg', 'Milk', 'Animal', 'Vitamin_A','Nuts', 'Eggs', 'junk'])

def fetch_Anthropometric():
    url = 'http://115.243.144.151/seed/fetchAllAnthropometric.php'
    data_fetched = json.loads(requests.post(url).text)
    data_dict = data_fetched['datalist']
    food_df = pd.DataFrame.from_dict(data_dict)
    food_df.to_csv('data/AnthropometricParameters.csv', index=False,
                   header=['Aadhaar', 'Month', 'Gender', 'Age', 'Height', 'Weight', 'BodyFat', 'MidArm', 'BMI', 'BMR'])


def fetch_Biochemical():
    url = 'http://115.243.144.151/seed/fetchAllBiochemical.php'
    data_fetched = json.loads(requests.post(url).text)
    data_dict = data_fetched['datalist']
    food_df = pd.DataFrame.from_dict(data_dict)
    food_df.to_csv('data/BiochemicalParameters.csv', index=False,
                   header=['Aadhaar', 'Month', 'Haemoglobin'])


def fetch_Clinical():
    url = 'http://115.243.144.151/seed/fetchAllClinical.php'
    data_fetched = json.loads(requests.post(url).text)
    data_dict = data_fetched['datalist']
    food_df = pd.DataFrame.from_dict(data_dict)
    food_df.to_csv('data/ClinicalParameters.csv', index=False,
                   header=['Aadhaar', 'Month', 'NeckPatches', 'PaleSkin', 'Pellagra', 'WrinkledSkin',
                           'TeethDiscolouration', 'BleedingGums', 'Cavity', 'WeakGums', 'AngularCuts',
                           'InflammedTongue', 'LipCuts', 'MouthUlcer',
                           'BitotSpot', 'Xeropthalmia', 'RedEyes', 'Catract',
                           'HairFall', 'DamagedHair', 'SplitEnds', 'Discolouration',
                           'DarkLines', 'SpoonShapedNails', 'BrokenNails', 'PaleNails','lean','bony','goitre','obesity'])



fetch_FoodGroups()
fetch_Anthropometric()
fetch_Biochemical()
fetch_Clinical()

ANTHRO_URL = (
    "data/AnthropometricParameters.csv"
)
BIO_URL = (
    "data/BiochemicalParameters.csv"
)
CLINIC_URL = (
    "data/ClinicalParameters.csv"
)
DIET_URL = (
    "data/FoodGroups.csv"
)

st.markdown("<h1 style='text-align: center; color: red;'>SEED Project - Admin Dashboard</h1>", unsafe_allow_html=True)
st.sidebar.title("Admin Dashboard")
st.markdown("<div align='center'>Dashboard to gain insights from the user data</div>", unsafe_allow_html=True)


def loadAnthro():
    data = pd.read_csv(ANTHRO_URL, header=0)
    return data


def loadBio():
    data = pd.read_csv(BIO_URL, header=0)
    return data


def loadClinic():
    data = pd.read_csv(CLINIC_URL, header=0)
    return data


def loadDiet():
    data = pd.read_csv(DIET_URL, header=0)
    data['Date'] = pd.to_datetime(data['Date'])
    return data

def get_table_download_link(df, name):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() 
    href = f'<a href="data:file/csv;base64,{b64}" download="{name}.csv">Download {name} data</a>'
    return href


anthro = loadAnthro()
bio = loadBio()
clinic = loadClinic()
diet = loadDiet()

dropdown = ['Select one', 'Show data', 'Anthropometric Analysis', 'Biochemical Analysis', 'Clinical Analysis']
option = st.sidebar.selectbox(
    'Choose an option',
    dropdown)

if option == 'Show data':
    dropdown.remove('Select one')
    # if st.sidebar.checkbox("Show Anthropometric Details", False, key=1):
    st.markdown("### Anthropometric Table")
    st.markdown("The following table gives you a real-time feed of the AnthropometricParameters table")
    st.dataframe(anthro)
    st.markdown(get_table_download_link(df=anthro, name='Anthropometric'), unsafe_allow_html=True)

    # if st.sidebar.checkbox("Show Biochemical Details", False, key=1):
    st.markdown("### Biochemical Table")
    st.markdown("The following table gives you a real-time feed of the BiochemicalParameters table")
    st.dataframe(bio)
    st.markdown(get_table_download_link(df=bio, name='Biochemical'), unsafe_allow_html=True)

    # if st.sidebar.checkbox("Show Clinical Details", False, key=1):
    st.markdown("### Clinical Table")
    st.markdown("The following table gives you a real-time feed of the ClinicalParameters table")
    st.dataframe(clinic)
    st.markdown(get_table_download_link(df=clinic, name='Clinical'), unsafe_allow_html=True)

    # if st.sidebar.checkbox("Show Dietary Details", False, key=1):
    st.markdown("### Food Groups Table")
    st.markdown("The following table gives you a real-time feed of the FoodGroups table")
    st.dataframe(diet)
    st.markdown(get_table_download_link(df=diet, name='Dietary'), unsafe_allow_html=True)

elif option == 'Anthropometric Analysis':
    dropdown.remove('Select one')
    st.markdown("## Anthropometric Analysis")
    
    # if st.sidebar.checkbox('Gender wise distribution', False, key=1):
    st.markdown('### Gender wise distribution')
    fig = px.pie(values=anthro['Gender'].value_counts().values, names=anthro['Gender'].value_counts().index)
    st.plotly_chart(fig)

    # if st.sidebar.checkbox('Age', False, key=1):
    st.markdown('### Age wise distribution')
    ages = anthro['Age'].values
    count1 = count2 = count3 = 0
    for age in ages:
        if age < 20:
            count1+=1
        elif age < 60:
            count2+=1
        else:
            count3+=1
    fig = px.bar(x=['Less than 20', 'Between 20 and 60', 'Over 60'], y =[count1, count2, count3])
    st.plotly_chart(fig)

    # if st.sidebar.checkbox('BMI'):
    bmi = anthro['BMI'].values
    count1 = count2 = count3 = 0
    for i in bmi:
        if i < 18:
            count1+=1
        elif i < 29:
            count2+=1
        else:
            count3+=1
    fig = px.bar(x=['Less than 18', 'Between 19 and 29', 'Over 30'], y =[count1, count2, count3])
    st.plotly_chart(fig)

elif option == 'Biochemical Analysis':
    dropdown.remove('Select one')
    print(dropdown)
    st.markdown("## Biochemical Analysis")
    bmi = bio['Haemoglobin'].values
    count1 = count2 = 0
    for i in bmi:
        if i < 13:
            count1+=1
        else:
            count2+=1
    fig = px.bar(x=['Less than 13', 'Over 13'], y =[count1, count2])
    st.plotly_chart(fig)

elif option == 'Clinical Analysis':
    dropdown.remove('Select one')
    st.markdown("## Clinical Analysis")
