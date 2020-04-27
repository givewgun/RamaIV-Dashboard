import os
import pandas as pd
import json


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

east_w = []
east_seg = []
east_seg_id = {}
west_w = []
west_seg = []
west_seg_id = {}
rama_iv_way = []

def load_segment():
    global east_w, east_seg, east_seg_id, west_w, west_seg, west_seg_id, rama_iv_way
    print(THIS_FOLDER)
    ways_json_f = os.path.join(THIS_FOLDER, 'segments', 'segment.json')
    with open(ways_json_f) as json_file:
        ways_json = json_file.read()
        ways_json = json.loads(ways_json)
    east_w = ways_json['east']['way_id']
    east_w = [str(w) for w in east_w]
    east_seg = ways_json['east']['segment']
    west_w = ways_json['west']['way_id']
    west_w = [str(w) for w in west_w]
    west_seg = ways_json['west']['segment']
    rama_iv_way = east_w + west_w

    lon_seg_f =  os.path.join(THIS_FOLDER, 'segments', 'lon_to_seg_map.json')
    with open(lon_seg_f) as json_file:
        lon_seg = json_file.read()
        lon_seg = json.loads(lon_seg)
    east_seg_id = lon_seg['east_seg_id']
    west_seg_id = lon_seg['west_seg_id']
    east_seg_id = { float(key):value for key,value in east_seg_id.items()}
    west_seg_id = { float(key):value for key,value in west_seg_id.items()}

load_segment()