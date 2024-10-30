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


import json
from bs4 import BeautifulSoup
from metaflow import FlowSpec, step, card, Parameter
import pandas as pd
from itables import to_html_datatable
from __visualisations__ import Plot
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
        
        self.next(self.transform)
    
    def clean(self):
        pass
        # self.next(self.transform)
    
    @step
    def transform(self):
        self.output = self.data[['name', 'latitude', 'longitude']]
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
        pass



if __name__ == "__main__":
    Source_05()


# url = "https://www.makertour.fr/map"

# response = requests.get(url)
# print(response)

# # %%
# file_name = "raw_" + org_name.replace(" ", "_").lower() + date

# # %%
# html_bytes = response.content
# html_string = html_bytes.decode('utf-8')

# soup = BeautifulSoup(html_string, 'html.parser')
# map_content = soup.find('div', id='map')
# markers_string = map_content.get('data-markers')

# markers_json = json.loads(markers_string)

# # %%
# data = []
# for record in markers_json:

#     data.append(html_collector(record['content']) + [record['lat'], record['lng']])

# columns = ['name', 'city', 'country', 'tags', 'url', 'latitude', 'longitude']

# # %%
# input_ = pd.DataFrame(data, columns=columns)

# # %%
# input_.columns.tolist()

# # %%
# print("OKW entries: {r[0]}, columns = {r[1]}".format(r=input_.shape))

# # %%
# input_.reset_index(drop=True, inplace=True)

# # %%
# input_.to_csv('data/' + 'source_05' + '.csv')
