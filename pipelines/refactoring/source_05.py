
__generated_with = "0.8.20"

# %%
import marimo as mo

# %%
# This line installs the required libraries for running the script, uncomment the line:
# !pip install -r requirements.txt

# %%
import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
from datetime import datetime

# %%
#notes: notebooks will change to only collect raw data, and generate DB metadata on preparation for data aggregation process. Cleaning and sorting will be arreanged on following notebooks fro data validation and cleansing.

# %%
"""
meta.json
Entries, column_names, creation_date
"""

# %%
mo.md(
    r"""
    <img src="https://avatars.githubusercontent.com/u/61060916?s=200&v=4" width=80px style="text-align:right"><h1>The Internet of Production Alliance </h1>

    ## Data collection program for the [OKW, Map of facilities](https://www.internetofproduction.org/open-know-where)
    """
)

# %%
mo.md(
    r"""
    Author: Antonio de Jesus Anaya Hernandez, DevOps eng. for the IoPA.

    Author: The internet of Production Alliance, 2023.

    Data was collected by "Makertour, and its partners", URL location: https://www.makertour.fr/workshops/

    The Open Know Where (OKW) Initiative is part of the Internet of Production Alliance and its members.

    License: CC BY SA

    ![CC BY SA](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)

    Description: Python code for downloading, parsing, filtering, sorting data, exporting the RAW FabLabs, and the processed IOPA data as CSV.
    """
)

# %%
def extract_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    title = soup.find('h2', class_='workshop-title').text.strip()
    location = soup.find('span', class_='city-country').text.strip()
    tags = [tag.text.strip() for tag in soup.find_all('span', class_='tag primary')]
    href = soup.find('a', class_='card-link')['href'].strip()

    return [title] + location.split(", ") + [tags, "https://www.makertour.fr" + href]

# %%
date = datetime.now().strftime("%Y_%m_%d_%H%M")
url = "https://www.makertour.fr/map"
org_name = "Maker Tour"
response = requests.get(url)
print(response)

# %%
file_name = "raw_" + org_name.replace(" ", "_").lower() + date

# %%
html_bytes = response.content
html_string = html_bytes.decode('utf-8')

soup = BeautifulSoup(html_string, 'html.parser')
map_content = soup.find('div', id='map')
markers_string = map_content.get('data-markers')

markers_json = json.loads(markers_string)

# %%
data = []
for record in markers_json:

    data.append(extract_info(record['content']) + [record['lat'], record['lng']])

columns = ['name', 'city', 'country', 'tags', 'url', 'latitude', 'longitude']

# %%
input_ = pd.DataFrame(data, columns=columns)

# %%
input_.columns.tolist()

# %%
print("OKW entries: {r[0]}, columns = {r[1]}".format(r=input_.shape))

# %%
metadata = {
    "source": org_name,
    "url": url,
    "csv": file_name,
    "records": input_.shape[0],
    "columns": input_.shape[1],
    "attributes": input_.columns.tolist(),
    "updated": date
}

# Serializing json
metadata_json = json.dumps(metadata, indent=4)

# Writing to sample.json
with open("data/" + "source_05" + ".json", "w") as outfile:
    outfile.write(metadata_json)

# %%
input_.reset_index(drop=True, inplace=True)

# %%
input_.to_csv('data/' + 'source_05' + '.csv')
