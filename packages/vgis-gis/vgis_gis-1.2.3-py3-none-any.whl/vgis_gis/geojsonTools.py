"""
#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
@Project :pythonCodeSnippet
@File    :geojsonTools.py
@IDE     :PyCharm
@Author  :chenxw
@Date    :2023/12/5 14:16
@Descr:
"""

import os
import json
class GeoJsonHelper:


    def __init__(self):
        pass

    @staticmethod
    # 合并 geojson
    def merge_geojsons(self, geojson_files_path, merge_result_file):
        index = 0
        all_data = {}
        for file_name in os.listdir(geojson_files_path):
            geojson_file = os.path.join(geojson_files_path, file_name)
            with open(geojson_file, 'r', encoding='utf-8') as fp:
                each_data = json.load(fp)
            if index == 0:
                all_data = each_data
            else:
                all_data["features"] += each_data["features"]
        result_file = open(merge_result_file, "w")
        json.dump(all_data, result_file)
