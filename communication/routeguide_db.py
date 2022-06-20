# -*- coding: UTF-8 -*-
"""
@Summary ：
@Author  ：Zhuguojun
@Time    ：2022-06-20 14:21
@log     ：
            author datetime(DESC) summary
"""
import json
import routeguide_pb2

def read_routeguide_db():
    feature_list = []
    with open('routeguide_db.json') as f:
        for item in json.load(f):
            feature = routeguide_pb2.Feature(
                name = item['name'],
                location = routeguide_pb2.Point(
                    latitude=item['location']['latitude'],
                    longitude=item['location']['longitude']
                )
            )
            feature_list.append(feature)
    return feature_list
