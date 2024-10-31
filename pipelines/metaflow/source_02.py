description ='''
Author: Antonio de Jesus Anaya Hernandez, DevOps eng. for the IoPA.

Author: The internet of Production Alliance, 2023.

Data was collected by "Fab Foundation and it's partners" at "https://api.fablabs.io/0/labs.json"

Data source license: Limited

The Open Know Where (OKW) Initiative is part of the Internet of Production Alliance and its members.

License: CC BY SA

![CC BY SA](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)

Description: Python code for downloading, parsing, filtering, sorting data, exporting the RAW makery locations, and the processed IOPA data as CSV.

<img src="https://avatars.githubusercontent.com/u/61060916?s=200&v=4" width=80px style="text-align:right"><h1>The Internet of Production Alliance </h1>

## Data collection program for the [OKW, Map of facilities](https://www.internetofproduction.org/open-know-where)
'''


from metaflow import FlowSpec, step, card, Parameter
import pandas as pd
from itables import to_html_datatable
from __visualisations__ import Plot
from __functions__ import req_data, filter_points_by_proximity



class Source_02(FlowSpec):
    
    url = Parameter('url', default="https://api.fablabs.io/0/labs.json")
    radius_ = Parameter('radius', default=100)
    min_points_ = Parameter('min_points', default=2)
    
    @step
    def start(self):
        print("Starting...")
        self.next(self.extract)
    
    @step
    def extract(self):
        self.raw = req_data(self.url).json()
        self.data = pd.DataFrame(self.raw)
        self.data.reset_index(drop=True, inplace=True)
        print(self.data.columns.tolist())
        self.next(self.clean)
    
    @card(type='html')
    @step
    def clean(self):
        c_transform = self.data[self.data['activity_status'] != 'closed']
        n_transform = c_transform[c_transform['activity_status'] != 'planned']
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
    Source_02()
