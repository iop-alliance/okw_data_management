import marimo

__generated_with = "0.8.20"
app = marimo.App(width="medium")


@app.cell
def __():
    import requests
    import pandas as pd
    from datetime import datetime
    import marimo as mo

    now = datetime.now()
    creation_date = "2024_07_16_1423"
    update_date = now.strftime("%Y_%m_%d_%H%M")
    return creation_date, datetime, mo, now, pd, requests, update_date


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
def __(pd, req_data):
    url = "https://api.fablabs.io/0/labs.json"
    data = req_data(url).json()
    input_ = pd.DataFrame(data)
    input_.reset_index(drop=True, inplace=True)
    return data, input_, url


@app.cell
def __(input_, update_date):
    input_.to_csv('data/raw_source_01_' + update_date + '.csv')
    return


@app.cell
def __(input_):
    input_.columns.tolist()
    transform = input_.rename(columns={'id': 'org_id'})
    transform['url'] = 'https://www.fablabs.io/labs/' + transform.slug
    transform = transform[transform['activity_status'] != 'closed']
    transform = transform[transform['activity_status'] != 'planned']
    # transform['address'] = transform.address_1.astype(str) + ', ' + transform.address_2 + ', ' + transform.county
    output = transform.drop(columns=['activity_status','kind_name','slug', 'address_2', 'address_notes', 'parent_id', 'blurb', 'avatar_url', 'header_url', 'capabilities', 'links', 'description', 'phone'])
    output_db = output.fillna('null')
    return output, output_db, transform


@app.cell
def __(output_db):
    output_db.columns.tolist()
    return


@app.cell
def __(output_db, update_date):
    output_db.to_csv('data/iopa_source_01_' + update_date + '.csv')
    return


@app.cell
def __(creation_date, output, update_date):
    DatabaseSourceMetadata = {
            'source_id': "01", #key
            'name': "Fablabs.io FabLab Network", #unique #not_null
            'description': "World wide Fablabs within the fablab.io platform.",
            'source_type': "JSON",
            'source_url': "https://api.fablabs.io/0/labs.json",
            'license_type': "Limited",
            'data_policy_url': "https://fablabs.io/privacy-policy", #not_null
            'version': "0.1",
            'creation_date': creation_date, #not_null
            'update_date': str(update_date), #not_null
            'keywords': "Fablab, Network, Capibilities, Machines, World",
            'publisher': "Fab Foundation", #not_null
            'publisher_url': "https://fabfoundation.org/", #not_null
            'contributor': "Fab Foundation", #not_null
            'language': "en", #not_null #language_id
            'shape': {'entries': {str(output.shape[0])}, 'columns': {str(output.shape[1])}} #not_null
        }
    return (DatabaseSourceMetadata,)


@app.cell
def __():
    ManufacturingFacility = {
        "facility_id": None,      # int: Unique identifier for the facility
        # "resource_id": None,      # int: Reference to the distributed resource
        "name": "",               # string: Name of the facility
        "description": "",        # string: Description of the facility
        "type": "",               # string: Type of the facility
        # "capacity": None,         # int: Capacity of the facility
        # "capabilities": "",       # string: Capabilities of the facility
        "inventory": "None",
        # "source_id": None         # int: Reference to the metadata of the source
        "version": "0.1",
    }
    return (ManufacturingFacility,)


@app.cell
def __(DatabaseSourceMetadata):
    print(DatabaseSourceMetadata)
    return


@app.cell
def __():
    from data_models import ParserSchema
    return (ParserSchema,)


@app.cell
def __(ParserSchema, output):
    _schema = ParserSchema()

    location_json_mapping = []
    for index, row in output.iterrows():
        data_dict = {
        'latitude': row['latitude'],
        'longitude': row['longitude'],
        'zip_code': row['postal_code'],
        'extended': row['address_1'],
        'country': row['country_code'],
        'state_region': row['county'],
        'city_town': row['city'],
        'org_id': row['org_id'],
        'description': 'fablab',
        'name': row['name'],
        'url': row['url']
    }
        location_json_mapping.append(_schema.dumping(data_dict))
    return data_dict, index, location_json_mapping, row


@app.cell
def __(location_json_mapping):
    location_json_mapping
    return


@app.cell
def __(location_json_mapping):
    geocode_list = [item['geocoding'] for item in location_json_mapping if item['geocoding'] is not None]
    return (geocode_list,)


@app.cell
def __(location_json_mapping):
    region_list = [item['region'] for item in location_json_mapping if item['region'] is not None]
    return (region_list,)


@app.cell
def __(pd, region_list):
    df_region = pd.DataFrame(region_list).drop_duplicates(subset=['country', 'state_region', 'city_town'])
    return (df_region,)


@app.cell
def __(df_region):
    df_region
    return


@app.cell
def __(df_region):
    df_region_unique = df_region.drop_duplicates(subset=['country', 'state_region', 'city_town'], keep='first')
    return (df_region_unique,)


@app.cell
def __(df_region_unique):
    df_region_unique.to_json('iopa_okw_regions.json', orient="records")
    return


@app.cell
def __():
    return


@app.cell
def __(df_region_unique):
    df_region_unique.to_csv('iopa_okw_regions.csv')
    return


@app.cell
def __(geocode_list):
    geocode_list
    return


@app.cell
def __(region_list):
    region_list
    return


@app.cell
def __(region_list):
    region_list
    return


@app.cell
def __(location_json_mapping):
    import json

    #jsonfile = json.loads(location_json_mapping)
    with open('data/preliminary_iop_okw_fac_source_01.json', 'w') as base:
        json.dump(location_json_mapping, base, indent=4)
        base.close()
    return base, json


@app.cell
def __():
    return


@app.cell
def __(mo, output):
    mo.ui.table(output)
    return


@app.cell
def __(output):
    import folium
    import numpy as np
    from folium.plugins import FastMarkerCluster, Fullscreen, FloatImage

    tiles_url = 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}'
    tiles_attribution = 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'

    output_map_w = output.dropna(subset=['latitude', 'longitude'])

    # Filtered for EG FR map
    output_map = output_map_w[output_map_w['country_code'].isin(['FR','EG'])]

    # Check for NaN values in latitude and longitude before creating the map
    if not np.isnan(output_map['latitude']).any() and not np.isnan(output_map['longitude']).any():
        m = folium.Map(
            location=[output_map['latitude'].mean(), output_map['longitude'].mean()],
            zoom_start=4,
            tiles=tiles_url,
            attr=tiles_attribution,
            max_zoom=16,
            # worldCopyJump= False,
            zoomControl= False,
            prefer_canvas=True
        )

    else:
        print("Location values cannot contain NaNs.")
    return (
        FastMarkerCluster,
        FloatImage,
        Fullscreen,
        folium,
        m,
        np,
        output_map,
        output_map_w,
        tiles_attribution,
        tiles_url,
    )


@app.cell
def __():
    icon_cluster = '''
        function (cluster) {

        var childCount = cluster.getChildCount();

        var size, opacity, text, color, colors;

        colors = ['#1E90FF', '#69B4FF', '#B469FF', '#FF69FF', '#FF69B4', '#FF6F69'];

        text = '<span style = "font-family: "Fira Mono", monospace !important; font-weight: 500; font-style: normal;">' + childCount + '</span>';

        opacity = 0.8;

        if (childCount == 1) {
            size = 20;
            text = '';
            color = colors[0];
    } else if (childCount >= 2 && childCount <= 5) {
        size = 20;
        color = colors[1];
    } else if (childCount >= 5 && childCount <= 20) {
        size = 25;
        color = colors[2];
    } else if (childCount >= 20 && childCount <= 100) {
        size = 30;
        color = colors[3];
    } else if (childCount >= 100 && childCount <= 500) {
        size = 35;
        color = colors[4];
    } else if (childCount > 500) {
        size = 40;
        color = colors[5];
    }
        return new L.DivIcon({
            html: text + '<div style="background-color:' + color + '; height:' + size + 'px; width:' + size + 'px; opacity:' + opacity + '; border-radius: 10%;"></div>',
            className: '',
            iconSize: new L.Point(size, size)
        });
    }
    '''
    # clip-path: inset(1% 1% round 40% 1% 1% 1%);
    return (icon_cluster,)


@app.cell
def __():
    callback = (
        "function (row) {"
        "    var marker = L.marker(new L.LatLng(row[0], row[1]));"
        "    var popup = L.popup({maxWidth: '300'});"
        "    const name = {text: row[2]};"
        "    const url = {text: row[3]};"
        "    const email = {text: row[4]};"
        "    if (email.text) {"
        "        var s = email.text;"
        "        var e = s.split('').reverse().join('');"
        "        var mytext = $(`<div id='mytext' class='name' style='width: 100.0%; height: 100.0%;'>"
        "                       <strong> ${name.text} </strong> <br>"
        "                       <a href=${url.text} target='_blank'> Website </a> <br>"
        "                       </div>`)[0];"
        "    } else {"
        "        var mytext = $(`<div id='mytext' class='name' style='width: 100.0%; height: 100.0%;'>"
        "                       <strong> ${name.text} </strong> <br>"
        "                       <a href=${url.text} target='_blank'> Website </a>"
        "                       </div>`)[0];"
        "    }"
        "    popup.setContent(mytext);"
        "    marker.bindPopup(popup);"
        "    return marker;"
        "};"
    )
    return (callback,)


@app.cell
def __(
    FastMarkerCluster,
    FloatImage,
    callback,
    icon_cluster,
    m,
    output_map,
):
    zip_data = [(row['latitude'], row['longitude'], row['name'], 
                 row['url'], 
                 row['email']) 
                for index, row in output_map.iterrows()]

    marker_cluster = FastMarkerCluster(data=zip_data, 
                                       icon_create_function=icon_cluster,
                                       callback=callback,
                                       options={'singleMarkerMode': True}).add_to(m)

    #Fullscreen(
    #    position="topright",
    #    force_separate_button=True,
    #).add_to(m)

    FloatImage("https://github.com/iop-alliance/data_reports/blob/main/assets/img/iopa_logo_okw_sm.png?raw=true", 
                    bottom=5, 
                    left=5).add_to(m)

    m.save('output.html')
    return marker_cluster, zip_data


@app.cell
def __(m):
    m
    return


@app.cell
def __(m):
    m.save('mvp_10.html')
    return


@app.cell
def __(output):
    print(output["country_code"].value_counts().nlargest(10))
    return


@app.cell
def __(output_db):
    import pycountry_convert as pcountry

    def get_continent(country_alpha2):
        continent_code = pcountry.country_alpha2_to_continent_code(country_alpha2)
        continent_name = pcountry.convert_continent_code_to_continent_name(continent_code)
        return continent_name

    output_db['continent'] = output_db['country_code'].apply(get_continent)
    grouped_db = output_db.groupby(['continent', 'country_code']).size().reset_index(name='Location Count')
    top_three_db = (
        grouped_db
        .sort_values(['continent', 'Location Count'], ascending=[True, False])
        .groupby('continent')
        .head(3)
    )
    return get_continent, grouped_db, pcountry, top_three_db


@app.cell
def __(top_three_db):
    top_three_db
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
