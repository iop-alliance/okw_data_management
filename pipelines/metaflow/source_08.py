description ='''
Author: Antonio de Jesus Anaya Hernandez, DevOps eng. for the IoPA.

Author: The internet of Production Alliance, 2023.

Data was collected by "sridhar[at]upbeatlabs.com, and its partners", URL location: "https://www.google.com/maps/d/u/0/viewer?mid=10q6m1yyAUzFn2zqDcRwq-qInUmvoVz4q&ll=37.844558%2C-122.27696200000003&z=8"

Data source license:

The Open Know Where (OKW) Initiative is part of the Internet of Production Alliance and its members.

License: CC BY SA

![CC BY SA](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)

Description: Python code for downloading, parsing, filtering, sorting data, exporting the RAW makery locations, and the processed IOPA data as CSV.

<img src="https://avatars.githubusercontent.com/u/61060916?s=200&v=4" width=80px style="text-align:right"><h1>The Internet of Production Alliance </h1>

## Data collection program for the [OKW, Map of facilities](https://www.internetofproduction.org/open-know-where)
'''

# %%

# %%
from datetime import datetime
now = datetime.now()
from metaflow import FlowSpec, step, card, Parameter
# from pretty_html_table import build_table
# from metaflow.cards import Markdown

import pandas as pd
from itables import to_html_datatable
from __visualisations__ import Plot
from __functions__ import extract_kml_data

class Source_08(FlowSpec):
    
    url = Parameter('url', default="https://www.google.com/maps/d/u/0/viewer?mid=123W1JzyYEJlCg3Dh21OcTCLIknk-s_Y&ll=38.418307201373004%2C-100.67343475982062&z=5")
        
    @step
    def start(self):
        self.next(self.extract)
    
    @step
    def extract(self):
        self.raw = extract_kml_data(self.url)
        self.next(self.transform)
    
    
    @step
    def transform(self):
        self.data = [(record.name, record.geometry.y, record.geometry.x) for folder in list(list(self.raw.features())[0].features()) for record in folder.features()]
        self.output = pd.DataFrame(self.data, columns=['name', 'latitude', 'longitude'])
        self.count = "OKW entries: {r[0]}, columns: {r[1]}, info: {c}".format(r=self.output.shape, c=self.output.columns.tolist())
        self.next(self.load)
   
    @step
    def load(self):
        #self.output.to_csv('data/iopa/iopa_source_04_' + now.strftime("%Y_%m_%d_%H%M") + '.csv', index=False)
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
    
    @card
    @step
    def end(self):
        pass
    

if __name__ == '__main__':
    Source_08()