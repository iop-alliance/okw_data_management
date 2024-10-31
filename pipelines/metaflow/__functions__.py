import requests
from time import sleep
import logging
import functools
from fastkml import kml
import re
import numpy as np
import pandas as pd
from scipy.spatial import KDTree


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


def extract_kml_data(gmap_URL):
    """

    Args:
        gmap_URL:

    Returns:

    """

    pattern = r"mid=(\w+-\w+)"
    match = re.search(pattern, gmap_URL)
    mid_value = ""
    if not match:
        print("No 'mid' value found in the URL.")
    else:
        mid_value += match.group(1)
        print(f"The extracted 'mid' value is: {mid_value}")

    kml_url = "http://www.google.com/maps/d/kml?forcekml=1&mid=" + mid_value
    g_map = req_data(kml_url)
    kml_file = kml.KML()
    kml_file.from_string(g_map.content)

    return kml_file


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


from sklearn.cluster import DBSCAN
from scipy.spatial import KDTree

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
