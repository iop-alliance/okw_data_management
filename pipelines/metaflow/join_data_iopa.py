#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 06:17:15 2024

@author: kny5
"""


# create workspaces/tag prod, test and dev
# get flows from each workspace/tag
# run merge join strategy on each workspace/tag


import pandas as pd
from metaflow import FlowSpec, step, Flow, card
from __visualisations__ import Plot
from itables import to_html_datatable


class JoinData01(FlowSpec): 
    @step
    def start(self):
        # Define the sources from which to fetch data
        self.sources = [
            Flow('Source_02').latest_successful_run,
            Flow('Source_03').latest_successful_run,
            Flow('Source_04').latest_successful_run,
            Flow('Source_05').latest_successful_run,
            Flow('Source_06').latest_successful_run,
            Flow('Source_07').latest_successful_run,
            Flow('Source_08').latest_successful_run,
            Flow('Source_09').latest_successful_run,
            Flow('Source_10').latest_successful_run,
        ]
        # Initialize an empty DataFrame to append sources
        self.append_source = pd.DataFrame(columns=['name', 'latitude', 'longitude'])
        self.next(self.get_data, foreach='sources')
    
    @step
    def get_data(self):
        # Access the 'output' attribute of the latest run in each source
        self.data = self.input.data.output  # Assuming 'output' exists in each source
        self.next(self.join)
        
    @step
    def join(self, inputs):
        # Concatenate the data collected from each input in get_data step
        self.append_source = pd.concat([inp.data for inp in inputs], ignore_index=True)
        self.next(self.clean)
        
    @step
    def clean(self):
        self.output = self.append_source.drop_duplicates(subset=['latitude', 'longitude'], keep='last')
        self.next(self.data_table)
        
    @card(type='html')
    @step
    def data_table(self):
        self.html = to_html_datatable(self.output, display_logo_when_loading=True, buttons=[
         "pageLength",
         {"extend": "csvHtml5", "title": "Manufacturing Locations"},
         {"extend": "excelHtml5", "title": "Manufacturing Locations"},],)
        self.next(self.data_map)
    
    @card(type='html')
    @step
    def data_map(self):
        self.html = Plot(self.output).render()
        self.next(self.end)
    
    @step
    def end(self):
        # Print the final combined DataFrame
        print(self.append_source)

if __name__ == "__main__":
    JoinData01()
