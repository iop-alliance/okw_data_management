
__generated_with = "0.8.20"

# %%
import marimo as mo

# %%
#!pip install fastkml lxml

# %%
from fastkml import kml

# %%
import requests
import pandas as pd

# %%
from datetime import datetime
now = datetime.now()

# %%
kml_url = "http://www.google.com/maps/d/kml?forcekml=1&mid=1wKXDd1rOs4ls1EiZswQr-upFq7o"

# %%


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

    Data was collected by "University of Michigan 3D Lab, and its partners", URL location: "https://www.google.com/maps/d/u/0/viewer?mid=1wKXDd1rOs4ls1EiZswQr-upFq7o&ll=38.418307201373004%2C-100.67343475982062&z=5"

    Data source license:

    The Open Know Where (OKW) Initiative is part of the Internet of Production Alliance and its members.

    License: CC BY SA

    ![CC BY SA](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)

    Description: Python code for downloading, parsing, filtering, sorting data, exporting the RAW makery locations, and the processed IOPA data as CSV.
    """
)

# %%
def req_data(url):

    response = requests.get(url)

    print(response.status_code)

    if response.status_code == 200:
        return response
    else:
        print("Error response: Check URL or internet avalability, and Try again.")
        print(url)

# %%
g_map = req_data(kml_url).content

# %%
kml_file = kml.KML()
kml_file.from_string(g_map)

# %%
features = list(kml_file.features())

# %%
table = []

for folder in list(features[0].features()):
    f = folder.features()
    for record in f:
        table.append((record.name, record.geometry.x, record.geometry.y, folder.name))

# %%
output = pd.DataFrame(table, columns=['name', 'latitude', 'longitude', 'type'])

# %%
output.to_csv('data/source_04_' + now.strftime("%Y_%m_%d_%H%M") + '.csv')

# %%
print("OKW entries: {r[0]}, columns = {r[1]}".format(r=output.shape))
