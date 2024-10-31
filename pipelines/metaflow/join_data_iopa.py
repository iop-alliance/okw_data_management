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
from metaflow import FlowSpec, step, Flow, card, resources
from __visualisations__ import Plot, Tabular


class JoinData01(FlowSpec):
    
    @resources(memory=6000, cpu=6, gpu=1)
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
            Flow('Source_11').latest_successful_run,
        ]
        # Initialize an empty DataFrame to append sources
        self.append_source = pd.DataFrame(columns=['name', 'latitude', 'longitude'])
        self.next(self.get_data, foreach='sources')
    
    @step
    def get_data(self):
        # Access the 'output' attribute of the latest run in each source
        self.data = self.input.data.output
        self.next(self.join)
        
    @step
    def join(self, inputs):
        # Concatenate the data collected from each input in get_data step
        self.append_source = pd.concat([inp.data for inp in inputs], ignore_index=True)
        self.next(self.visualise)
        
    @step
    def visualise(self):
        # self.output = self.append_source.drop_duplicates(subset=['latitude', 'longitude'], keep='last')
        self.output = self.append_source
        self.next(self.data_table, self.data_map)
        
    @card(type='html')
    @step
    def data_table(self):
        self.html = Tabular(self.output).table_output()
        self.next(self.join_2)
    
    @card(type='html')
    @step
    def data_map(self):
        self.html = Plot(self.output, max_cluster_rad=30).render()
        self.next(self.join_2)
        
    @step
    def join_2(self, inputs):
        self.next(self.end)
    
    @step
    def end(self):
        print(self.output)

if __name__ == "__main__":
    JoinData01()
