'''
Author: Antonio de Jesus Anaya Hernandez, DevOps eng. for the IoPA.

Author: The internet of Production Alliance, 2023.

Data was collected by "sridhar[at]upbeatlabs.com, and its partners", URL location: "https://www.google.com/maps/d/u/0/viewer?mid=10q6m1yyAUzFn2zqDcRwq-qInUmvoVz4q&ll=37.844558%2C-122.27696200000003&z=8"

Data source license:

The Open Know Where (OKW) Initiative is part of the Internet of Production Alliance and its members.

License: CC BY SA

![CC BY SA](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)

Description: Python code for downloading, parsing, filtering, sorting data, exporting the RAW makery locations, and the processed IOPA data as CSV.
'''

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

callback = (
    "function (row) {"
    "    var marker = L.marker(new L.LatLng(row[0], row[1]));"
    "    var popup = L.popup({maxWidth: '300'});"
    "    const name = {text: row[2]};"
#    "    const lat = {text: row[0]};"
#    "    const long = {text: row[1]};"
#    "    const url = {text: row[3]};"
#    "    const email = {text: row[4]};"
#    "    if (email.text) {"
 #   "        var s = email.text;"
#    "        var e = s.split('').reverse().join('');"
#    "        var mytext = $(`<div id='mytext' class='name' style='width: 100.0%; height: 100.0%;'>"
#    "                       <strong> ${name.text} </strong> <br>"
#    "                       <a href=${url.text} target='_blank'> Website </a> <br>"
#    "                       </div>`)[0];"
#    "    } else {"
    "        var mytext = $(`<div id='mytext' class='name' style='width: 100.0%; height: 100.0%;'>"
    "                       <strong> ${name.text} </strong> <br>"
#    "                       <strong> ${lat.text} </strong> <br>"
#    "                       <strong> ${long.text} </strong> <br>"
#    "                       <a href=${url.text} target='_blank'> Website </a>"
    "                       </div>`)[0];"
#    "    }"
    "    popup.setContent(mytext);"
    "    marker.bindPopup(popup);"
    "    return marker;"
    "};"
)
    
# output_map = output_map_w[output_map_w['country_code'].isin(['FR','EG'])]

import folium
import numpy as np
from folium.plugins import FastMarkerCluster, FloatImage


class Plot():
    
    def __init__(self, dataframe):

        self.tiles_url = 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}'
        self.tiles_attribution = 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
        self.data = dataframe
        
        self.prep_data()
        self.set_map()
        self.add_points()
        # self.render()
        
    def prep_data(self):
        self.output_map = self.data.dropna(subset=['latitude', 'longitude'])
        # self.output_map.reset_index(drop=True, inplace=True)
        self.zip_data = [(row['latitude'], row['longitude'], row['name'] 
                     # row['url'], 
                     # row['email']
                     ) 
                    for index, row in self.output_map.iterrows()]
        
    def set_map(self):
        
        # Check for NaN values in latitude and longitude before creating the map
        if not np.isnan(self.output_map['latitude']).any() and not np.isnan(self.output_map['longitude']).any():
            self.m = folium.Map(
                location=[self.output_map['latitude'].mean(), self.output_map['longitude'].mean()],
                zoom_start=7,
                tiles=self.tiles_url,
                attr=self.tiles_attribution,
                max_zoom=16,
                # worldCopyJump= False,
                zoomControl= False,
                prefer_canvas=True
            )
    
        else:
            print("Location values cannot contain NaNs.")
 
    def add_points(self):
        FastMarkerCluster(data=self.zip_data, icon_create_function=icon_cluster, callback=callback, options={'singleMarkerMode': True}).add_to(self.m)


    def render(self):
        FloatImage("https://github.com/iop-alliance/data_reports/blob/main/assets/img/iopa_logo_okw_sm.png?raw=true", bottom=5, left=5).add_to(self.m)
        return self.m.get_root().render()


#Fullscreen(
#    position="topright",
#    force_separate_button=True,
#).add_to(m)

# print(output["country_code"].value_counts().nlargest(10))

# import pycountry_convert as pcountry

# def get_continent(country_alpha2):
#     continent_code = pcountry.country_alpha2_to_continent_code(country_alpha2)
#     continent_name = pcountry.convert_continent_code_to_continent_name(continent_code)
#     return continent_name

# output_db['continent'] = output_db['country_code'].apply(get_continent)
# grouped_db = output_db.groupby(['continent', 'country_code']).size().reset_index(name='Location Count')
# top_three_db = (
#     grouped_db
#     .sort_values(['continent', 'Location Count'], ascending=[True, False])
#     .groupby('continent')
#     .head(3)
# )

# top_three_db

