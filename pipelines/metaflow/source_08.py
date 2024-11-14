#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 07:51:41 2024

@author: kny5
"""



from metaflow import FlowSpec, step, card
import pandas as pd
from __visualisations__ import Plot, Tabular
from okw_libs.dwld import req_data
from okw_libs.g_maps import extract_kml_data, extract_urls



class Source_08(FlowSpec):
    
    url = "https://www.google.com/maps/d/u/0/viewer?mid=123W1JzyYEJlCg3Dh21OcTCLIknk-s_Y&ll=38.418307201373004%2C-100.67343475982062&z=5"
        
    @step
    def start(self):
        self.next(self.extract)
    
    @step
    def extract(self):
        self.raw = extract_kml_data(self.url, req_data)
        self.next(self.clean)
        
    
    @step
    def clean(self):
        self.data = [(record.name, record.geometry.y, record.geometry.x) for folder in list(list(self.raw.features())[0].features()) for record in folder.features()]
        self.data['web_url'] = self.data['description'].apply(extract_urls)
        self.output = pd.DataFrame(self.data, columns=['name', 'latitude', 'longitude'])
        self.count = "OKW entries: {r[0]}, columns: {r[1]}, info: {c}".format(r=self.output.shape, c=self.output.columns.tolist())
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
    

if __name__ == '__main__':
    Source_08()