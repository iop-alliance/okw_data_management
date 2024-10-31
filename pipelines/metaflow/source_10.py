from metaflow import FlowSpec, step, card, Parameter
import pandas as pd
from itables import to_html_datatable
from __visualisations__ import Plot
from __functions__ import req_data, filter_points_by_proximity



class Source_10(FlowSpec):
    
    url = Parameter('url', default="https://makery.gogocarto.fr/api/elements.json")
    radius_ = Parameter('radius', default=100)
    min_points_ = Parameter('min_points', default=2)
    
    @step
    def start(self):
        self.next(self.extract)
    
    @step
    def extract(self):
        data = req_data(self.url).json()
        self.raw = pd.json_normalize(data, 'data')
        self.next(self.clean)
    
    @card(type='html')
    @step
    def clean(self):
        rn = self.raw.rename(columns={'id': 'makery_id','site_web': 'url', 'geo.latitude': 'latitude', 'geo.longitude': 'longitude'})
        filtered = rn[rn['status'] != 'closed']
        self.duplicates = filter_points_by_proximity(filtered, radius=int(self.radius_), min_points=int(self.min_points_))
        self.html = to_html_datatable(self.duplicates, display_logo_when_loading=True, buttons=[
            "pageLength",
            {"extend": "csvHtml5", "title": "Duplicates Source 02"},
            {"extend": "excelHtml5", "title": "Duplicates Source 02"},],)
        self.data = filtered[['name', 'latitude', 'longitude']]
        self.output = self.data[~self.data.isin(self.duplicates).all(axis=1)]
        
        self.next(self.transform)
    
    @step
    def transform(self):
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
    Source_10()

