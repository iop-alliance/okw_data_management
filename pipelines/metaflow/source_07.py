#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 07:51:41 2024

@author: kny5
"""



import json
import re
from bs4 import BeautifulSoup as soup
from metaflow import FlowSpec, step, card, Parameter
import pandas as pd
from __visualisations__ import Plot, Tabular
from __functions__ import req_data



class Source_07(FlowSpec):
    
    url = Parameter('url', default="https://www.offene-werkstaetten.org/widgets/search?colorA=74ac61&colorB=0489B1&customMarkerSrc=https://cdn0.iconfinder.com/data/icons/map-location-solid-style/91/Map_-_Location_Solid_Style_06-48.png&customClusterSrc=https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-ios7-circle-filled-48.png")
    radius_ = Parameter('radius', default=5)
    min_points_ = Parameter('min_points', default=4)
    
    @step
    def start(self):
        print("Starting...")
        self.next(self.extract)
    
    @step
    def extract(self):
        html_parser = [x.text for x in soup(req_data(self.url).text, 'html.parser').find_all('script') if 'vow.Map' in x.text][-1]
        data = '[{"' + re.findall(r'\[{"(.*?)"\}\]\,', html_parser)[0] + '"}]'
        self.raw = json.loads(data)
        self.data = pd.DataFrame(self.raw)
        print(self.data.columns.tolist())
        self.next(self.clean)
    
    @card(type='html')
    @step
    def clean(self):
        self.data['latitude'] = self.data['lat']
        self.data['longitude'] = self.data['lng']
        self.output = self.data[['name','latitude','longitude']]
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
    Source_07()


