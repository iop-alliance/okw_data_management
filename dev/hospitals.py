#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 12:08:24 2024

@author: kny5
"""

import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from geopy.distance import geodesic

# Load datasets A and B
# Replace 'path_to_dataset_A.csv' and 'path_to_dataset_B.csv' with your dataset paths
dataset_B = pd.read_csv('locations.csv')  # Dataset A with columns ['lat', 'lon']
dataset_A = pd.read_csv('hospitals.csv')  # Dataset B with columns ['lat', 'lon']

# Clustering points in dataset B
def cluster_points(data, eps_km=1):
    """
    Cluster points in a dataset using DBSCAN.
    eps_km: The maximum distance between two samples for them to be considered as in the same neighborhood, in kilometers.
    """
    # Convert eps from kilometers to radians (DBSCAN uses radians for haversine metric)
    eps_rad = eps_km / 6371.0  # Earth radius in kilometers
    
    # Convert lat/lon to radians for haversine distance metric
    coords = np.radians(data[['latitude', 'longitude']])
    
    # Perform DBSCAN clustering
    dbscan = DBSCAN(eps=eps_rad, min_samples=1, metric='haversine')
    clusters = dbscan.fit_predict(coords)
    
    # Add cluster labels to the data
    data['cluster'] = clusters
    return data

# Cluster dataset B
clustered_B = cluster_points(dataset_B, eps_km=1)  # Adjust eps_km as needed

# Compute cluster centroids
cluster_centroids = (
    clustered_B.groupby('cluster')[['latitude', 'longitude']]
    .mean()
    .reset_index()
    .rename(columns={'latitude': 'centroid_lat', 'longitude': 'centroid_lon'})
)

# Function to filter dataset A based on proximity to clustered points
def filter_points(dataset_A, cluster_centroids, max_distance_km=5):
    """
    Filters out points from dataset A that are within max_distance_km of any cluster centroid in dataset B.
    """
    filtered_data = []

    for _, row in dataset_A.iterrows():
        point = (row['latitude'], row['longitude'])
        within_distance = False

        for _, centroid in cluster_centroids.iterrows():
            centroid_point = (centroid['centroid_lat'], centroid['centroid_lon'])
            distance = geodesic(point, centroid_point).kilometers
            if distance <= max_distance_km:
                within_distance = True
                break
        
        if not within_distance:
            filtered_data.append(row)
    
    return pd.DataFrame(filtered_data)

# Filter dataset A
filtered_A = filter_points(dataset_A, cluster_centroids, max_distance_km=5)

# Save the filtered dataset A
filtered_A.to_csv('filtered_dataset_A.csv', index=False)
print("Filtered dataset A saved to 'filtered_dataset_A.csv'.")
