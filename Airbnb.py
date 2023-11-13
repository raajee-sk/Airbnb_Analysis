#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importing Libraries
import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
# Setting up page configuration

# Creating option menu in the side bar
st.set_page_config(layout='wide')
option = st.radio(':red[**Select your option**]',('Home','OverView','Explore'),horizontal=True)

# CREATING CONNECTION WITH MONGODB ATLAS AND RETRIEVING THE DATA
client = pymongo.MongoClient("mongodb+srv://raajeesk:atx1c1d1@cluster0.f14yrhp.mongodb.net/")
db = client.sample_airbnb
col = db.listingsAndReviews

# READING THE CLEANED DATAFRAME
df = pd.read_csv('C:\\Users\\SKAN\\Downloads\\Airbnb_data.csv')

# HOME PAGE

if option=="Home":  # Title Image
 st.markdown(
    f"<h1 style='color:#ff6666; font-size: 20px;'>AIRBNB DATA ANALYSIS</h1>",
    unsafe_allow_html=True,)
 c=Image.open("C:\\Users\\SKAN\\Downloads\\airbnb.jpg")
 st.image(c)
 
 st.markdown(
    f"<h1 style='color:#ff6666; font-size: 20px;'>Domain:Travel Industry, Property Management and Tourism</h1>",
    unsafe_allow_html=True,)
 st.markdown(
    f"<h1 style='color:#ff6666; font-size: 20px;'>Technologies used: Python, Pandas, Plotly, Streamlit, MongoDB</h1>",
    unsafe_allow_html=True,)
 st.markdown(
    f"<h1 style='color:#ff6666; font-size: 20px;'>Overview: To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.</h1>",
    unsafe_allow_html=True,)
      
# OVERVIEW PAGE
if option == "OverView":
    tab1,tab2=st.tabs(['Raw Data','Insight'])

     # RAW DATA TAB
    with tab1:
        # RAW DATA
        col1,col2 = st.columns(2)
        if col1.button("Click to view Raw data"):
            st.write(col.find_one())
        # DATAFRAME FORMAT
        if col2.button("Click to view Dataframe"):
            st.dataframe(df)  
     # INSIGHTS TAB
    with tab2:
        col1,col2=st.columns(2)
        # AVG PRICE IN COUNTRIES SCATTERGEO
        with col1:
         country_df = df.groupby('Country',as_index=False)['Price'].mean()
         fig = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Price', 
                                       hover_data=['Price'],
                                       locationmode='country names',
                                       size='Price',
                                       title= 'Avg Price in each Country',
                                       color_continuous_scale='agsunset'
                            )
         st.plotly_chart(fig,use_container_width=True)
  
         
# AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        with col2:
         country_df = df.groupby('Country',as_index=False)['Availability_365'].mean()
         country_df.Availability_365 = country_df.Availability_365.astype(int)
         fig = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Availability_365', 
                                       hover_data=['Availability_365'],
                                       locationmode='country names',
                                       size='Availability_365',
                                       title= 'Avg Availability in each Country',
                                       color_continuous_scale='agsunset'
                            )
        st.plotly_chart(fig,use_container_width=True)      
                            
        
        col1,col2,col3=st.columns(3)
        # TOP 10 PROPERTY TYPES BAR CHART
        with col1:
            fig=plt.figure(figsize=(5,5))
            ax = sns.countplot(data=df,y=df.Property_type,order=df.Property_type.value_counts().index[:10])
            ax.set_title("Top 10 Property Types available")
            st.pyplot(fig,use_container_width=True)
         # TOP 10 PROPERTY TYPES BAR CHART  
        with col2:
            fig1=plt.figure(figsize=(8,8))
            ax = sns.countplot(data=df,x=df.Room_type)
            ax.set_title("Total Listings in each Room Type")
            st.pyplot(fig1,use_container_width=True)

        # TOP 10 HOSTS BAR CHART  
        with col3:
           fig2=plt.figure(figsize=(5,5))
           ax = sns.countplot(data=df,y=df.Host_name,order=df.Host_name.value_counts().index[:10])
           ax.set_title("Top 10 Hosts with Highest number of Listings")
           st.pyplot(fig2,use_container_width=True)
                
            
# EXPLORE PAGE
if option == "Explore":
    st.markdown(
    f"<h1 style='color:#ff6666; font-size: 20px;'>Explore more about the Aiebnb Data</h1>",
    unsafe_allow_html=True,)
# GETTING USER INPUTS
    country = st.selectbox('Select a Country',sorted(df.Country.unique()))
    prop = st.selectbox('Select Property_type',sorted(df.Property_type.unique()))
    room=st.selectbox('Select Room_type',sorted(df.Room_type.unique()))
   
    button=st.button("Search")
    if button:
# CONVERTING THE USER INPUT INTO QUERY                
     df1=df[(df["Country"]==country)&(df["Property_type"]==prop)&(df["Room_type"]==room)]
     df2=df1[["Country","Name","Host_name","Property_type","Room_type","Price"]].sort_values(by="Price",ascending=False).reset_index(drop=True)
     st.markdown(
    f"<h1 style='color:#ff6666; font-size: 20px;'>Room Availability</h1>",
    unsafe_allow_html=True,)
     st.dataframe(df2)
       
    
     col1,col2 = st.columns(2)
     with col1:
        st.markdown(
    f"<h1 style='color:#ff6666; font-size: 20px;'>Price Analysis</h1>",
    unsafe_allow_html=True,)
        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df.groupby(['Room_type','Country'],as_index=False)['Price'].mean().sort_values(by='Price',ascending=False)
        fig = px.bar(data_frame=pr_df,
                     x='Room_type',
                     y='Price',
                     color='Country',
                     title='Avg Price in each Room type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
        
     with col2:   
        # AVAILABILITY BY ROOM TYPE BOX PLOT
        st.markdown(
    f"<h1 style='color:#ff6666; font-size: 20px;'>Availability Analysis</h1>",
    unsafe_allow_html=True,)
        av_df = df.groupby(['Room_type','Country'],as_index=False)['Availability_365'].mean().sort_values(by='Availability_365',ascending=False)
        fig = px.bar(data_frame=av_df,
                     x='Room_type',
                     y='Availability_365',
                     color='Country',
                     title='Availability by Room_type'
                    )
        st.plotly_chart(fig,use_container_width=True)
    
        
        

