#!/usr/bin/env python
# encoding: utf-8

import conf
import logging
import traceback
import time
import oss2
import DTK_linux
from pymongo import MongoClient
from mns.account import Account
from mns.mns_exception import MNSExceptionBase
from recognition import pick_oss
from recognition import pick_message
from recognition import get_rec_Qrcode
from recognition import get_json_info
from recognition import insert_result

_ALL_SUPPORT_SUBJECTS = ['yuwen', 'shuxue', 'yingyu',
                         'wuli', 'huaxue', 'shengwu',
                         'zhengzhi', 'lishi', 'dili']


class MNSReader(object):
    id = None
    secret = None
    point = None
    message = None
    queue_name = None
    db = dict()
    def __init__(self):
        self.id = conf.access_key_id
        self.secret = conf.access_key_secret
        self.point = conf.queue_endpoint
        self.queue_name = conf.queue_name
        self.auth = oss2.Auth(conf.access_key_id, conf.access_key_secret)
        self.bucket = oss2.Bucket(self.auth, conf.oss_endpoint, conf.bucket_name)
        self.oss_img_path = conf.oss_img_path
        client = MongoClient(conf.mongo_host)
        client['admin'].authenticate('root', 'qwer1234')
        self.userdb = client['qp_account']
        for index, subject in enumerate(_ALL_SUPPORT_SUBJECTS):
            db_name = 'qp_' + subject
            self.db[index] = client[db_name]
        logging.critical('connect mongodb success:{}'.format(conf.mongo_host))
        if self.id is None or self.secret is None or self.point is None or self.queue_name is None:
            raise Exception('lose conf')
        try:
            self.account = Account(self.point, self.id, self.secret)
            self.queue = self.account.get_queue(self.queue_name)
            logging.critical('init_MNS success:')
            logging.critical(u'id:{}, point:{}, queue_name'.format(self.id, self.point, self.queue_name))
        except:
            traceback.print_exc()
            raise Exception('connect MNS fail')

    def pop(self):
        retry = 2
        while retry > 0:
            try:
                self.queue.delete_message(self.message.receipt_handle)
            except MNSExceptionBase, e:
                logging.fatal('release message fail: ' + str(e))
                retry -= 1
                time.sleep(1)
            else:
                logging.info('release message success')
                break
        self.message = None

    def run_single(self):
        req = pick_message(self)
        key = req['events'][0]['oss']['object']['key']
        if key == 'test_connect' or key[-5] == '0':
            self.pop()
            return
        else:
            try:
                oss_data = pick_oss(self, key)
            except:
                logging.fatal(u'fail pick_oss:{}'.format(key))
                self.pop()
                return

        if oss_data:
            try:
                qr_code = get_rec_Qrcode(self, oss_data)
                i = DTK_linux.init_CNN_model("DTK.prototxt", "DTK.caffemodel", "DTK.binaryproto")
                json_info1, json_info2 = get_json_info(self, qr_code)
                insert_result(self, json_info1, json_info2, oss_data, qr_code)
                logging.critical(u'success DTK:{}'.format(key))
            except:
                logging.fatal(u'fail DTK:{}'.format(key))
            self.pop()

    def run(self):
        while True:
            try:
                self.run_single()
            except:
                traceback.print_exc()


if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL,
                        format='[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
                        datefmt='%y%m%d %H:%M:%S')
    reader = MNSReader()
    reader.run()
