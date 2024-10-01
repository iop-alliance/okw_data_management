import marimo

__generated_with = "0.8.20"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        <img src="https://avatars.githubusercontent.com/u/61060916?s=200&v=4" width=80px style="text-align:right"><h1>The Internet of Production Alliance </h1>

        ## Data collection program for the [OKW, Map of facilities](https://www.internetofproduction.org/open-know-where)
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
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
    return


@app.cell
def __():
    #!pip install fastkml lxml
    return


@app.cell
def __():
    from fastkml import kml
    return (kml,)


@app.cell
def __():
    import requests
    import pandas as pd
    return pd, requests


@app.cell
def __():
    from datetime import datetime
    now = datetime.now()
    return datetime, now


@app.cell
def __(requests):
    def req_data(url):

        response = requests.get(url)

        print(response.status_code)

        if response.status_code == 200:
            return response
        else:
            print("Error response: Check URL or internet avalability, and Try again.")
            print(url)
    return (req_data,)


@app.cell
def __():
    kml_url = "http://www.google.com/maps/d/kml?forcekml=1&mid=1wKXDd1rOs4ls1EiZswQr-upFq7o"
    return (kml_url,)


@app.cell
def __(kml_url, req_data):
    g_map = req_data(kml_url).content
    return (g_map,)


@app.cell
def __(g_map, kml):
    kml_file = kml.KML()
    kml_file.from_string(g_map)
    return (kml_file,)


@app.cell
def __(kml_file):
    features = list(kml_file.features())
    return (features,)


@app.cell
def __(features):
    table = []

    for folder in list(features[0].features()):
        f = folder.features()
        for record in f:
            table.append((record.name, record.geometry.x, record.geometry.y, folder.name))
    return f, folder, record, table


@app.cell
def __(pd, table):
    output = pd.DataFrame(table, columns=['name', 'latitude', 'longitude', 'type'])
    return (output,)


@app.cell
def __(now, output):
    output.to_csv('data/source_04_' + now.strftime("%Y_%m_%d_%H%M") + '.csv')
    return


@app.cell
def __(output):
    print("OKW entries: {r[0]}, columns = {r[1]}".format(r=output.shape))
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
