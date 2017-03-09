#!/usr/bin/env python
# encoding: utf-8

import DTK_linux
import cv2
import os
import oss2
import logging
import traceback
import time
import json
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from PIL import Image
from mns.mns_exception import MNSExceptionBase
from data_op import save_scan_data
from bson import ObjectId

'''
def insert_segImgData_result(handler, oss_data):

    try:
        result = DTK_linux.segImgData(oss_data['raw_data0'], oss_data['width0'], oss_data['height0'],
                                      oss_data['raw_data1'], oss_data['width1'], oss_data['height1'])
        ret = list()
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

        _id = handler.db[1].recognition_template.insert(ret[0])

        ret[1]['another_id'] = _id
        another_id = handler.db[1].recognition_template.insert(ret[1])
        handler.db[1].recognition_template.update({"_id": _id}, {"$set": {'another_id': another_id}})
        return True
    except:
        return False
'''

def pick_oss(handler, key):
    key_another = key[:-5] + str(int(key[-5]) ^ 1) + '.jpg'
    tem_key = key[key.rfind('/')+1:]
    tem_key_another = key_another[key_another.rfind('/')+1:]
    try:
        handler.bucket.get_object_to_file(key, tem_key)
        handler.bucket.get_object_to_file(key_another, tem_key_another)
    except oss2.exceptions.NoSuchKey:
        time.sleep(1)
        handler.bucket.get_object_to_file(key, tem_key)
        handler.bucket.get_object_to_file(key_another, tem_key_another)
    finally:
        if not(os.path.exists(tem_key) and os.path.exists(tem_key_another)):
            logging.fatal('get oss error from key:{} and {}'.format(key, key_another))
            handler.message = None
            return False

    img1 = cv2.cv.LoadImage(tem_key, 0)  # tem_key 为背面
    img0 = cv2.cv.LoadImage(tem_key_another, 0)

    data = dict()
    data['height0'] = img0.height
    data['width0'] = img0.width
    data['height1'] = img1.height
    data['width1'] = img1.width
    data['raw_data0'] = img0.tostring()
    data['raw_data1'] = img1.tostring()
    data['oss_key0'] = key_another
    data['oss_key1'] = key
    os.remove(tem_key)
    os.remove(tem_key_another)
    logging.info('get oss success from key:{} and {}'.format(key, key_another))
    return data


def pick_message(handler):
    while True:
        while handler.message is None:
            try:
                handler.message = handler.queue.receive_message(10)
            except MNSExceptionBase, e:
                logging.info('mns fail returns: ' + str(e))
                handler.message = None
                time.sleep(1)

        try:
            message = json.loads(handler.message.message_body)
        except:
            logging.fatal('bad message ' + handler.message.message_body)
            handler.message = None
            handler.pop()
        else:
            logging.info('Got message: ' + str(message))
            return message


def get_json_info(handler, qr_code):
    if 'cid' not in qr_code:
        return '', ''
    info = handler.db[1].recognition_template.find_one({"cid": qr_code['cid'], 'no': 1})
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

    info = handler.db[1].recognition_template.find_one({"cid": qr_code['cid'], 'no': 2})
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


def get_answer(qzRanswer):
    answers = list()
    if qzRanswer == 'A':
        answer = 0
    elif qzRanswer == 'B':
        answer = 1
    elif qzRanswer == 'C':
        answer = 2
    elif qzRanswer == 'D':
        answer = 3
    else:
        answer = qzRanswer
    answers.append([answer, ])
    return answers


def get_rec_Qrcode(handler, oss_data):
    result = DTK_linux.rec_QrCode(oss_data['raw_data0'], oss_data['width0'], oss_data['height0'],
                                  oss_data['raw_data1'], oss_data['width1'], oss_data['height1'])
    logging.critical(u'result:{}'.format(result))
    mark = list()
    for index in range(0, len(result)):
        if result[index] == ',':
            mark.append(index)
    detail = {
        'subject': result[mark[2] + 1:],
        'cid': result[:mark[0]],
        'book_paper_id': ObjectId(result[:mark[0]]),
    }
    logging.critical(u'detail:{}'.format(detail))
    return detail


def get_details(handler, qzR, book_paper_id, dis_page, key):
    try:
        dis_details = list()
        book_paper = handler.db[1].book_papers.find_one({'_id': book_paper_id})
        if book_paper is None:
            return None

        questions = [question for question in book_paper['items'][dis_page]]
        for i in range(0, len(questions)):
            if i >= qzR.size():
                detail = {
                    'item_type': questions[i]['item_type'],
                    'score_list': [None, ],
                    'item_id': questions[i]['item_id'],
                    'answers': [None, ],
                    'img_list': [None, ]
                }
            else:
                answers = get_answer(qzR[i].answer)
                width = qzR[i].qzone.width
                height = qzR[i].qzone.height
                img_buffer = qzR[i].qzone.buffer
                oss_file_path = u'img_list' + os.sep + key[:-4] + 'z' + str(i) + '.jpg'
                try:
                    img = Image.frombytes('L', (width, height), img_buffer)
                    img_path = u'{}_{}_{}.jpg'.format(book_paper_id, dis_page, i)
                    img.save(u'{}_{}_{}.jpg'.format(book_paper_id, dis_page, i))
                    handler.bucket.put_object_from_file(oss_file_path, img_path)
                    #os.remove(img_path)
                    oss_file_path = handler.oss_img_path + oss_file_path
                except:
                    logging.info(u'upload img fail:{}'.format(oss_file_path))
                    oss_file_path = None
                score = qzR[i].score if qzR[i].score <= questions[i]['total_score'] else None

                detail = {
                    'item_type': 1001 if qzR[i].type == 0 else 1002,
                    'score_list': [score, ],
                    'item_id': questions[i]['item_id'],
                    'answers': answers,
                    'img_list': [oss_file_path, ]
                }
            dis_details.append(detail)
        logging.critical(u'get_dis_details_successful')
        return dis_details
    except:
        print traceback.print_exc()


def insert_result(handler, layout1, layout2, oss_data, qr_code):
    result = DTK_linux.getSegRecResult2(layout1, layout2,
                                        oss_data['raw_data0'], oss_data['width0'], oss_data['height0'],
                                        oss_data['raw_data1'], oss_data['width1'], oss_data['height1'])
    subject = qr_code['subject']
    school_name = oss_data['oss_key1'][oss_data['oss_key1'].rfind('/')+1:oss_data['oss_key1'].rfind('x')]
    school_id = handler.userdb.shcool_info.find_one({'name': school_name})
    batch_id = oss_data['oss_key1'][oss_data['oss_key1'].rfind('x') + 1:oss_data['oss_key1'].rfind('y')]

    student_number = float(result[0].student)
    print student_number
    a = open('a', 'aw+')
    a.write(" {} ".format(student_number))
    a.close()
    school_name = '清华大学附属中学'
    if student_number is not None:
        student = handler.userdb.student_number_in_school.find_one({'number': float(student_number),
                                                                    'school': school_name})
        if student is None:
            student_username = ''
            teacher_username = ''
        else:
            student_username = student['username']
            cla = handler.userdb.qp_student.find_one({'username': student_username})
            if cla is None or 'class_id' not in cla:
                teacher_username = ''
            else:
                teacher = handler.userdb.qp_classes.find_one({'_id': cla['class_id']})
                if teacher is not None:
                    teacher_username = teacher['teachers'][subject]['username']
                else:
                    teacher_username = ''
    else:
        student_username = ''
        teacher_username = ''

    book_paper_id = qr_code['book_paper_id']
    try:
        dis_page0 = result[0].no
        dis_page1 = result[1].no
    except:
        dis_page0 = ''
        dis_page1 = ''
    dis_flag0 = '[{}_{}_{}]'.format(book_paper_id, dis_page0, student_username)
    dis_flag1 = '[{}_{}_{}]'.format(book_paper_id, dis_page1, student_username)
    try:
        dis_details0 = get_details(handler, result[0].qzR, book_paper_id, dis_page0-1, oss_data['oss_key0'])
        dis_details1 = get_details(handler, result[1].qzR, book_paper_id, dis_page1-1, oss_data['oss_key1'])
    except:
        dis_details0 = None
        dis_details1 = None
    save_scan_data(handler.db[1], batch_id, handler.oss_img_path + oss_data['oss_key0'],
                   handler.oss_img_path + oss_data['oss_key1'],
                   student_number, student_username, teacher_username, book_paper_id,
                   dis_page0, dis_details0, school_name, school_id, dis_flag0)
    save_scan_data(handler.db[1], batch_id, handler.oss_img_path + oss_data['oss_key1'],
                   handler.oss_img_path + oss_data['oss_key0'],
                   student_number, student_username, teacher_username, book_paper_id,
                   dis_page1, dis_details1, school_name, school_id, dis_flag1)
    logging.critical(u'save_scan_data successful: teacher:{} student:{} book_paper_id:{}'
                     .format(teacher_username, student_username, book_paper_id))

"""
    print 'batch_id: ', batch_id
    print 'source_img: ', oss_data['oss_key1']
    print 'back_img: ', oss_data['oss_key2']
    print 'dis_student_number: ', student_number
    print 'dis_student_username: ', student_username
    print 'dis_teacher_username: ', teacher_username
    print 'dis_book_paper_id: ', book_paper_id
    print 'school_name: ', school_name
    print 'school_id: ', school_id
    print 'dis_details0: ', dis_details0
    print 'dis_details1: ', dis_details1
    print 'save_scan_data_ok'
"""
