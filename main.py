"""
Name: Samantha Plunkett
CS230: Section SN1
Data: Colleges and Universities Data Set
URL: Link to your web application online (see extra credit)

Description:

How I satisfied everyone of the features

This program ... (a few sentences about your program and the queries and charts)

"""
import csv
import numpy as np
import streamlit as st
import pydeck as pdk
import pandas as pd
import mapbox as mb
import matplotlib.pyplot as plt
import random as random


# datafile = "Postsecondary_School_Locations_-_Current (1).csv"

def read_file(datafile):
    df = pd.read_csv(datafile)
    df_new = df.rename(columns={"X": "lon", "Y": "lat"})
    return df_new


read_file("Postsecondary_School_Locations_-_Current (1).csv")


def bar_chart(states, count, title):
    plt.bar(states, count, color="plum", linewidth=4)
    plt.title(title)
    plt.xlabel("State")
    plt.ylabel("Count of Universities and Colleges")
    return plt


def pie_chart(dict, title):
    values = dict.values()
    values_list = list(values)

    EXPLODE_NUM = 0.05
    largest_value = max(values_list)
    largest = values_list.index(largest_value)
    explode = [0] * len(values_list)
    explode[largest] = EXPLODE_NUM

    plt.figure()
    plt.pie(dict.values(), labels=dict.keys(), explode=explode, autopct='%1.2f%%')
    plt.title(title)
    plt.legend(dict.keys())
    return plt


def bar_chart1(locales, count1, title):
    plt.figure()
    plt.bar(locales, count1, color="blue", linewidth=4)
    plt.title(title)
    plt.xlabel("Locale Code")
    plt.ylabel("Count of Universities and Colleges")
    return plt


def county_map(locations):
    map_df = pd.DataFrame(locations, columns=["school name", "X", "Y"])

    view_location = pdk.ViewState(
        latitude=map_df["Y"].mean(),
        longitude=map_df["X"].mean(),
        zoom=9,
        pitch=0)

    location_data = {"html": "University Name:<br/> <b>{school name}</br>",
                     "style": {"backgroundColor": "grey",
                               "color": "black"}
                     }

    layer_county_map = pdk.Layer('ScatterplotLayer',
                                 data=map_df,
                                 get_position='[X, Y]',
                                 get_radius=400,
                                 radius_scale=2,
                                 get_color=[51, 51, 255],
                                 pickable=True
                                 )

    county_map1 = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_location,
        layers=[layer_county_map],
        tooltip=location_data
    )
    st.pydeck_chart(county_map1)


def main():
    df_new = read_file("Postsecondary_School_Locations_-_Current (1).csv")

    st.sidebar.title("Universities and Colleges")
    st.sidebar.header("Map of Colleges and Universities in the United States")
    st.sidebar.subheader("County Map Selector")

    county = df_new['NMCNTY'].unique().tolist()
    countySelection = st.sidebar.selectbox("Select a county: ", county)

    st.write("You chose ", countySelection)

    locations = []
    for index, row in df_new.iterrows():
        if countySelection == row[11]:
            lon = row[0]
            lat = row[1]
            name = row[4]
            locations.append((name, lon, lat))

    county_map(locations)

    st.sidebar.subheader("College and University Count Bar Chart")

    states = df_new['STATE'].unique().tolist()
    stateSelection = st.sidebar.multiselect("Select states: ", states)

    state_dict = {}
    for state in stateSelection:
        count = 0
        for item in df_new["STATE"].iteritems():
            if item[1] == state:
                count += 1
        state_dict[state] = count
    # st.write(state_dict)
    dictionary = state_dict.keys()
    updated_dict = list(dictionary)
    new = ', '.join(updated_dict)

    st.write("You chose ", new)

    title = f'Count of Colleges and Universities in {new}'

    st.sidebar.subheader("Locale Code Selector")

    locales = df_new['LOCALE'].unique().tolist()
    localeSelection = st.sidebar.radio("Select a locale code: ", locales)

    locale_dict = {}
    for locale in locales:
        count1 = 0
        for item in df_new["LOCALE"].iteritems():
            if item[1] == locale:
                count1 += 1
        locale_dict[locale] = count1

    print(locale_dict)
    st.write(state_dict)
    dictionary1 = locale_dict.keys()
    updated_dict1 = list(dictionary1)

    st.write("You chose ", localeSelection)

    title1 = f'Count of Colleges and Universities by Locale Code'

    st.pyplot(bar_chart(state_dict.keys(), state_dict.values(), title))
    st.pyplot(pie_chart(state_dict, title))
    st.pyplot(bar_chart1(locale_dict.keys(), locale_dict.values(), title1))


main()
