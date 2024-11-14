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
from okw_libs.g_maps import extract_kml_data, kml_object_to_dict, parse_description



class Source_03(FlowSpec):
    
    url = "https://www.google.com/maps/d/u/0/viewer?mid=10q6m1yyAUzFn2zqDcRwq-qInUmvoVz4q&ll=37.844558%2C-122.27696200000003&z=8"
        
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
        filter_30 = filter_20['description'].apply(parse_description).apply(pd.Series)
        self.data = pd.concat([filter_20, filter_30], axis=1).drop(columns=['description', 'ns', 'styleUrl'])
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
    Source_03()