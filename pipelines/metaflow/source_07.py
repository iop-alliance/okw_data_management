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
from __functions__ import req_data, ReverseGeocode



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
    
    @step
    def clean(self):
        self.data['record_source_url'] = self.data.url.apply(lambda x: 'https://offene-werkstaetten.org/werkstatt/' + x)
        self.data.rename(columns={'lat':'latitude', 'lng': 'longitude', 'web': 'web_url'}, inplace=True)
        self.output = self.data[['name','latitude','longitude','record_source_url', 'web_url']]
        self.next(self.transform)
    
    @card(type='html')
    @step
    def transform(self):
        self.geocode = ReverseGeocode(self.output).get()
        self.html = Tabular(self.geocode).table_output()
        self.next(self.visualise)
    
        
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
        self.html = Plot(self.output.dropna(subset=['latitude','longitude'])).render()
        self.next(self.wrapup)
        
    @step
    def data_stats(self):
        self.count = "OKW entries: {r[0]}, columns: {r[1]}, info: {c}".format(r=self.output.shape, c=self.output.columns.tolist())
        self.next(self.wrapup)
    
    @step
    def wrapup(self, inputs):
        self.output = inputs[0].output
        self.next(self.end)
    
    @step    
    def end(self):
        print("Success")


if __name__ == "__main__":
    Source_07()


