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
    
    @step
    def clean(self):
        self.raw.rename(columns={'id': 'makery_id', 'status': 'makery_status', 'site_web': 'url', 'geo.latitude': 'latitude', 'geo.longitude': 'longitude'})
        self.next(self.transform)
    
    @step
    def transform(self):
        self.data = self.raw[self.raw['makery_status'] != 'closed']
        self.output = self.data[['name','latitude','longitude']]
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




# __generated_with = "0.8.20"

# # %%
# import marimo as mo

# # %%
# import requests
# import pandas as pd

# # %%
# from datetime import datetime
# now = datetime.now()

# # %%
# drops = ['sourceKey', 'categoriesFull', 'article_makery', 'fullAddress', 'mode_gestion', 'subscriberEmails', 'address.customFormatedAddress', 'description_courte', 'surface', 'telephone', 'images', 'openHours.Mo', 'openHours.Tu', 'openHours.We', 'openHours.Th', 'openHours.Fr', 'address.streetNumber', 'address.streetAddress', 'address.addressLocality', 'address.postalCode', 'address.addressCountry', 'affiliation', 'description', 'openHours.Sa', 'openHours.Su', 'makery_status','createdAt', 'updatedAt','makery_url','categories','makery_id']

# # %%


# # %%
# mo.md("""\n    Author: Antonio de Jesus Anaya Hernandez, DevOps eng. for the IoPA.\n\n    Author: The internet of Production Alliance, 2023.\n\n    Data was collected by "Makery, gogocarto, and its partners", URL location: https://makery.gogocarto.fr/api\n\n    Data source license: ODBL 1.0, Open Data Commons Open Database License\n\n    The Open Know Where (OKW) Initiative is part of the Internet of Production Alliance and its members.\n\n    License: CC BY SA\n\n    ![CC BY SA](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)\n\n    Description: Python code for downloading, parsing, filtering, sorting data, exporting the RAW makery locations, and the processed IOPA data as CSV.\n""")

# # %%
# mo.md(
#     """
#     <img src="https://avatars.githubusercontent.com/u/61060916?s=200&v=4" width=80px style="text-align:right"><h1>The Internet of Production Alliance </h1>

#     ## Data collection program for the [OKW, Map of facilities](https://www.internetofproduction.org/open-know-where)
#     """
# )

# # %%
# def req_data(url):

#     response = requests.get(url)

#     print(response.status_code)

#     if response.status_code == 200:
#         return response
#     else:
#         print("Error response: Check URL or internet avalability, and Try again.")
#         print(url)

# # %%
# url = 'https://makery.gogocarto.fr/api/elements.json'
# data = req_data(url).json()
# print(type(data))

# # %%
# data_ = pd.DataFrame(data)

# # %%
# input_d = pd.DataFrame(data_.data)
# print(input_d.shape)
# from pandas import json_normalize
# input_ = pd.json_normalize(input_d['data'])

# # %%
# input_.to_csv('data/raw_source_10_' + now.strftime('%Y_%m_%d_%H%M') + '.csv')

# # %%
# transform = input_.rename(columns={'id': 'makery_id', 'status': 'makery_status', 'site_web': 'url', 'geo.latitude': 'latitude', 'geo.longitude': 'longitude'})

# # %%
# input_.columns.tolist()

# # %%
# input_.reset_index(drop=True, inplace=True)

# # %%
# active_spaces = transform[transform['makery_status'] != 'closed']

# # %%
# transform['makery_url'] = transform.apply(lambda row: 'https://makery.gogocarto.fr/map#/fiche/{name}/{id}/'.format(name=str(row['name']).replace(' ', '-'), id=row['makery_id']), axis=1)

# # %%
# real_spaces = active_spaces[active_spaces['makery_status'] != 'planned']

# # %%
# real_spaces['address_composed'] = real_spaces['address.streetNumber'].astype(str) + ', ' + real_spaces['address.streetAddress'].astype(str) + ', ' + real_spaces['address.addressLocality'].astype(str) + ', ' + real_spaces['address.postalCode'].astype(str) + ', ' + real_spaces['address.addressCountry'].astype(str)

# # %%
# output = real_spaces.drop(columns=drops)

# # %%
# output.to_csv('data/source_10_' + now.strftime('%Y_%m_%d_%H%M') + '.csv')

# # %%
# print('OKW entries: {r[0]}, columns = {r[1]}'.format(r=output.shape))

# # %%
# output.columns.tolist()
