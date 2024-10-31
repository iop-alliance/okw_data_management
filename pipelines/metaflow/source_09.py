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

from metaflow import FlowSpec, step, card, Parameter
import pandas as pd
from itables import to_html_datatable
from __visualisations__ import Plot
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
        self.next(self.transform)

    @step
    def transform(self):
        
        self.output = self.data[['name','latitude','longitude']]
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
        pass
        

if __name__ == "__main__":
    Source_09()
