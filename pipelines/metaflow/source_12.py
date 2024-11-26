#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 07:51:41 2024

@author: kny5
"""



import sqlite3
from metaflow import FlowSpec, step, card, Parameter
import pandas as pd
from __visualisations__ import Plot, Tabular
from __functions__ import req_data, filter_points_by_proximity, ReverseGeocode



class Source_12(FlowSpec):
        
    url = Parameter('url', default="https://github.com/kny5/db/raw/refs/heads/db_global/Global.sqlite")
    radius_ = Parameter('radius', default=100)
    min_points_ = Parameter('min_points', default=2)
    
    @step
    def start(self):
        self.next(self.extract)
    
    @card(type='html')
    @step
    def extract(self):
        response = req_data(self.url)
        local_file = "Global.sqlite"
        
        with open(local_file, 'wb') as f:
            f.write(response.content)

        con = sqlite3.connect(local_file)
        self.raw = pd.read_sql_query("SELECT * from field_ready_verified", con)
        self.patch = pd.read_sql_query("SELECT * from patch_01", con)
        con.close()
        
        print(self.raw.info())
        self.html = Tabular(self.raw).table_output()
        self.next(self.clean)
        
    @card(type='html')
    @step
    def clean(self):
        self.patch['latitude'] = pd.to_numeric(self.patch['latitude'], errors='coerce')
        self.patch['longitude'] = pd.to_numeric(self.patch['longitude'], errors='coerce')
        self.raw['latitude'] = pd.to_numeric(self.raw['location-Latitude'], errors='coerce')
        self.raw['longitude'] = pd.to_numeric(self.raw['location-Longitude'], errors='coerce')
        filter_0 = self.raw[~self.raw['country'].isin(['iraq', 'somalia', 'somaliland'])]
        filter_a = pd.concat([filter_0, self.patch], ignore_index=True)
        filter_1 = filter_a[filter_a['name'].str.len() >= 4]
        filter_1.rename(columns={'social_fb': 'web_url'}, inplace=True)
        filter_2 = filter_1[['name','latitude','longitude','web_url']].drop_duplicates(keep='last')
        filter_3 = filter_points_by_proximity(filter_2, radius=self.radius_, min_points=self.min_points_)
        print(self.raw.columns.tolist())
        self.output = filter_2[~filter_2.isin(filter_3).all(axis=1)]
        self.html = Tabular(filter_3).table_output()
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
    Source_12()