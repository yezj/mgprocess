#!/usr/bin/env python
# encoding: utf-8

import os
import oss2
import logging
import traceback
import time
import json
import random
import sys
import conf
reload(sys)
from pymongo import MongoClient
sys.setdefaultencoding('utf8')
from PIL import Image
from mns.mns_exception import MNSExceptionBase
from data_op import save_scan_data
from bson import ObjectId

client = MongoClient(conf.mongo_host)
client['admin'].authenticate('root', 'qwer1234')
db = client['qp_shuxue']
print 'connect qp_shuxue successful'

def get_json_info(db, cid):

    info = db.recognition_template.find_one({"cid": cid, 'no': 1})
    if info is None:
        return '', ''
    layout1 = "{"
    layout1 += '"qz":['
    for index, qz in enumerate(info['qz']):
        if index != 0:
            layout1 += ','
        layout1 += '{'
        layout1 += '"y":{},"x":{},"height":{},"width":{},' \
            .format(qz['y'], qz['x'], qz['height'], qz['width'])
        layout1 += '"scorezones":['
        for cnt, scorezones in enumerate(qz['scorezones']):
            if cnt != 0:
                layout1 += ','
            layout1 += '{'
            layout1 += '"y":{},"x":{},"height":{},"width":{}'.format(scorezones['y'], scorezones['x'],
                                                                     scorezones['height'], scorezones['width'])
            layout1 += '}'
        layout1 += ']'
        layout1 += '}'
    layout1 += '],'
    layout1 += '"num":{},"no":{},"cid":"{}"'.format(info['num'], info['no'], info['cid'])
    layout1 += '}'

    info = db.recognition_template.find_one({"cid": cid, 'no': 2})
    if info is None:
        return '', ''
    layout2 = "{"
    layout2 += '"qz":['
    for index, qz in enumerate(info['qz']):
        if index != 0:
            layout2 += ','
        layout2 += '{'
        layout2 += '"y":{},"x":{},"height":{},"width":{},' \
            .format(qz['y'], qz['x'], qz['height'], qz['width'])
        layout2 += '"scorezones":['
        for cnt, scorezones in enumerate(qz['scorezones']):
            if cnt != 0:
                layout2 += ','
            layout2 += '{'
            layout2 += '"y":{},"x":{},"height":{},"width":{}'.format(scorezones['y'], scorezones['x'],
                                                                     scorezones['height'], scorezones['width'])
            layout2 += '}'
        layout2 += ']'
        layout2 += '}'
    layout2 += '],'
    layout2 += '"num":{},"no":{},"cid":"{}"'.format(info['num'], info['no'], info['cid'])
    layout2 += '}'
    return layout1, layout2

cid = "58379f74421aa9c513c68d71"

layout1, layout2 = get_json_info(db, cid)

