from numpy import arange
import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title= 'Analysis of Dietary Data',
    page_icon='🍴'
)

st.title('Visualisation of Dietary Data')   
head = st.container()
c1 = st.container()
c2 = st.container()
c3 = st.container()

dietary = pd.read_csv('./Dietary.csv')

types = ['Grains', 'Pulses', 'Other Fruits',
        'Leafy Vegetables', 'Other Vegetables', 'Dairy',
        'Meat, Poultry and Fish', 'Vitamin A Rich', 'Nuts and Seeds', 'Eggs',
        'Junk Foods']

def graph1():

    ds1 = pd.DataFrame(columns=['Aadhaar', 'Grains', 'Pulses', 'Other Fruits',
        'Leafy Vegetables', 'Other Vegetables', 'Dairy',
        'Meat, Poultry and Fish', 'Vitamin A Rich', 'Nuts and Seeds', 'Eggs',
        'Junk Foods'])

    for i in dietary['Aadhaar'].unique():
        temp = dietary[dietary['Aadhaar'] == i]

        k = [i]

        for ftype in types:
            k = k + [1 if 1 in list(temp[ftype]) else 0]
            

        ds1.loc[len(ds1.index)] = k  

    out = pd.DataFrame(columns=['Food Type', 'Count'])

    for ftype in types:
        out.loc[len(out)] = [ftype, ds1[ftype].sum()]

    return px.bar(out, x = 'Food Type', y = 'Count', title='Consumption Tally')

def graph2(num):
    ds2 = pd.DataFrame(columns=['Aadhaar', 'Grains', 'Pulses', 'Other Fruits',
       'Leafy Vegetables', 'Other Vegetables', 'Dairy',
       'Meat, Poultry and Fish', 'Vitamin A Rich', 'Nuts and Seeds', 'Eggs',
       'Junk Foods'])

    for i in dietary['Aadhaar'].unique():
       temp = dietary[dietary['Aadhaar'] == i]

       k = [i]

       for ftype in types:
            k = k + [temp[ftype].sum()]
              

       ds2.loc[len(ds2.index)] = k  
    
    out = pd.DataFrame(columns=['Food Type', 'Count'])

    for ftype in types:
        out.loc[len(out)] = [ftype, len([i for i in ds2[ftype] if i >= num])]

    return px.bar(out, x = 'Food Type', y = 'Count', title= 'Frequency of Consumption')


def graph3():
    red = []
    yellow = []
    green = []

    for i in dietary['Aadhaar'].unique():
        temp = dietary[dietary['Aadhaar'] == i]

        k = 0

        for ftype in types:
            if 1 in list(temp[ftype]):
                k += 1
            else:
                k += 0

        if k in range(1, 5):
            red.append(i)
        elif k in range(5, 7):
            yellow.append(i)
        elif k in range(7, 12):
            green.append(i)

    fig = go.Figure(data = [go.Bar(
        x = ['Dietary Diversity : 1-4', 'Dietary Diversity : 5-6', 'Dietary Diversity : 7-11'],
        y = [len(red), len(yellow), len(green)],
        marker_color = ['red', 'yellow', 'green']
    )])

    fig.update_layout(title_text = 'Dietary Diversity')

    return fig, red, yellow

with head:
    with c1:        
        st.header('Consumption Tally of Food Groups')
        fig1 = graph1()
        st.write(fig1)

    with c2:
        st.header('Frequency of Consumption of Food Groups')
        num = st.selectbox('Number of Days', (arange(1, 29)))
        fig2 = graph2(num)
        st.write(fig2)

    with c3:
        fig3, red, yellow = graph3()
        st.header('Exploration of Dietary Diversity')
        st.write('In this graphic, a color of red indicates that the diversity of a person\'s diet is below 4 groups. A color of yellow indicates that the diet is restricted to 5 or 6 groups. A color of green indicates a diverse diet that includes more than 6 groups.')
        st.write(fig3)
        with st.expander('People in Red Zone'):
            st.write(pd.Series(red, index = arange(1, len(red) + 1)), name = 'Aadhaar Numbers')
        with st.expander('People in Yellow Zone'):
            st.write(pd.Series(yellow, index = arange(1, len(yellow) + 1)), name = 'Aadhaar Numbers')

