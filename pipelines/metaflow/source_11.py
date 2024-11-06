#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 07:51:41 2024

@author: kny5
"""



from metaflow import FlowSpec, step, card, Parameter
import pandas as pd
from __visualisations__ import Plot, Tabular
from __functions__ import req_data


class Source_11(FlowSpec):
    
    url = Parameter('url', default="https://makerspace.com/wp-json/makerspaces/v1/spacedata/5/")
    radius_ = Parameter('radius', default=100)
    min_points_ = Parameter('min_points', default=2)
    
    @step
    def start(self):
        self.next(self.extract)
    
    @card(type='html')
    @step
    def extract(self):
        data = req_data(self.url).json()
        self.raw = pd.json_normalize(data, 'Makerspaces')
        self.html = Tabular(self.raw).table_output()
        self.next(self.clean)
    
    @card(type='html')
    @step
    def clean(self):
        self.raw['latitude'] = pd.to_numeric(self.raw['lat'], errors='coerce')
        self.raw['longitude'] = pd.to_numeric(self.raw['long'], errors='coerce')
        self.output = self.raw[['name','latitude','longitude']]
        self.html_2 = Tabular(self.output).table_output()
        # self.next(self.transform)
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
    Source_11()
