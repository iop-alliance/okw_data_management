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

        Data was collected by "Makertour, and its partners", URL location: https://www.makertour.fr/workshops/

        The Open Know Where (OKW) Initiative is part of the Internet of Production Alliance and its members.

        License: CC BY SA

        ![CC BY SA](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)

        Description: Python code for downloading, parsing, filtering, sorting data, exporting the RAW FabLabs, and the processed IOPA data as CSV.
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
    from bs4 import BeautifulSoup
    from datetime import datetime
    return BeautifulSoup, datetime, json, pd, requests


@app.cell
def __(datetime, requests):
    date = datetime.now().strftime("%Y_%m_%d_%H%M")
    url = "https://www.makertour.fr/map"
    org_name = "Maker Tour"
    response = requests.get(url)
    print(response)
    return date, org_name, response, url


@app.cell
def __(BeautifulSoup, json, response):
    html_bytes = response.content
    html_string = html_bytes.decode('utf-8')

    soup = BeautifulSoup(html_string, 'html.parser')
    map_content = soup.find('div', id='map')
    markers_string = map_content.get('data-markers')

    markers_json = json.loads(markers_string)
    return (
        html_bytes,
        html_string,
        map_content,
        markers_json,
        markers_string,
        soup,
    )


@app.cell
def __(BeautifulSoup):
    def extract_info(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        title = soup.find('h2', class_='workshop-title').text.strip()
        location = soup.find('span', class_='city-country').text.strip()
        tags = [tag.text.strip() for tag in soup.find_all('span', class_='tag primary')]
        href = soup.find('a', class_='card-link')['href'].strip()

        return [title] + location.split(", ") + [tags, "https://www.makertour.fr" + href]
    return (extract_info,)


@app.cell
def __(extract_info, markers_json):
    data = []
    for record in markers_json:

        data.append(extract_info(record['content']) + [record['lat'], record['lng']])

    columns = ['name', 'city', 'country', 'tags', 'url', 'latitude', 'longitude']
    return columns, data, record


@app.cell
def __(columns, data, pd):
    input_ = pd.DataFrame(data, columns=columns)
    return (input_,)


@app.cell
def __(input_):
    input_.reset_index(drop=True, inplace=True)
    return


@app.cell
def __(date, org_name):
    file_name = "raw_" + org_name.replace(" ", "_").lower() + date
    return (file_name,)


@app.cell
def __(input_):
    input_.to_csv('data/' + 'source_05' + '.csv')
    return


@app.cell
def __(input_):
    input_.columns.tolist()
    return


@app.cell
def __(input_):
    print("OKW entries: {r[0]}, columns = {r[1]}".format(r=input_.shape))
    return


@app.cell
def __():
    #notes: notebooks will change to only collect raw data, and generate DB metadata on preparation for data aggregation process. Cleaning and sorting will be arreanged on following notebooks fro data validation and cleansing.
    return


@app.cell
def __():
    """
    meta.json
    Entries, column_names, creation_date
    """
    return


@app.cell
def __(date, file_name, input_, json, org_name, url):
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
    return metadata, metadata_json, outfile


if __name__ == "__main__":
    app.run()
