description ='''
Author: Antonio de Jesus Anaya Hernandez, DevOps eng. for the IoPA.

Author: The internet of Production Alliance, 2023.

Data was collected by "MAke works and it's partners" at "https://make.works/companies?page={n}&format=json"

Data source license: Limited

The Open Know Where (OKW) Initiative is part of the Internet of Production Alliance and its members.

License: CC BY SA

![CC BY SA](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)

Description: Python code for downloading, parsing, filtering, sorting data, exporting the RAW makery locations, and the processed IOPA data as CSV.

<img src="https://avatars.githubusercontent.com/u/61060916?s=200&v=4" width=80px style="text-align:right"><h1>The Internet of Production Alliance </h1>

## Data collection program for the [OKW, Map of facilities](https://www.internetofproduction.org/open-know-where)
'''


from datetime import datetime
now = datetime.now()
from metaflow import FlowSpec, step, card, Parameter
# from metaflow.cards import Markdown

import pandas as pd
from itables import to_html_datatable
from __visualisations__ import Plot
from __functions__ import filter_points_by_proximity, iter_request

update_date = now.strftime("%Y_%m_%d_%H%M")


class Source_06(FlowSpec):
    
    url = Parameter('url', default="https://make.works/companies?page={n}&format=json")
    radius_ = Parameter('radius', default=100)
    min_points_ = Parameter('min_points', default=2)
    
    @step
    def start(self):
        print("Starting...")
        self.next(self.extract)
    
    @card
    @step
    def extract(self):
        self.raw = iter_request(self.url)
        self.data = pd.DataFrame(self.raw)
        self.data.reset_index(drop=True, inplace=True)
        self.data.to_csv('data/iopa/raw_source_06_' + update_date + '.csv')
        print(self.data.columns.tolist())
        self.next(self.clean)
    
    @card(type='html')
    @step
    def clean(self):
        self.data['latitude'] = self.data['lat']
        self.data['longitude'] = self.data['lng']
        n_transform = self.data[['latitude', 'longitude', 'name']]
        d_transform = filter_points_by_proximity(n_transform, radius=int(self.radius_), min_points=int(self.min_points_))
        self.html = to_html_datatable(d_transform, display_logo_when_loading=True, buttons=[
            "pageLength",
            {"extend": "csvHtml5", "title": "Duplicates Source 02"},
            {"extend": "excelHtml5", "title": "Duplicates Source 02"},],)
        e_transform = n_transform[['name', 'latitude', 'longitude']]
        self.validata = e_transform[~e_transform.isin(d_transform).all(axis=1)]
        print(self.validata.columns.tolist())
        self.next(self.transform)
    
    @step
    def transform(self):
        self.output = self.validata.drop_duplicates(subset=['latitude', 'longitude', 'name'], keep='last')
        print(self.output.columns.tolist())
        self.next(self.load)
    
    @step
    def load(self):
        
        self.output.to_csv('data/iopa/iopa_source_06_' + update_date + '.csv')
        self.next(self.data_table)
    
        
    @card(type='html')
    @step
    def data_table(self):
        self.html = to_html_datatable(self.output, display_logo_when_loading=True, buttons=[
        "pageLength",
        {"extend": "csvHtml5", "title": "Manufacturing Locations"},
        {"extend": "excelHtml5", "title": "Manufacturing Locations"},],)
        
        self.next(self.data_map)
    
    
    @card(type='html')
    @step
    def data_map(self):
        self.html = Plot(self.output).render()
        self.next(self.end)
    
    @step    
    def end(self):
        print("Success")


if __name__ == "__main__":
    Source_06()