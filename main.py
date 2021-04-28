"""
Name: Samantha Plunkett
CS230: Section SN1
Data: Colleges and Universities Data Set
URL: https://share.streamlit.io/samantha-plunkett/colleges-and-universities/main/main.py

For colors I used: https://matplotlib.org/stable/gallery/color/named_colors.html
Learning about iterrows: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iterrows.html
Learning about iteritems: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iteritems.html

Description:

This program uses Streamlit UI controls (selectbox, multiselect, radio) to create an interface with 1 map and 4 charts
The default parameter is read_file
Map: A map using custom values by developing data regarding counties
    in a data frame that was then put on the map
Chart 1: A bar chart using custom chart features by creating a dictionary and
        iterating through a column in a data frame to count state occurrences
Chart 2: A pie chart using custom chart features by creating a dictionary and
        iterating through a column in a data frame to count county occurrences
        and compare percentages of state counts for all states selected
Chart 3: A bar chart using custom chart features by creating a dictionary and
        iterating through a column in a data frame to count locale code occurrences
Chart 4: A pie chart using custom chart features by creating a dictionary and
        exploding values based on the radio button selection

"""
import csv
import numpy as np
import streamlit as st
import pydeck as pdk
import pandas as pd
import mapbox as mb
import matplotlib.pyplot as plt


# default parameter

def read_file(file):
    df = pd.read_csv(file)
    df_new = df.rename(columns={"X": "lon", "Y": "lat"})
    return df_new


# use of default parameter with default value

datafile = "Postsecondary_School_Locations_-_Current (1).csv"
read_file(datafile)


# bar chart counting the number of colleges and universities in selected states

def bar_chart(states, count, title):
    colors = ["thistle", "lightsteelblue", "mediumorchid", "powderblue", "slategrey", "lightskyblue"]
    plt.bar(states, count, color=colors, linewidth=4)
    plt.title(title)
    plt.xlabel("State")
    plt.ylabel("Count of Universities and Colleges")
    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    return plt


# pie chart showing the percentages of the number of colleges and universities in selected states

def pie_chart(dict, title):
    colors = ["thistle", "lightsteelblue", "mediumorchid", "powderblue", "slategrey", "lightskyblue"]
    values = dict.values()
    values_list = list(values)

    EXPLODE = 0.05
    largest_value = max(values_list)
    largest = values_list.index(largest_value)
    explode = [0] * len(values_list)
    explode[largest] = EXPLODE

    plt.figure()
    plt.pie(dict.values(), labels=dict.keys(), colors=colors, explode=explode, autopct='%1.2f%%')
    plt.title(title)
    plt.legend(dict.keys())
    return plt


# pie chart showing the percentages of the number of colleges and universities in all locale codes

def pie_chart2(dict, index):
    EXPLODE = 0.1
    explode = [0] * len(dict.values())
    explode[index] = EXPLODE

    colors = ["thistle", "lightsteelblue", "mediumorchid", "powderblue", "slategrey",
              "lightskyblue", "plum", "gainsboro", "mediumslateblue",
              "hotpink", "lightgreen", "dodgerblue"]

    plt.figure()
    plt.pie(dict.values(), labels=dict.keys(), colors=colors, explode=explode, autopct='%1.1f%%',
            textprops={'fontsize': 8})
    plt.title("College and University Counts by Locale Code")
    plt.legend(dict.keys(), loc="upper left", prop={'size': 6})
    return plt


# bar chart showing the counts of colleges and universities in each locale code

def bar_chart1(locales, count1, title):
    plt.figure()
    plt.bar(locales, count1, color="thistle", linewidth=4)
    plt.title(title)
    plt.xlabel("Locale Code")
    plt.ylabel("Count of Universities and Colleges")
    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    return plt


# creating the map using a data frame and pandas features to plot the locations on the map

def county_map(locations):
    map_df = pd.DataFrame(locations, columns=["school name", "X", "Y"])

    view_location = pdk.ViewState(
        latitude=map_df["Y"].mean(),
        longitude=map_df["X"].mean(),
        zoom=9,
        pitch=0)

    location_data = {
        "html": "University Name:<br/> <b>{school name}</b></br> Latitude: <b>{Y}</b><br/> Longitude: <b>{X}</b><br/>",
        "style": {"backgroundColor": "steelblue",
                  "color": "lavender"}
    }

    layer_county_map = pdk.Layer('ScatterplotLayer',
                                 data=map_df,
                                 get_position='[X, Y]',
                                 get_radius=400,
                                 radius_scale=2,
                                 get_color=[200, 66, 245],
                                 pickable=True
                                 )

    county_map1 = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_location,
        layers=[layer_county_map],
        tooltip=location_data
    )
    st.pydeck_chart(county_map1)


# main function to call all of the other functions

def main():
    # second application of the default parameter

    df_new = read_file("Postsecondary_School_Locations_-_Current (1).csv")

    # creating a professional appearance on the side bar of Streamlit

    st.sidebar.title("Universities and Colleges")
    st.sidebar.header("Map of Colleges and Universities in the United States")
    st.sidebar.subheader("County Map Selector")

    # data frame to list for county selection and Streamlit UI control

    county = df_new['NMCNTY'].unique().tolist()
    sort_county = sorted(county)
    countySelection = st.sidebar.selectbox("Select a county: ", sort_county)

    # letting the user know which county they selected

    st.write("The county you selected is ", countySelection)

    # creating a list to retrieve the name, lat, and lon of each school in a certain county

    locations = []
    for index, row in df_new.iterrows():
        if countySelection == row[11]:
            lon = row[0]
            lat = row[1]
            name = row[4]
            locations.append((name, lon, lat))

    # displaying the map on streamlit

    county_map(locations)

    # adding a subheader for chart 1 and chart 2

    st.sidebar.subheader("College and University Count Bar Chart")

    # data frame to list for state selection and Streamlit UI control

    states = df_new['STATE'].unique().tolist()
    sorted_states = sorted(states)
    stateSelection = st.sidebar.multiselect("Select states: ", sorted_states)

    # creating a dictionary and iterating through the state column in the dataframe to add the states to the dictionary

    state_dict = {}
    for state in stateSelection:
        count = 0
        for item in df_new["STATE"].iteritems():
            if item[1] == state:
                count += 1
        state_dict[state] = count
    dictionary = state_dict.keys()
    updated_dict = list(dictionary)
    new = ', '.join(updated_dict)

    # creating a title for the bar chart

    title = f'Count of Colleges and Universities in {new}'

    # adding a subheader for chart 3 and chart 4

    st.sidebar.subheader("Locale Code Selector")

    locales = df_new['LOCALE'].unique().tolist()
    sorted_locales = sorted(locales)
    localeSelection = st.sidebar.radio("Select a locale code: ", sorted_locales)

    localeIndex = locales.index(localeSelection)

    # creating a dictionary and iterating through the locale column in the dataframe to add the locale codes to the dictionary

    locale_dict = {}
    for locale in locales:
        count1 = 0
        for item in df_new["LOCALE"].iteritems():
            if item[1] == locale:
                count1 += 1
        locale_dict[locale] = count1

    # title for the chart 3

    title1 = f'Count of Colleges and Universities by Locale Code'

    # plotting the 4 graphs once a state is chosen for the state selection
    # waiting to show any charts until a state has been selected

    if len(stateSelection) > 0:
        # letting the user know which states they selected

        st.write("The states you selected are ", new)

        # plotting the state bar chart

        st.pyplot(bar_chart(state_dict.keys(), state_dict.values(), title))

        # plotting the state pie chart

        st.pyplot(pie_chart(state_dict, title))

        # plotting the locale code bar chart

        st.pyplot(bar_chart1(locale_dict.keys(), locale_dict.values(), title1))

        # plotting the locale code pie chart

        st.pyplot(pie_chart2(locale_dict, localeIndex))

        # letting the user know which locale code they selected and the
        # number of colleges and universities in that locale code

        st.write(f'You have selected locale code {localeSelection}.')
        st.write(f'Locale code {localeSelection} has {locale_dict[localeSelection]} colleges and universities.')


main()
