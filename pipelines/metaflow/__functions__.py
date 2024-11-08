#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 07:51:41 2024

@author: kny5
"""



import requests
from time import sleep
import logging
import functools
import re
import numpy as np
import pandas as pd
from scipy.spatial import KDTree
from sklearn.cluster import DBSCAN



def retry_on_exception(max_retries=3, backoff_factor=1):
    """
    Decorator to retry a function on exception.

    Args:
        max_retries:
        backoff_factor:
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while True:
                try:
                    return func(*args, **kwargs)  # Execute and return the function result
                except requests.exceptions.RequestException as e:
                    if retries < max_retries:
                        sleep(backoff_factor * (retries + 1))
                        retries += 1
                    else:
                        raise e

        return wrapper

    return decorator


def req_data(url, timer=1, verbose=False, head={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'}):
    """
    Sends a GET request to the specified URL and returns the response.

    Args:
        url:
        timer:
        recursive:
        verbose:
    """
    @retry_on_exception(max_retries=5, backoff_factor=2)  # Increase max retries and backoff factor
    def inner():
        response = requests.get(url, headers=head)
        if response.status_code == 200:
            sleep(timer)
            if verbose:
                logging.info(f"URL: {url}")
                logging.info(f"Status Code: {response.status_code}")
            return response
        else:
            logging.error(f"Error Response: {response.status_code} ({url})")
            raise Exception("Request failed")

    return inner()  # Directly return the response





def marsh_json(dataframe):
    from data_models import ParserSchema
        
    _schema = ParserSchema()

    location_json_mapping = []
    for index, row in dataframe.iterrows():
        data_dict = {
        'latitude': row['latitude'],
        'longitude': row['longitude'],
        'zip_code': row['postal_code'],
        'extended': row['address_1'],
        'country': row['country_code'],
        'state_region': row['county'],
        'city_town': row['city'],
        'org_id': row['org_id'],
        'description': 'fablab',
        'name': row['name'],
        'url': row['url']
        }
        location_json_mapping.append(_schema.dumping(data_dict))
        
    return location_json_mapping



def filter_points_by_proximity(df, radius=100, min_points=2):
    # Drop rows with missing values in 'latitude' or 'longitude'
    df = df.dropna(subset=['latitude', 'longitude'])
    
    # Convert radius from meters to degrees
    radius_in_degrees = radius / 111_139  # Approximation for latitude/longitude degrees
    
    # Step 1: Extract latitude and longitude as a 2D numpy array
    coordinates = df[['latitude', 'longitude']].to_numpy()
    
    # Step 2: Cluster points with DBSCAN to find nearby groups
    clustering = DBSCAN(eps=radius_in_degrees, min_samples=1).fit(coordinates)
    labels = clustering.labels_
    
    # Step 3: Filter points based on proximity count within each cluster
    filtered_points = []
    unique_points = set()  # Keep track of unique points to remove duplicates
    
    for label in np.unique(labels):
        # Select points and subset of DataFrame in this cluster
        cluster_points = coordinates[labels == label]
        cluster_df = df[labels == label]
        
        # Use KDTree for efficient neighbor lookup within the cluster
        tree = KDTree(cluster_points)
        for i, point in enumerate(cluster_points):
            # Get neighbors within the 10-meter radius
            neighbors = tree.query_ball_point(point, radius_in_degrees)
            
            # Filter if it has enough nearby points
            if len(neighbors) >= min_points:
                # Convert the point to a tuple (latitude, longitude) for hashing
                point_tuple = tuple(cluster_df.iloc[i][['latitude', 'longitude']])
                
                # Check for duplicates; keep only the latest
                if point_tuple not in unique_points:
                    unique_points.add(point_tuple)
                    filtered_points.append(cluster_df.iloc[i])
    
    # Return the filtered, non-duplicate points as a DataFrame
    return pd.DataFrame(filtered_points)


def iter_request(url):
    data = []
    x = 0
    
    while True:
        response = requests.get(url.format(n=x))
        json_data = response.json()
        if not json_data:
            break
        data += json_data
        x += 1
        print('Pages: {p}'.format(p=x))
        print('Entries: {e}'.format(e=len(data)))
    return data


class ReverseGeocode:
    column_names = [
        "geonameid", "name", "asciiname", "alternatenames", "latitude", 
        "longitude", "feature class", "feature code", "country code", "cc2", 
        "admin1 code", "admin2 code", "admin3 code", "admin4 code", 
        "population", "elevation", "dem", "timezone", "modification date"
    ]
   
    def __init__(self, dataframe, output=['cc2', 'city']):
        self.df = dataframe
        read_cities = pd.read_csv('data/cities500.txt', names=self.column_names, delimiter='\t')
        geocodes = read_cities[['name', 'country code', 'latitude', 'longitude']].rename(
            columns={'country code': 'cc', 'latitude': 'lat', 'longitude': 'lon'}
        )
        # Initialize KDTree once for fast lookups
        self.tree = KDTree(geocodes[['lat', 'lon']])
    
    def nearest_neighbor(self, lat, lon):
        """Get nearest location info based on latitude and longitude."""
        _, idx = self.tree.query([lat, lon])
        row = self.geocodes.iloc[idx]
        return row['cc'], row['name']
    
    def get(self):
        """Process merged data for reverse geocoding."""
        self.df[['cc2', 'city']] = self.df.apply(lambda row: pd.Series(self.nearest_neighbor(row['latitude'], row['longitude'])), axis=1)
        
        return self.df


from fuzzywuzzy import fuzz
import unicodedata

def ngram_fingerprint(text, n=3):
    """
    Generate an n-gram fingerprint for a given text following specific normalization steps.

    Steps:
        1. Change all characters to lowercase.
        2. Remove all punctuation, whitespace, and control characters.
        3. Obtain all n-grams of the specified length.
        4. Sort the n-grams and remove duplicates.
        5. Join the sorted n-grams back together.
        6. Normalize extended Western characters to their ASCII representation.

    Parameters:
        text (str): The input text to be fingerprinted.
        n (int): The size of n-grams.

    Returns:
        str: The n-gram fingerprint.
    """
    # Step 1: Change all characters to lowercase
    text = text.lower()
    
    # Step 2: Remove all punctuation, whitespace, and control characters
    text = re.sub(r'[^\w]', '', text)
    
    # Step 3: Normalize extended Western characters to their ASCII representation
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    
    # Step 4: Obtain all n-grams
    ngrams = [text[i:i+n] for i in range(len(text) - n + 1)]
    
    # Step 5: Sort the n-grams and remove duplicates
    unique_ngrams = sorted(set(ngrams))
    
    # Step 6: Join the sorted n-grams back together
    fingerprint = ''.join(unique_ngrams)
    
    return fingerprint


def normalize_name(name):
    """Normalize names by removing punctuation, extra spaces, accents, and sorting words."""
    # Convert to lowercase
    name = name.lower()
    # Remove punctuation and extra spaces
    name = re.sub(r'[^\w\s]', '', name)
    # Remove accents
    name = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    # Sort words to handle reordering
    name = ' '.join(sorted(name.split()))
    return name

def cluster_and_aggregate(df, distance_threshold=100, similarity_threshold=0.8):
    """
    Clusters GPS points and aggregates URLs and sources of similar locations.
    
    Parameters:
        df (pd.DataFrame): DataFrame with columns 'name', 'lat', 'long', 'url', and 'source'.
        distance_threshold (float): Maximum distance (in meters) for clustering.
        similarity_threshold (float): Minimum similarity ratio (0.0 - 1.0) for names to be considered similar.
        
    Returns:
        pd.DataFrame: DataFrame with columns 'name', 'lat', 'long', and 'occurrences', where occurrences 
                      is a list of dictionaries containing 'url' and 'source' for each similar occurrence.
    """
    # Step 1: Normalize names in the DataFrame
    df['normalized_name'] = df['name'].apply(ngram_fingerprint)
    
    # Step 2: Cluster based on geographical coordinates using DBSCAN
    coordinates = df[['latitude', 'longitude']].to_numpy()
    db = DBSCAN(eps=distance_threshold / 6371000, min_samples=1, metric='haversine').fit(coordinates)
    df['cluster'] = db.labels_
    
    # Step 3: Group by cluster and process each cluster
    aggregated_data = []
    processed_names = set()  # Track processed names
    
    for cluster_id, cluster_df in df.groupby('cluster'):
        cluster_df = cluster_df.reset_index(drop=True)
        
        for idx, row in cluster_df.iterrows():
            norm_name = row['normalized_name']
            
            # Only process if the normalized name is not in processed_names
            if norm_name not in processed_names:
                # Filter for similar normalized names within the cluster
                similar_rows = cluster_df[
                    cluster_df['normalized_name'].apply(
                        lambda n: fuzz.token_sort_ratio(norm_name, n) / 100.0 >= similarity_threshold
                    )
                ]
                
                # Collect URLs and sources for each similar name
                # occurrences = similar_rows[['url', 'source']].to_dict(orient='records')
                aggregated_data.append({
                    'name': row['name'],
                    'latitude': row['latitude'],
                    'longitude': row['longitude'],
                    # 'occurrences': occurrences
                })
                
                # Add processed names to avoid duplications
                processed_names.update(similar_rows['normalized_name'])
    
    # Convert to DataFrame for output
    aggregated_df = pd.DataFrame(aggregated_data)
    return aggregated_df




def cluster_and_key_collision(df, distance_threshold=100, n=3):
    """
    Clusters GPS points, applies n-gram fingerprinting for collision detection, and aggregates URLs and sources.
    
    Parameters:
        df (pd.DataFrame): DataFrame with columns 'name', 'lat', 'long', 'url', and 'source'.
        distance_threshold (float): Maximum distance (in meters) for clustering.
        n (int): The n-gram size for fingerprinting.
        
    Returns:
        pd.DataFrame: DataFrame with columns 'name', 'lat', 'long', and 'occurrences', where occurrences 
                      is a list of dictionaries containing 'url' and 'source' for each similar occurrence.
    """
    # Step 1: Apply n-gram fingerprinting to the 'name' column
    df['name_fingerprint'] = df['name'].apply(lambda x: ngram_fingerprint(x, n))

    # Step 2: Cluster based on geographical coordinates using DBSCAN
    coordinates = df[['latitude', 'longitude']].to_numpy()
    db = DBSCAN(eps=distance_threshold / 6371000, min_samples=1, metric='haversine').fit(coordinates)
    df['cluster'] = db.labels_
    
    # Step 3: Group by cluster and process each cluster
    aggregated_data = []
    
    for cluster_id, cluster_df in df.groupby('cluster'):
        cluster_df = cluster_df.reset_index(drop=True)
        fingerprint_groups = cluster_df.groupby('name_fingerprint')
        
        for fingerprint, group in fingerprint_groups:
            # Get the first occurrence for latitude and longitude
            first_row = group.iloc[0]
            
            # Collect URLs and sources for each entry with the same fingerprint
            # occurrences = group[['url', 'source']].to_dict(orient='records')
            aggregated_data.append({
                'name': first_row['name'],
                'latitude': first_row['latitude'],
                'longitude': first_row['longitude'],
                # 'occurrences': occurrences
            })
    
    # Convert to DataFrame for output
    aggregated_df = pd.DataFrame(aggregated_data)
    return aggregated_df
