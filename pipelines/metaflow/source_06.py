#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 07:51:41 2024

Author: Antonio de Jesus Anaya Hernandez
Role: DevOps Engineer
Organization: Internet of Production Alliance
Description: 
This script implements a Metaflow pipeline for extracting, transforming, 
and visualizing data from the Make.Works API. The data is processed into a 
cleaned format suitable for visualization in tabular and map formats.
"""

from metaflow import FlowSpec, step, card, Parameter
import pandas as pd
from __visualisations__ import Plot, Tabular
from __functions__ import ReverseGeocode
from okw_libs.dwld import iter_request


class Source_06(FlowSpec):
    """
    Metaflow pipeline class to manage the data flow:
    Extract, clean, and visualize data from the Make.Works API.
    """

    # URL of the Make.Works API with pagination placeholder
    url = "https://make.works/companies?page={n}&format=json"

    # Pipeline parameters with default values
    radius_ = Parameter('radius', default=1, help="Radius value for proximity filtering")
    min_points_ = Parameter('min_points', default=3, help="Minimum number of points for proximity filtering")
    
    @step
    def start(self):
        """
        Initial step of the pipeline.
        Prepares for data extraction.
        """
        print("Starting...")
        self.next(self.extract)
    
    @card
    @step
    def extract(self):
        """
        Extract step.
        Fetches raw data from the Make.Works API and converts it into a DataFrame.
        """
        self.raw = iter_request(self.url)  # Fetch data from API
        self.data = pd.DataFrame(self.raw)  # Convert to DataFrame
        print(self.data.columns.tolist())  # Print column names for debugging
        self.next(self.clean)
    
    @card(type='html')
    @step
    def clean(self):
        """
        Clean step.
        Renames and filters columns to create a standardized output dataset.
        """
        # Rename columns for clarity and standardization
        self.data.rename(columns={
            'url': 'record_source_url',
            'lat': 'latitude',
            'lng': 'longitude',
            'website': 'web_url'
        }, inplace=True) 
        print(self.data.columns.tolist())
        # Select relevant columns for further processing
        self.output = self.data[['name', 'latitude', 'longitude', 'record_source_url', 'web_url']]
        print(self.output.columns.tolist())  # Print column names for debugging
        self.next(self.transform)

    @card(type='html')
    @step
    def transform(self):
        self.geocode = ReverseGeocode(self.output).get()
        self.html = Tabular(self.geocode).table_output()
        self.next(self.visualise)
    
    @step
    def visualise(self):
        """
        Visualization step.
        Routes the cleaned data to tabular and map-based visualization tasks.
        """
        self.next(self.data_table, self.data_map)
    
    @card(type='html')
    @step
    def data_table(self):
        """
        Tabular visualization step.
        Converts the cleaned data into an HTML table.
        """
        self.html = Tabular(self.output).table_output()  # Generate table visualization
        self.next(self.join)
    
    @card(type='html')
    @step
    def data_map(self):
        """
        Map visualization step.
        Generates an interactive map from the cleaned data.
        """
        # Drop rows with missing latitude/longitude and create a map visualization
        self.html = Plot(self.output.dropna(subset=['latitude', 'longitude'])).render()
        self.next(self.join)
    
    @step
    def join(self, inputs):
        """
        Join step.
        Combines the outputs of the tabular and map visualizations.
        """
        self.output = inputs[0].output  # Use the output from the first input (data_table)
        self.next(self.end)
    
    @step    
    def end(self):
        """
        End step.
        Finalizes the pipeline and confirms successful execution.
        """
        print("Success")


if __name__ == "__main__":
    Source_06()

