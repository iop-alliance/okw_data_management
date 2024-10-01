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
        r"""
        <img src="https://avatars.githubusercontent.com/u/61060916?s=200&v=4" width=80px style="text-align:right"><h1>The Internet of Production Alliance </h1>

        ## Data collection program for the [OKW, Map of facilities](https://www.internetofproduction.org/open-know-where)
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        Author: Antonio de Jesus Anaya Hernandez, DevOps eng. for the IoPA.

        Author: The internet of Production Alliance, 2023.

        Data was collected by "Hackerspaces.org, and its partners", URL location: https://hackerspaces.org

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
    # This line installs the required libraries for running the script, uncomment the line:
    # !pip install -r requirements.txt
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
def __(req_data):
    url = "https://wiki.hackerspaces.org/w/index.php?title=Special%3AAsk&_action=submit&q=%5B%5BCategory%3AHackerspace%5D%5D+%5B%5BHackerspace+status%3A%3Aactive%5D%5D&po=%3FCountry%0D%0A%3FState%0D%0A%3FCity%0D%0A%3FWebsite%0D%0A%3FLast+Updated%0D%0A%3FEmail&eq=yes&p%5Bformat%5D=csv&p%5Blimit%5D=5000&p%5Boffset%5D=400&p%5Blink%5D=all&p%5Bheaders%5D=show&p%5Bmainlabel%5D=hackerspace&p%5Bintro%5D=&p%5Boutro%5D=&p%5Bsearchlabel%5D=...+further+results&p%5Bdefault%5D=&p%5Bsep%5D=%2C&p%5Bvaluesep%5D=%2C&p%5Bfilename%5D=result.csv&sort_num%5B%5D=Last+Updated&order_num%5B%5D=desc&sort_num%5B%5D=&order_num%5B%5D=asc&eq=yes&ask=on"
    data = req_data(url)
    print(type(data))
    return data, url


@app.cell
def __(data, io, pd):
    input_ = pd.read_csv(io.StringIO(data.text))
    return (input_,)


@app.cell
def __(input_):
    input_.reset_index(drop=True, inplace=True)
    return


@app.cell
def __(input_, now):
    input_.to_csv('data/raw_source_09_' + now.strftime("%Y_%m_%d_%H%M") + '.csv')
    return


@app.cell
def __(input_):
    input_.columns.tolist()
    return


@app.cell
def __(input_):
    output = input_.drop(columns=[])
    return (output,)


@app.cell
def __(now, output):
    output.to_csv('data/source_09_' + now.strftime("%Y_%m_%d_%H%M") + '.csv')
    return


@app.cell
def __(input_):
    print("OKW entries: {r[0]}, columns = {r[1]}".format(r=input_.shape))
    return


if __name__ == "__main__":
    app.run()