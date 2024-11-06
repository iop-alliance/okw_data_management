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
from __functions__ import req_data, filter_points_by_proximity


class Source_12(FlowSpec):
        
    url = Parameter('url', default="https://github.com/kny5/db/raw/refs/heads/db_global/Global.sqlite")
    radius_ = Parameter('radius', default=100)
    min_points_ = Parameter('min_points', default=5)
    
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
        filter_1 = pd.concat([filter_0, self.patch], ignore_index=True)
        filter_2 = filter_1[['name','latitude','longitude']].drop_duplicates(keep='last')
        filter_3 = filter_points_by_proximity(filter_2, radius=self.radius_, min_points=self.min_points_)
        self.output = filter_2[~filter_2.isin(filter_3).all(axis=1)]
        self.html = Tabular(filter_3).table_output()
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
    Source_12()