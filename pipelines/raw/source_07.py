import marimo

__generated_with = "0.8.20"
app = marimo.App()


@app.cell(hide_code=True)
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

        Data was collected by "Offene Werkstaetten, and its partners", URL location: https://www.offene-werkstaetten.org/de/werkstatt-suche

        The Open Know Where (OKW) Initiative is part of the Internet of Production Alliance and its members.

        License: CC BY SA

        ![CC BY SA](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)

        Description: Python code for downloading, parsing, filtering, sorting data, exporting the RAW FabLabs, and the processed IOPA data as CSV.
        """
    )
    return


@app.cell
def __():
    import requests, json, re, time
    import pandas as pd
    from datetime import datetime
    now = datetime.now()
    from bs4 import BeautifulSoup as soup
    from __functions__ import req_data
    return datetime, json, now, pd, re, req_data, requests, soup, time


@app.cell
def __():
    url = "https://www.offene-werkstaetten.org/widgets/search?colorA=74ac61&colorB=0489B1&customMarkerSrc=https://cdn0.iconfinder.com/data/icons/map-location-solid-style/91/Map_-_Location_Solid_Style_06-48.png&customClusterSrc=https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-ios7-circle-filled-48.png"
    return (url,)


@app.cell
def __(req_data, soup, url):
    data = [x.text for x in soup(req_data(url).text, 'html.parser').find_all('script') if 'vow.Map' in x.text][-1]
    return (data,)


@app.cell
def __(data, json, re):
    data_f = '[{"' + re.findall(r'\[{"(.*?)"\}\]\,', data)[0] + '"}]'
    data_json = json.loads(data_f)
    return data_f, data_json


@app.cell
def __(data_json, pd):
    input_ = pd.DataFrame(data_json)
    return (input_,)


@app.cell
def __(input_):
    input_.reset_index(drop=True, inplace=True)
    return


@app.cell
def __(input_, now):
    input_.to_csv('data/raw_source_07_' + now.strftime("%Y_%m_%d_%H%M") + '.csv')
    return


@app.cell
def __(input_):
    input_.columns.tolist()
    return


@app.cell
def __(input_):
    transform = input_.rename(columns={'uid': 'offene_id', 'lat': 'latitude', 'lng': 'longitude', 'zip':'postal_code'})
    return (transform,)


@app.cell
def __(transform):
    transform['offene_url'] = 'https://www.offene-werkstaetten.org/werkstatt/' + transform.url
    return


@app.cell
def __(transform):
    transform['address'] = transform.street.astype(str) + ', ' + transform.street_nr + ', ' + transform.aai
    return


@app.cell
def __(re):
    def decrypt(js):
        if js != None:

            a_cut = js[17:104].replace('\\', '')
            c_cut = js[123:181].replace('\\', '')

            try: 
                a = re.search(re.compile(r'var a="(.*?)";'), a_cut).group(1)
                c = re.search(re.compile(r'var c="(.*?)";'), c_cut).group(1)
            except AttributeError:
                return None

            b = ''.join(sorted(a))
            d = ''

            for e in c:
                d += b[a.index(e)]

            return d
        else:
            print("No Js received")
            return None
    return (decrypt,)


@app.cell
def __(decrypt, re, req_data, soup, transform):
    transform['contact_email']  = transform.offene_url.apply(lambda x: decrypt(soup(req_data(x, 2).content, 'html.parser').find('span', text=re.compile(r'javascript protected email address')).find_next_sibling('script').text))
    return


@app.cell
def __(transform):
    output = transform.drop(columns=['img', 'street', 'street_nr', 'aai', 'cats', 'url', 'icm', 'web'])
    return (output,)


@app.cell
def __(now, output):
    output.to_csv('data/source_07_' + now.strftime("%Y_%m_%d_%H%M") + '.csv')
    return


@app.cell
def __(output):
    output.columns.tolist()
    return


@app.cell
def __(output):
    print("OKW entries: {r[0]}, columns = {r[1]}".format(r=output.shape))
    return


if __name__ == "__main__":
    app.run()
