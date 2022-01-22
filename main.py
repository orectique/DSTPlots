from numpy import arange
import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from math import ceil

st.set_page_config(
    page_title= 'Analysis of Dietary Data',
    page_icon = '📊'
)

st.title('Visualisation of Dietary Data')   
head = st.container()
c1 = st.container()
c2 = st.container()
c4 = st.container()
c5 = st.container()
c3 = st.container()


dietary = pd.read_csv('./Dietary.csv')
dietary['Date'] = pd.to_datetime(dietary['Date'], infer_datetime_format=True)
dietary['Day'] = dietary['Date'].dt.dayofweek


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
    dietary['Sum'] = dietary[['Grains', 'Pulses', 'Other Fruits', 'Leafy Vegetables',
       'Other Vegetables', 'Dairy', 'Meat, Poultry and Fish', 'Vitamin A Rich',
       'Nuts and Seeds', 'Eggs']].sum(axis =1)
    red1 = []
    red2 = []
    yellow = []
    green1 = []
    green2 = []

    for i in dietary['Aadhaar'].unique():
        temp = dietary[dietary['Aadhaar'] == i]

        k = ceil(temp['Sum'].mean())

        if k in range(1, 3):
            red1.append(i)
        elif k in range(3, 5):
            red2.append(i)
        elif k in range(5, 7):
            yellow.append(i)
        elif k in range(7, 10):
            green1.append(i)
        elif k in range(10, 11):
            green2.append(i)

    fig = go.Figure(data = [go.Bar(
        x = ['Dietary Diversity : 1-2', 'Dietary Diversity : 3-4', 'Dietary Diversity : 5-6', 'Dietary Diversity : 7-9', 'Dietary Diversity : 10-11'],
        y = [len(red1), len(red2), len(yellow), len(green1), len(green2)],
        marker_color = ['red', 'red', 'yellow', 'green', 'green']
    )])

    N = len(dietary['Aadhaar'].unique())

    fig.update_layout(title_text = f'Food Groups Consumed, Ceiling of Mean, N = {N}')

    return fig, red1, red2, yellow, green1, green2

def graph4():
    delta = pd.DataFrame(columns = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    for ftype in types:
        days = [i for i in range(7)]
        change = []
        for day in range(7):
            change.append(dietary[dietary['Day'] == day][ftype].sum())
        delta.loc[ftype] = change

    return px.line(delta.transpose(), title = 'Variation by Day of the Week', markers = True)

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

    with c4:
        st.header('Variation in Food Intake by Day of the Week')
        fig4 = graph4()
        st.write(fig4)

    with c3:
        fig3, red1, red2, yellow, green1, green2 = graph3()
        st.header('Exploration of Dietary Diversity')
        st.write('In this graphic, a color of red indicates that the average diversity of a person\'s diet is below 4 groups. A color of yellow indicates that the diet is restricted to 5 or 6 groups. A color of green indicates a diverse diet that includes more than 6 groups.')
        st.write(fig3)
        with st.expander('People in Red Zone - 1-2'):
            st.write(pd.Series(red1, index = arange(1, len(red1) + 1)), name = 'Aadhaar Numbers')
        with st.expander('People in Red Zone - 3-4'):
            st.write(pd.Series(red2, index = arange(1, len(red2) + 1)), name = 'Aadhaar Numbers')
        with st.expander('People in Yellow Zone - 5-6'):
            st.write(pd.Series(yellow, index = arange(1, len(yellow) + 1)), name = 'Aadhaar Numbers')
        with st.expander('People in Green Zone - 7-9'):
            st.write(pd.Series(green1, index = arange(1, len(green1) + 1)), name = 'Aadhaar Numbers')
        with st.expander('People in Green Zone - 10-11'):
            st.write(pd.Series(green2, index = arange(1, len(green2) + 1)), name = 'Aadhaar Numbers')
        

