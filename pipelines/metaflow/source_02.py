#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 07:51:41 2024

@author: kny5
"""



from metaflow import FlowSpec, step, card, Parameter
import pandas as pd
from __visualisations__ import Plot, Tabular
from __functions__ import req_data, filter_points_by_proximity



class Source_02(FlowSpec):
    
    url = Parameter('url', default="https://api.fablabs.io/0/labs.json")
    radius_ = Parameter('radius', default=100)
    min_points_ = Parameter('min_points', default=2)
    
    @step
    def start(self):
        print(self.__class__.__name__)
        self.next(self.extract)
    
    @step
    def extract(self):
        self.raw = req_data(self.url).json()
        self.data = pd.DataFrame(self.raw)
        self.data.reset_index(drop=True, inplace=True)
        print(self.data.columns.tolist())
        self.next(self.clean)
    
    @card(type='html')
    @step
    def clean(self):
        c_transform = self.data[self.data['activity_status'] != 'closed']
        n_transform = c_transform[c_transform['activity_status'] != 'planned']
        d_transform = filter_points_by_proximity(n_transform, radius=int(self.radius_), min_points=int(self.min_points_))
        e_transform = n_transform[['name', 'latitude', 'longitude']]
        self.validata = e_transform[~e_transform.isin(d_transform).all(axis=1)]
        self.output = self.validata.drop_duplicates(subset=['latitude', 'longitude', 'name'], keep='last')
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
    Source_02()
