#!/usr/bin/env python
# encoding: utf-8

import DTK_linux
import cv2
import conf
import os
import oss2
import logging
import traceback
import time
import json
import random
import sys
from pymongo import MongoClient
reload(sys)
sys.setdefaultencoding('utf8')
from PIL import Image
from mns.mns_exception import MNSExceptionBase
from data_op import save_scan_data
from bson import ObjectId


def insert_segImgData_result(db, data):

    try:
        result = DTK_linux.segImgData(data['raw_data0'], data['width0'], data['height0'],
                                      data['raw_data1'], data['width1'], data['height1'])
        ret = list()
        if result.size() == 2:
            print 'DTK_linux successful'
        else:
            print 'DTK_linux fail'
        for i in range(0, result.size()):
            page_one = dict()
            page_one['cid'] = result[i].cid
            page_one['num'] = result[i].num
            page_one['no'] = result[i].no
            page_one['qz'] = list()
            for j in range(result[i].qz.size()):
                qz = dict()
                qz['x'] = result[i].qz[j].qzone.x
                qz['y'] = result[i].qz[j].qzone.y
                qz['width'] = result[i].qz[j].qzone.width
                qz['height'] = result[i].qz[j].qzone.height
                qz['scorezones'] = list()
                for k in range(result[i].qz[j].scorezones.size()):
                    scorezones = dict()
                    scorezones['x'] = result[i].qz[j].scorezones[k].x
                    scorezones['y'] = result[i].qz[j].scorezones[k].y
                    scorezones['width'] = result[i].qz[j].scorezones[k].width
                    scorezones['height'] = result[i].qz[j].scorezones[k].height
                    qz['scorezones'].append(scorezones)
                page_one['qz'].append(qz)
            ret.append(page_one)

        _id = db.recognition_template.insert(ret[0])

        ret[1]['another_id'] = _id
        another_id = db.recognition_template.insert(ret[1])
        db.recognition_template.update({"_id": _id}, {"$set": {'another_id': another_id}})
        return True
    except:
        print 'insert：', traceback.print_exc()
        return False

client = MongoClient(conf.mongo_host)
client['admin'].authenticate('root', 'qwer1234')
db = client['qp_shuxue']
print 'connect qp_shuxue successful'

img0 = cv2.cv.LoadImage('muban_0.jpg', 0)
img1 = cv2.cv.LoadImage('muban_1.jpg', 0)  # 背面

data = dict()
data['height0'] = img0.height
data['width0'] = img0.width
data['height1'] = img1.height
data['width1'] = img1.width
data['raw_data0'] = img0.tostring()
data['raw_data1'] = img1.tostring()

flag = insert_segImgData_result(db, data)
print 'insert', flag
