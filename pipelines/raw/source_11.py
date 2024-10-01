import marimo

__generated_with = "0.8.20"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __(mo):
    mo.md(
        """
        <img src="https://avatars.githubusercontent.com/u/61060916?s=200&v=4" width=80px style="text-align:right"><h1>The Internet of Production Alliance </h1>

        ## Data collection program for the [OKW, Map of facilities](https://www.internetofproduction.org/open-know-where)
        """
    )
    return


@app.cell
def __(mo):
    mo.md("""\n    "https://www.google.com/maps/d/u/0/viewer?mid=10q6m1yyAUzFn2zqDcRwq-qInUmvoVz4q&ll=36.477161278633425%2C-119.52755771944813&z=7"Author: Antonio de Jesus Anaya Hernandez, DevOps eng. for the IoPA.\n\n    Author: The internet of Production Alliance, 2023.\n\n    Data was collected by "Makerspaces, MAKE makezine, and its partners", URL location: https://makerspaces.make.co/\n\n    Data source license:\n\n    The Open Know Where (OKW) Initiative is part of the Internet of Production Alliance and its members.\n\n    License: CC BY SA\n\n    ![CC BY SA](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)\n\n    Description: Python code for downloading, parsing, filtering, sorting data, exporting the RAW makery locations, and the processed IOPA data as CSV.\n""")
    return


@app.cell
def __():
    import requests
    import pandas as pd
    import json
    import io
    return io, json, pd, requests


@app.cell
def __():
    from datetime import datetime
    now = datetime.now()
    return datetime, now


@app.cell
def __(requests):
    def req_data(url, head):
        response = requests.get(url, headers=head)
        print(response.status_code)
        if response.status_code == 200:
            return response
        else:
            print('Error response: Check URL or internet avalability, and Try again.')
            print(url)
    return (req_data,)


@app.cell
def __(req_data):
    url = 'https://makerspace.com/wp-json/makerspaces/v1/spacedata/5/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'}
    data = req_data(url, headers)
    print(type(data))
    return data, headers, url


@app.cell
def __(data, io, pd):
    input_ = pd.read_json(io.StringIO(data.text))
    return (input_,)


@app.cell
def __(input_):
    input_.reset_index(drop=True, inplace=True)
    return


@app.cell
def __():
    #input_.Makerspaces
    return


@app.cell
def __(input_, pd):
    input_normalized = pd.json_normalize(input_.Makerspaces)
    return (input_normalized,)


@app.cell
def __(input_normalized, now):
    input_normalized.to_csv('data/raw_source_11_' + now.strftime('%Y_%m_%d_%H%M') + '.csv')
    return


@app.cell
def __(input_normalized):
    input_normalized.columns.tolist()
    return


@app.cell
def __(input_normalized, pd):
    output = pd.DataFrame(input_normalized, columns=['id', 'url', 'name', 'city', 'state', 'country', 'zip', 'latitude', 'longitude'])
    return (output,)


@app.cell
def __(now, output):
    output.to_csv('data/source_11_' + now.strftime('%Y_%m_%d_%H%M') + '.csv')
    return


@app.cell
def __(output):
    print('OKW entries: {r[0]}, columns = {r[1]}'.format(r=output.shape))
    return


if __name__ == "__main__":
    app.run()
