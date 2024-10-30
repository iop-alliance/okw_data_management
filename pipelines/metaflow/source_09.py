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
from __functions__ import req_data, ReverseGeocode
import json
# import re
from bs4 import BeautifulSoup as soup


class Source_09(FlowSpec):
    
    url = Parameter('url', default="https://wiki.hackerspaces.org/List_of_Hacker_Spaces")
    
    @step
    def start(self):
        self.next(self.extract)
    
    @step
    def extract(self):
        
        html_parser = soup(req_data(self.url).text, 'html.parser')
        #print(html_parser)
        data = html_parser.find("div", {"class": "mapdata"}).text
        print(data)
        self.raw = json.loads(data).get("locations", [])
        
        self.data = pd.DataFrame(self.raw)
        
        # self.raw = req_data(self.url).text
        
        # self.data = pd.read_csv(io.StringIO(self.raw))
        # self.data.reset_index(drop=True, inplace=True)
        
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
    
# __generated_with = "0.8.20"

# # %%
# import marimo as mo

# # %%
# # This line installs the required libraries for running the script, uncomment the line:
# # !pip install -r requirements.txt

# # %%
# import requests
# import pandas as pd
# import json
# import io

# # %%
# from datetime import datetime
# now = datetime.now()

# # %%
# mo.md(
#     r"""
#     <img src="https://avatars.githubusercontent.com/u/61060916?s=200&v=4" width=80px style="text-align:right"><h1>The Internet of Production Alliance </h1>

#     ## Data collection program for the [OKW, Map of facilities](https://www.internetofproduction.org/open-know-where)
#     """
# )

# # %%
# mo.md(
#     r"""
#     Author: Antonio de Jesus Anaya Hernandez, DevOps eng. for the IoPA.

#     Author: The internet of Production Alliance, 2023.

#     Data was collected by "Hackerspaces.org, and its partners", URL location: https://hackerspaces.org

#     Data source license:

#     The Open Know Where (OKW) Initiative is part of the Internet of Production Alliance and its members.

#     License: CC BY SA

#     ![CC BY SA](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)

#     Description: Python code for downloading, parsing, filtering, sorting data, exporting the RAW makery locations, and the processed IOPA data as CSV.
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
# url = "https://wiki.hackerspaces.org/w/index.php?title=Special%3AAsk&_action=submit&q=%5B%5BCategory%3AHackerspace%5D%5D+%5B%5BHackerspace+status%3A%3Aactive%5D%5D&po=%3FCountry%0D%0A%3FState%0D%0A%3FCity%0D%0A%3FWebsite%0D%0A%3FLast+Updated%0D%0A%3FEmail&eq=yes&p%5Bformat%5D=csv&p%5Blimit%5D=5000&p%5Boffset%5D=400&p%5Blink%5D=all&p%5Bheaders%5D=show&p%5Bmainlabel%5D=hackerspace&p%5Bintro%5D=&p%5Boutro%5D=&p%5Bsearchlabel%5D=...+further+results&p%5Bdefault%5D=&p%5Bsep%5D=%2C&p%5Bvaluesep%5D=%2C&p%5Bfilename%5D=result.csv&sort_num%5B%5D=Last+Updated&order_num%5B%5D=desc&sort_num%5B%5D=&order_num%5B%5D=asc&eq=yes&ask=on"
# data = req_data(url)
# print(type(data))

# # %%
# input_ = pd.read_csv(io.StringIO(data.text))

# # %%
# input_.reset_index(drop=True, inplace=True)

# # %%
# input_.columns.tolist()

# # %%
# output = input_.drop(columns=[])

# # %%
# input_.to_csv('data/raw_source_09_' + now.strftime("%Y_%m_%d_%H%M") + '.csv')

# # %%
# print("OKW entries: {r[0]}, columns = {r[1]}".format(r=input_.shape))

# # %%
# output.to_csv('data/source_09_' + now.strftime("%Y_%m_%d_%H%M") + '.csv')
