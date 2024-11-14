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
from okw_libs.g_maps import extract_kml_data, kml_object_to_dict, extract_urls



class Source_04(FlowSpec):
    
    url = "https://www.google.com/maps/d/u/0/viewer?mid=1wKXDd1rOs4ls1EiZswQr-upFq7o&ll=38.418307201373004%2C-100.67343475982062&z=5"
        
    @step
    def start(self):
        self.next(self.extract)
    
    @step
    def extract(self):
        self.raw = extract_kml_data(self.url, req_data)
        self.next(self.clean)
    
    @card(type='html')
    @step
    def clean(self):
        filter_10 = [kml_object_to_dict(record) for folder in list(list(self.raw.features())[0].features()) for record in folder.features()]
        filter_20 = pd.DataFrame(filter_10)
        filter_20['web_url'] = filter_20['description'].apply(extract_urls)
        self.data = filter_20.drop(columns=['ns', 'styleUrl'])
        self.html = Tabular(self.data).table_output()
        self.next(self.visualise)
    
    # @step
    # def transform(self):
    #     self.next(self.load)
    
    # @step
    # def load(self):        
    #     self.next(self.data_table, self.data_map)
    
        
    @step
    def visualise(self):
        self.output = self.data[['name','latitude', 'longitude', 'web_url']]
        self.next(self.data_table, self.data_map, self.data_stats)
    
    @card(type='html')
    @step
    def data_table(self):
        self.html = Tabular(self.output).table_output()
        self.next(self.wrapup)
    
    @card(type='html')
    @step
    def data_map(self):
        self.html = Plot(self.output.dropna(subset=['latitude','longitude'])).render()
        self.next(self.wrapup)
        
    @card(type='html')
    @step
    def data_stats(self):
        self.count = "OKW entries: {r[0]}, columns: {r[1]}, info: {c}".format(r=self.output.shape, c=self.output.columns.tolist())
        self.next(self.wrapup)
    
    @step
    def wrapup(self, inputs):
        # self.output = inputs[0].output
        self.next(self.end)
    
    @step    
    def end(self):
        print("Success")
    

if __name__ == '__main__':
    Source_04()