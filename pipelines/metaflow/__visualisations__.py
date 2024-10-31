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


import folium
import numpy as np
from folium.plugins import FastMarkerCluster, FloatImage
from itables import to_html_datatable



def load_js_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()



class Plot():
    
    def __init__(self, dataframe, max_cluster_rad=40):
        self.icon_cluster = load_js_file('pipelines/metaflow/assets/cluster_icon.js')
        self.callback = load_js_file('pipelines/metaflow/assets/cluster_mod.js')
        self.tiles_url = 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}'
        self.tiles_attribution = 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
        self.data = dataframe
        self.max_rad = max_cluster_rad
        self.prep_data()
        self.set_map()
        self.add_points()

        
        
    def prep_data(self):
        self.output_map = self.data.dropna(subset=['latitude', 'longitude'])
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
                # zoom_start=5,
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
        FastMarkerCluster(data=self.zip_data, icon_create_function=self.icon_cluster, callback=self.callback, options={'singleMarkerMode': True, 'maxClusterRadius':self.max_rad}).add_to(self.m)


    def render(self):
        FloatImage("https://github.com/iop-alliance/data_reports/blob/main/assets/img/iopa_logo_okw_sm.png?raw=true", bottom=5, left=5).add_to(self.m)
        return self.m.get_root().render()



class Tabular():
    
    def __init__(self, dataframe):
        self.data = dataframe
    
    def table_output(self):
        table_html = to_html_datatable(self.data, display_logo_when_loading=True, buttons=[
        "pageLength",
        {"extend": "csvHtml5", "title": "Manufacturing Locations"},
        {"extend": "excelHtml5", "title": "Manufacturing Locations"},],)
        return table_html
        

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

