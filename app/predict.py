#library
import numpy as np
import streamlit as st
import pandas as pd

from sklearn.preprocessing import StandardScaler , MinMaxScaler
from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids
from sklearn.cluster import KMeans 

data_file = st.file_uploader("Upload CSV",type=["csv"])

if data_file is not None:
    df = pd.read_csv(data_file)
    
    scaler = StandardScaler()
    scaled_df = scaler.fit_transform(df)
    normalizer = MinMaxScaler()
    normalized_df = normalizer.fit_transform(scaled_df)

    st.table(normalized_df)

    kmedoids = KMedoids(n_clusters=3, random_state= 5 )
    y_kmedoids = kmedoids.fit_predict(normalized_df)
    centroids = kmedoids.cluster_centers_
    st.table(centroids)