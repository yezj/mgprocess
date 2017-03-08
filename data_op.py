#!/usr/bin/env python
# encoding: utf-8

import time
import copy
from bson import ObjectId
import hashlib


def gen_md5(src):
    m2 = hashlib.md5()
    m2.update(src)
    return m2.hexdigest()


scan_data_tmp = {
    'batch_id': '',  # 批次id   psq
    'source_img': '',  # 大图
    'back_img': '',  # 背面大图
    'dis_student_number': '',  # 学号  识别获取
    'dis_student_username': '',  # 学生姓名  查库
    'dis_teacher_username': '',  # 老师姓名  查库
    'dis_book_paper_id': '',  # 二维码获取
    'dis_page': '',  # 当前页码  二维码
    'dis_details': [],  # 识别详情
    'dis_school_name': [],  # 学校名称
    'dis_school_id': '',  # 学校id
    'dis_detail_md5': '',
    'dis_flag': '',
    'dis_code': '',
    'int_student_number': '',
    'int_student_username': '',
    'int_page': '',
    'int_details': '',
    'skip_cnt': 0,
    'skip_time': 0,
    'ctime': time.time(),
    'init_time': time.time(),
    'init_status': 0,
    'status': 0,  # 0:扫描完成  1:需要手动选择学生的  2:已经归为作答数据了
    'abandon_teacher_usernames': [],
}


def get_student_user(userdb, school, number):
    s_n = userdb.student_number_in_school.find_one({'school': school,
                                                    'number': str(number)})
    if s_n is None:
        return None
    else:
        return s_n


def save_scan_data(db, batch_id, source_img, back_img, dis_student_number, dis_student_username,
                   dis_teacher_username, dis_book_paper_id, dis_page,
                   dis_details, dis_school_name, dis_school_id, dis_flag):
    scan_data = copy.deepcopy(scan_data_tmp)
    scan_data['batch_id'] = batch_id
    scan_data['source_img'] = source_img
    scan_data['back_img'] = back_img
    scan_data['dis_student_number'] = dis_student_number
    scan_data['dis_student_username'] = dis_student_username
    scan_data['dis_page'] = dis_page
    scan_data['dis_teacher_username'] = dis_teacher_username
    scan_data['dis_book_paper_id'] = dis_book_paper_id
    scan_data['dis_school_name'] = dis_school_name
    scan_data['dis_school_id'] = dis_school_id
    scan_data['dis_details'] = dis_details
    scan_data['dis_flag'] = dis_flag
    tmp_str = ''
    if dis_details is None:
        has_none = True
    else:
        has_none = False
        for detail in dis_details:
            if 'item_id' in detail:
                str_item_id = str(detail['item_id'])
            else:
                str_item_id = 'null_item_id'
            if detail is None:
                has_none = True
                break
            if detail['item_type'] == 1001:
                for answer in detail['answers']:
                    if answer is not None:
                        _str = str_item_id + '_' + str(answer) + '_'
                        tmp_str += _str
                    else:
                        has_none = True
            elif detail['item_type'] == 1002:
                for score in detail['score_list']:
                    if score is not None:
                        _str = str_item_id + '_' + str(int(score)) + '_'
                        tmp_str += _str
                    else:
                        has_none = True
    if has_none:
        tmp_str = ''
        scan_data['dis_code'] = '1110'
    else:
        scan_data['dis_code'] = '1111'
    scan_data['dis_detail_flag'] = tmp_str
    scan_data['dis_detail_md5'] = gen_md5(tmp_str)
    db.scan_datas.insert(scan_data)
