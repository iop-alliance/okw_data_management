#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 07:51:41 2024

@author: kny5
"""



from metaflow import FlowSpec, step, card, Parameter
import pandas as pd
from __visualisations__ import Plot, Tabular
from okw_libs.dwld import req_data



class Source_02(FlowSpec):
    
    url = "https://api.fablabs.io/0/labs.json"
    radius_ = Parameter('radius', default=100)
    min_points_ = Parameter('min_points', default=2)
    
    @step
    def start(self):
        print(self.__class__.__name__)
        self.next(self.extract)
    @card(type='html')
    @step
    def extract(self):
        self.raw = req_data(self.url).json()
        self.data = pd.DataFrame(self.raw)
        self.html = Tabular(self.data).table_output()
        print(self.data.columns.tolist())
        self.next(self.clean)
    
    @step
    def clean(self):
        filter_10 = self.data[~self.data['activity_status'].isin(['closed', 'planned'])]
        # d_transform = filter_points_by_proximity(n_transform, radius=int(self.radius_), min_points=int(self.min_points_))
        # self.validata = e_transform[~e_transform.isin(d_transform).all(axis=1)]
        self.cleaned = filter_10.drop_duplicates(subset=['name'], keep='last')
        self.next(self.transform)
    
    @step
    def transform(self):
        self.cleaned['record_source_url'] = 'https://www.fablabs.io/labs/' + self.cleaned.slug
        # Convert the JSON string in 'links' to a Python object, and then extract the URL
        # Directly access the first element of the 'links' list, and check for the 'url' key
        self.cleaned['web_url'] = self.cleaned['links'].apply(lambda x: x[0]['url'] if isinstance(x, list) and len(x) > 0 else None)
        self.output = self.cleaned[['name', 'latitude', 'longitude','record_source_url','web_url']]
        self.next(self.visualise)
    
    # @step
    # def load(self):        
    #     self.next(self.data_table, self.data_map)
    
        
    @step
    def visualise(self):
        self.next(self.data_table, self.data_map, self.data_stats)
        
    @card(type='html')
    @step
    def data_table(self):
        self.html = Tabular(self.output).table_output()
        self.next(self.wrapup)
    
    
    @card(type='html')
    @step
    def data_map(self):
        self.html = Plot(self.output).render()
        self.next(self.wrapup)
        
    @card(type='html')
    @step
    def data_stats(self):
        self.next(self.wrapup)
    
    @step
    def wrapup(self, inputs):
        self.output = inputs[0].output
        self.next(self.end)
    
    @step    
    def end(self):
        print("Success")


if __name__ == "__main__":
    Source_02()
