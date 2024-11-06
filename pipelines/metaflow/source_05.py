#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 07:51:41 2024

@author: kny5
"""



import json
from bs4 import BeautifulSoup
from metaflow import FlowSpec, step, card, Parameter
import pandas as pd
from __visualisations__ import Plot, Tabular
from __functions__ import req_data


def html_collector(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    title = soup.find('h2', class_='workshop-title').text.strip()
    location = soup.find('span', class_='city-country').text.strip()
    tags = [tag.text.strip() for tag in soup.find_all('span', class_='tag primary')]
    href = soup.find('a', class_='card-link')['href'].strip()

    return [title] + location.split(", ") + [tags, "https://www.makertour.fr" + href]



class Source_05(FlowSpec):
    
    url = Parameter('url', default="https://www.makertour.fr/map")
    
    @step
    def start(self):
        
        self.next(self.extract)
    
    @step
    def extract(self):
        html = req_data(self.url).content.decode('utf-8')
        html_parse_json = BeautifulSoup(html, 'html.parser').find('div', id='map').get('data-markers')
        json_data = json.loads(html_parse_json)
        
        self.raw = []
        for record in json_data:
            self.raw.append(html_collector(record['content']) + [record['lat'], record['lng']])

        columns = ['name', 'city', 'country', 'tags', 'url', 'latitude', 'longitude']
        self.data = pd.DataFrame(self.raw, columns=columns)
        
        self.next(self.clean)
    
    @step
    def clean(self):
        self.output = self.data[['name', 'latitude', 'longitude']]
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
    Source_05()
