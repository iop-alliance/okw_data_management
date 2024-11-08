#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 07:51:41 2024

@author: kny5
"""


from metaflow import FlowSpec, step, card, Parameter
import pandas as pd
from __visualisations__ import Plot, Tabular
# from __functions__ import filter_points_by_proximity, iter_request
from okw_libs.dwld import iter_request



class Source_06(FlowSpec):
    
    url = "https://make.works/companies?page={n}&format=json"
    radius_ = Parameter('radius', default=1)
    min_points_ = Parameter('min_points', default=3)
    
    @step
    def start(self):
        print("Starting...")
        self.next(self.extract)
    
    @card
    @step
    def extract(self):
        self.raw = iter_request(self.url)
        self.data = pd.DataFrame(self.raw)
        print(self.data.columns.tolist())
        self.next(self.clean)
    
    @card(type='html')
    @step
    def clean(self):
        self.data['latitude'] = self.data['lat']
        self.data['longitude'] = self.data['lng']
        # n_transform = self.data[['latitude', 'longitude', 'name']]
        # d_transform = filter_points_by_proximity(n_transform, radius=int(self.radius_), min_points=int(self.min_points_))
        # e_transform = n_transform[['name', 'latitude', 'longitude']]
        # self.output = e_transform[~e_transform.isin(d_transform).all(axis=1)]
        filter_10 = self.data[['name','latitude','longitude']]
        self.output = filter_10.drop_duplicates(subset=['name'])
        print(self.output.columns.tolist())
        self.next(self.visualise)
    
    # @step
    # def transform(self):
    #     self.next(self.load)
    
    # @step
    # def load(self):        
    #     self.next(self.data_table, self.data_map)
    
        
    @step
    def visualise(self):
        self.next(self.data_table, self.data_map)
    
        
    @card(type='html')
    @step
    def data_table(self):
        self.html = Tabular(self.output).table_output()
        self.next(self.join)
    
    
    @card(type='html')
    @step
    def data_map(self):
        self.html = Plot(self.output.dropna(subset=['latitude','longitude'])).render()
        self.next(self.join)
    
    @step
    def join(self, inputs):
        self.output = inputs[0].output
        self.next(self.end)
    
    @step    
    def end(self):
        print("Success")


if __name__ == "__main__":
    Source_06()
