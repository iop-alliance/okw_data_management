
__generated_with = "0.8.20"

# %%
import marimo as mo

# %%
import requests
import pandas as pd
import json
import io

# %%
from datetime import datetime
now = datetime.now()

# %%
#input_.Makerspaces

# %%
mo.md(
    """
    <img src="https://avatars.githubusercontent.com/u/61060916?s=200&v=4" width=80px style="text-align:right"><h1>The Internet of Production Alliance </h1>

    ## Data collection program for the [OKW, Map of facilities](https://www.internetofproduction.org/open-know-where)
    """
)

# %%
mo.md("""\n    "https://www.google.com/maps/d/u/0/viewer?mid=10q6m1yyAUzFn2zqDcRwq-qInUmvoVz4q&ll=36.477161278633425%2C-119.52755771944813&z=7"Author: Antonio de Jesus Anaya Hernandez, DevOps eng. for the IoPA.\n\n    Author: The internet of Production Alliance, 2023.\n\n    Data was collected by "Makerspaces, MAKE makezine, and its partners", URL location: https://makerspaces.make.co/\n\n    Data source license:\n\n    The Open Know Where (OKW) Initiative is part of the Internet of Production Alliance and its members.\n\n    License: CC BY SA\n\n    ![CC BY SA](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)\n\n    Description: Python code for downloading, parsing, filtering, sorting data, exporting the RAW makery locations, and the processed IOPA data as CSV.\n""")

# %%
def req_data(url, head):
    response = requests.get(url, headers=head)
    print(response.status_code)
    if response.status_code == 200:
        return response
    else:
        print('Error response: Check URL or internet avalability, and Try again.')
        print(url)

# %%
url = 'https://makerspace.com/wp-json/makerspaces/v1/spacedata/5/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'}
data = req_data(url, headers)
print(type(data))

# %%
input_ = pd.read_json(io.StringIO(data.text))

# %%
input_normalized = pd.json_normalize(input_.Makerspaces)

# %%
input_.reset_index(drop=True, inplace=True)

# %%
output = pd.DataFrame(input_normalized, columns=['id', 'url', 'name', 'city', 'state', 'country', 'zip', 'latitude', 'longitude'])

# %%
input_normalized.to_csv('data/raw_source_11_' + now.strftime('%Y_%m_%d_%H%M') + '.csv')

# %%
input_normalized.columns.tolist()

# %%
output.to_csv('data/source_11_' + now.strftime('%Y_%m_%d_%H%M') + '.csv')

# %%
print('OKW entries: {r[0]}, columns = {r[1]}'.format(r=output.shape))
