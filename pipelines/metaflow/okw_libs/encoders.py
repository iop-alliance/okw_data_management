#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 22:38:11 2024

@author: kny5
"""



import hashlib
import unicodedata
import re

def normalize_text(text):
    """
    Normalizes text by removing accents, converting to lowercase,
    stripping whitespace, and removing non-alphanumeric characters.
    """
    text = str(text)
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ASCII', 'ignore').decode('ASCII')
    text = text.lower()
    text = text.strip()
    text = re.sub(r'\W+', '', text)  # Remove non-alphanumeric characters
    return text

def generate_unique_identifier(row):
    """
    Generates a deterministic unique identifier for each entry,
    combining the specified fields and hashing them.
    """
    # Round latitude and longitude to 2 decimal places
    lat = round(float(row['lat']), 2)
    long = round(float(row['long']), 2)
    
    # Convert rounded lat and long to strings
    lat_str = str(lat)
    long_str = str(long)
    
    # Normalize the required fields
    lat_norm = normalize_text(lat_str)
    long_norm = normalize_text(long_str)
    country = normalize_text(row['country'])  # Should be ISO alpha-2 code
    name = normalize_text(row['name'])
    town = normalize_text(row['town'])  # Replace with town code if available
    type_ = normalize_text(row['type'])
    
    # Create a unique string by concatenating the normalized fields
    unique_string = f"{lat_norm}|{long_norm}|{country}|{name}|{town}|{type_}"
    
    # Compute a SHA-256 hash of the unique string
    uid_hash = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()
    
    # Truncate the hash to get a fixed-length UID (e.g., 12 characters)
    uid = uid_hash[:12]
    
    # The unique identifier
    unique_identifier = f"{uid}"
    
    return unique_identifier

# # Sample DataFrame for demonstration
# df = pd.DataFrame({
#     'lat': [40.7128, 34.0522, 40.7128],
#     'long': [-74.0060, -118.2437, -74.0060],
#     'country': ['US', 'US', 'US'],  # Using ISO alpha-2 country codes
#     'name': ['New York', 'Los Angeles', 'New York'],
#     'town': ['Manhattan', 'Downtown', 'Manhattan'],
#     'type': ['City', 'City', 'City']
# })

# # Apply the function to each row in the DataFrame to create the 'unique_identifier' column
# df['unique_identifier'] = df.apply(generate_unique_identifier, axis=1)

# # Display the DataFrame with the new unique identifiers
# print(df[['name', 'unique_identifier']])
