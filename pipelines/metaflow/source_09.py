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
import json
from bs4 import BeautifulSoup as soup


class Source_09(FlowSpec):
    
    url = Parameter('url', default="https://wiki.hackerspaces.org/List_of_Hacker_Spaces")
    
    @step
    def start(self):
        self.next(self.extract)
    
    @step
    def extract(self):
        html_parser = soup(req_data(self.url).text, 'html.parser')
        data = html_parser.find("div", {"class": "mapdata"}).text
        print(data)
        self.raw = json.loads(data).get("locations", [])
        self.data = pd.DataFrame(self.raw)
        self.next(self.clean)
        
    @step
    def clean(self):
        self.data.rename(columns={'lat': 'latitude', 'lon': 'longitude', 'title': 'name'}, inplace=True)
        self.output = self.data[['name','latitude','longitude']]
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
    Source_09()
