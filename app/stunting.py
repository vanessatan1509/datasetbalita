#Library
import numpy as np
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import matplotlib.pyplot as plt

import psycopg2
import sys
sys.path.append('/path/to/module')
from sklearn.metrics import pairwise_distances
from streamlit_option_menu import option_menu
from datetime import date
from psycopg2 import connect, Error
from sklearn.preprocessing import StandardScaler , MinMaxScaler
from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids
from sklearn.cluster import KMeans 

#Project Title
st.title(""" Stunting Prediction """)

# Initialize connection.
@st.cache_resource
def init_connection():
    try:
        return psycopg2.connect(**st.secrets["postgres"])
    except Error as e:
        print(e)

conn = init_connection()

#Function insert data 
def insert_record(name, gender, birthdate, age, weight, height):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO public.stunting(name, gender, birthdate, age, weight, height) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING", (name, gender, birthdate, age, weight, height))
        conn.commit()

#Function read data
def read_records():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM public.stunting")
        records = cursor.fetchall()
        return records

#Function select data untuk diproses 
def prosesdata_records():
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, gender, age, weight, height FROM public.stunting")
        records = cursor.fetchall()
        return records

#Function select data untuk dinormalisasi
def normalizeddata_records():
    with conn.cursor() as cursor:
        cursor.execute("SELECT age, weight, height FROM public.stunting")
        records = cursor.fetchall()
        return records

#Funciton update data
def update_record(name, gender, birthdate, age, weight, height, id):
    with conn.cursor() as cursor:
        cursor.execute("UPDATE public.stunting SET name = %s, gender = %s, birthdate = %s, age = %s, weight = %s, height = %s WHERE id = %s", (name, gender, birthdate, age, weight, height, id))
        conn.commit()

#Function delete data
def delete_record(id):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM public.stunting WHERE id = %s", (id))
        conn.commit()

#K-Medoid clustering
def kmedoids_clustering (X, n_clusters):
    D = pairwise_distances(X, metric='euclidean')
    kmedoids = KMedoids(n_clusters=n_clusters, random_state=42)
    kmedoids.fit(D)
    return kmedoids.cluster_centers_


#Side Bar
with st.sidebar :
    nav_bar = option_menu(
        menu_title = "Main Menu",
        options = ["Home" , "About" , "Predict", "Database" , "Admin"],
        icons = ["house-door-fill" , "person-fill" , "question-octagon-fill" , "file-earmark-fill" , "gear-fill"],
        menu_icon = "cast",
        default_index = 0,
)

#Menu Home
if nav_bar == "Home":
    st.write("Stunting is defined as low height-for-age. It is the result of chronic or recurrent undernutrition, usually associated with poverty, poor maternal health and nutrition, frequent illness and/or inappropriate feeding and care in early life. Stunting prevents children from reaching their physical and cognitive potential.")

  

#Menu About   
elif nav_bar == "About":
    st.title(f"You Have Selected {nav_bar}")

#Menu Predict
elif nav_bar == "Predict":
    data_file = st.file_uploader("Upload CSV",type=["csv"])
    if data_file is not None:
        df = pd.read_csv(data_file)
        df_view_filtered = df[['Nama Balita', 'Jenis Kelamin', 'Umur (Bulan)', 'Tinggi Badan (cm)', 'Berat Badan (kg)']]
        df_view_filtered = df_view_filtered.dropna(subset=["Nama Balita", "Jenis Kelamin", "Umur (Bulan)", "Tinggi Badan (cm)", "Berat Badan (kg)"])
        st.dataframe(df_view_filtered)
        df_view_filtered['Jenis Kelamin'].replace(['P', 'L'], [0, 1], inplace=True)
        
        for index, row in df_view_filtered.iterrows():
            insert_record(row["Nama Balita"], row["Jenis Kelamin"], '2001-09-15' , row["Umur (Bulan)"], row["Tinggi Badan (cm)"], row["Berat Badan (kg)"])

        scaler = StandardScaler()
        scaled_df = scaler.fit_transform(normalizeddata_records())
        normalizer = MinMaxScaler()
        normalized_df = normalizer.fit_transform(scaled_df)

        st.write (normalized_df)
        klaster_slider = st.slider(min_value = 2, max_value = 10, value = 2, label = "Number of Clusters : ")
        col1, col2 = st.columns(2)
        
        st.write(normalizeddata_records())

        #kmedoids_clustering(normalizeddata_records, klaster_slider)
        with col1:
            kmeans = KMeans(max_iter=1,n_init=1,n_clusters=klaster_slider, random_state=5)
            kmeans.fit(normalizeddata_records())
            centeroid = kmeans.cluster_centers_
            st.write("Centeroids")
            st.write(centeroid)
            pred1 = kmeans.predict(normalizeddata_records())
            st.write(pred1)

        
        #with col2:
        kmedoids = KMedoids(n_clusters=klaster_slider, random_state=25)
        kmedoids.fit(normalizeddata_records())
        centeroid = kmedoids.cluster_centers_
        st.write("Centeroids")
        st.write(centeroid)
        #st.write(pred2)
        st.write(labels)
        st.write (normalizeddata_records())


#Menu Database
if nav_bar == "Database":
    st.title("Input")
    name = st.text_input("Enter your Child Name : ",max_chars =50)
    gender = st.radio(
        "Choose your child gender : ",
        ('Female', 'Male',)
    )
    birthdate = st.date_input(
        "Enter your child birthdate : ", 
        min_value = date(1950, 1, 1), 
        max_value = date.today(),
    )
    umur = (date.today() - birthdate).days // 31
    age = st.write(f"Your Child Age :  {umur}")
    weight = st.number_input("Enter your Child weight : ")
    height = st.number_input("Enter your Child height : ")
    
    if st.button('Add'):
        insert_record(name,gender,birthdate,umur,weight,height)
        st.success('akhirnya')
        
#Menu Admin
if nav_bar == "Admin":
    st.title(f"You Have Selected {nav_bar}")
    st.table(prosesdata_records())
    st.write("Mau Hapus Data ?")
    id = st.number_input("Input Id",value=0, step=1)
    if st.button('Delete'):
        delete_record()
        st.success("berhasil")