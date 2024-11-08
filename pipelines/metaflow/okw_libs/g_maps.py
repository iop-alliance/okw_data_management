#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 01:40:20 2024

@author: kny5
"""

from fastkml import kml
import re



def extract_kml_data(gmap_URL, func):
    pattern = r"mid=(\w+-\w+)"
    match = re.search(pattern, gmap_URL)
    mid_value = ""
    
    if not match:
        print("No 'mid' value found in the URL.")
    else:
        mid_value += match.group(1)
        print(f"The extracted 'mid' value is: {mid_value}")

    kml_url = "http://www.google.com/maps/d/kml?forcekml=1&mid=" + mid_value
    g_map = func(kml_url)
    kml_file = kml.KML()
    kml_file.from_string(g_map.content)

    return kml_file