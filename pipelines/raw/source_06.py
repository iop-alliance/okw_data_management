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
    mo.md("""\n    Author: Antonio de Jesus Anaya Hernandez, DevOps eng. for the IoPA.\n\n    Author: The internet of Production Alliance, 2023.\n\n    Data was collected by "Make Works, FabLab Barcelona and its partners", URL location: https://make.works/companies\n\n    The Open Know Where (OKW) Initiative is part of the Internet of Production Alliance and its members.\n\n    License: CC BY SA\n\n    ![CC BY SA](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)\n\n    Description: Python code for downloading, parsing, filtering, sorting data, exporting the RAW FabLabs, and the processed IOPA data as CSV.\n""")
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
            print(response.status_code)
            return response
        else:
            print(response.status_code)
            print('Error response: Check URL or internet avalability, and Try again.')
            print(url)
            return False
    return (req_data,)


@app.cell
def __(requests):
    url = 'https://make.works/companies?page={n}&format=json'
    data = []
    x = 0
    while True:
        response = requests.get(url.format(n=x))
        json_data = response.json()
        if not json_data:
            break
        data += json_data
        x += 1
    print('Pages: {p}'.format(p=x))
    print('Entries: {e}'.format(e=len(data)))
    return data, json_data, response, url, x


@app.cell
def __(data, pd):
    input_ = pd.DataFrame(data)
    return (input_,)


@app.cell
def __(input_):
    input_.reset_index(drop=True, inplace=True)
    return


@app.cell
def __(input_, now):
    input_.to_csv('data/source_06_' + now.strftime('%Y_%m_%d_%H%M') + '.csv')
    return


@app.cell
def __(input_):
    input_.columns.tolist()
    return


@app.cell
def __(input_):
    transform = input_.rename(columns={'id': 'makeworks_id', 'url': 'makeworks_url', 'lat': 'latitude', 'lng': 'longitude'})
    return (transform,)


@app.cell
def __(transform):
    transform_2 = transform[transform['soft_delete'] != True]
    return (transform_2,)


@app.cell
def __(transform_2):
    output = transform_2.drop(columns=['medium_run', 'minimum_order', 'short_run', 'turnaround_time', 'twitter', 'm_id', 'region_ids', 'background', 'intro', 'contact_name', 'contact_phone', 'contact_jobtitle', 'youtube', 'year_founded', 'film_ready', 'title', 'top_image', 'flickr', 'facebook', 'instagram', 'number_of_staff', 'file_types', 'image_bucket', 'photo1', 'photo2', 'photo3', 'photo4', 'photo5', 'photo6', 'photo7', 'photo8', 'photo9', 'pinterest', 'portrait', 'sample_production', 'soft_delete', 'large_run', 'linkedin', 'video_link'])
    return (output,)


@app.cell
def __(now, output):
    output.to_csv('data/source_06_' + now.strftime('%Y_%m_%d_%H%M') + '.csv')
    return


@app.cell
def __(output):
    output.columns.tolist()
    return


@app.cell
def __(output):
    print('OKW entries: {r[0]}, columns = {r[1]}'.format(r=output.shape))
    return


if __name__ == "__main__":
    app.run()
