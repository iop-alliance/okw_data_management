
__generated_with = "0.8.20"

# %%
import marimo as mo

# %%
from fastkml import kml
import pandas as pd
from datetime import datetime
now = datetime.now()
from __functions__ import req_data

# %%
google_map_url = "https://www.google.com/maps/d/u/0/viewer?mid=10q6m1yyAUzFn2zqDcRwq-qInUmvoVz4q&ll=37.844558%2C-122.27696200000003&z=8"

kml_url = "http://www.google.com/maps/d/kml?forcekml=1&mid=10q6m1yyAUzFn2zqDcRwq-qInUmvoVz4q"


# %%
mo.md(
    r"""
    Author: Antonio de Jesus Anaya Hernandez, DevOps eng. for the IoPA.

    Author: The internet of Production Alliance, 2023.

    Data was collected by "sridhar[at]upbeatlabs.com, and its partners", URL location: "https://www.google.com/maps/d/u/0/viewer?mid=10q6m1yyAUzFn2zqDcRwq-qInUmvoVz4q&ll=37.844558%2C-122.27696200000003&z=8"

    Data source license:

    The Open Know Where (OKW) Initiative is part of the Internet of Production Alliance and its members.

    License: CC BY SA

    ![CC BY SA](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)

    Description: Python code for downloading, parsing, filtering, sorting data, exporting the RAW makery locations, and the processed IOPA data as CSV.
    """
)

# %%
mo.md(
    r"""
    <img src="https://avatars.githubusercontent.com/u/61060916?s=200&v=4" width=80px style="text-align:right"><h1>The Internet of Production Alliance </h1>

    ## Data collection program for the [OKW, Map of facilities](https://www.internetofproduction.org/open-know-where)
    """
)

# %%
g_map = req_data(kml_url).content

# %%
kml_file = kml.KML()
kml_file.from_string(g_map)

# %%
features = list(kml_file.features())

# %%
f2 = list(features[0].features())

# %%
table = []

for folder in f2:
    for record in folder.features():
        table.append((record.name, record.geometry.x, record.geometry.y, folder.name))

# %%
output = pd.DataFrame(table, columns=['name', 'latitude', 'longitude', 'type'])

# %%
file = output.to_csv('data/source_03_' + now.strftime("%Y_%m_%d_%H%M") + '.csv', index=False)

# %%
print("OKW entries: {r[0]}, columns = {r[1]}".format(r=output.shape))
