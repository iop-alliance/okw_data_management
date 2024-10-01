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
    mo.md("""\n    Author: Antonio de Jesus Anaya Hernandez, DevOps eng. for the IoPA.\n\n    Author: The internet of Production Alliance, 2023.\n\n    Data was collected by "Makery, gogocarto, and its partners", URL location: https://makery.gogocarto.fr/api\n\n    Data source license: ODBL 1.0, Open Data Commons Open Database License\n\n    The Open Know Where (OKW) Initiative is part of the Internet of Production Alliance and its members.\n\n    License: CC BY SA\n\n    ![CC BY SA](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)\n\n    Description: Python code for downloading, parsing, filtering, sorting data, exporting the RAW makery locations, and the processed IOPA data as CSV.\n""")
    return


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
def __(req_data):
    url = 'https://makery.gogocarto.fr/api/elements.json'
    data = req_data(url).json()
    print(type(data))
    return data, url


@app.cell
def __(data, pd):
    data_ = pd.DataFrame(data)
    return (data_,)


@app.cell
def __(data_, pd):
    input_d = pd.DataFrame(data_.data)
    print(input_d.shape)
    from pandas import json_normalize
    input_ = pd.json_normalize(input_d['data'])
    return input_, input_d, json_normalize


@app.cell
def __(input_):
    input_.reset_index(drop=True, inplace=True)
    return


@app.cell
def __(input_, now):
    input_.to_csv('data/raw_source_10_' + now.strftime('%Y_%m_%d_%H%M') + '.csv')
    return


@app.cell
def __(input_):
    input_.columns.tolist()
    return


@app.cell
def __(input_):
    transform = input_.rename(columns={'id': 'makery_id', 'status': 'makery_status', 'site_web': 'url', 'geo.latitude': 'latitude', 'geo.longitude': 'longitude'})
    return (transform,)


@app.cell
def __(transform):
    transform['makery_url'] = transform.apply(lambda row: 'https://makery.gogocarto.fr/map#/fiche/{name}/{id}/'.format(name=str(row['name']).replace(' ', '-'), id=row['makery_id']), axis=1)
    return


@app.cell
def __(transform):
    active_spaces = transform[transform['makery_status'] != 'closed']
    return (active_spaces,)


@app.cell
def __(active_spaces):
    real_spaces = active_spaces[active_spaces['makery_status'] != 'planned']
    return (real_spaces,)


@app.cell
def __(real_spaces):
    real_spaces['address_composed'] = real_spaces['address.streetNumber'].astype(str) + ', ' + real_spaces['address.streetAddress'].astype(str) + ', ' + real_spaces['address.addressLocality'].astype(str) + ', ' + real_spaces['address.postalCode'].astype(str) + ', ' + real_spaces['address.addressCountry'].astype(str)
    return


@app.cell
def __():
    drops = ['sourceKey', 'categoriesFull', 'article_makery', 'fullAddress', 'mode_gestion', 'subscriberEmails', 'address.customFormatedAddress', 'description_courte', 'surface', 'telephone', 'images', 'openHours.Mo', 'openHours.Tu', 'openHours.We', 'openHours.Th', 'openHours.Fr', 'address.streetNumber', 'address.streetAddress', 'address.addressLocality', 'address.postalCode', 'address.addressCountry', 'affiliation', 'description', 'openHours.Sa', 'openHours.Su', 'makery_status','createdAt', 'updatedAt','makery_url','categories','makery_id']
    return (drops,)


@app.cell
def __(drops, real_spaces):
    output = real_spaces.drop(columns=drops)
    return (output,)


@app.cell
def __(output):
    output.columns.tolist()
    return


@app.cell
def __(now, output):
    output.to_csv('data/source_10_' + now.strftime('%Y_%m_%d_%H%M') + '.csv')
    return


@app.cell
def __(output):
    print('OKW entries: {r[0]}, columns = {r[1]}'.format(r=output.shape))
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
