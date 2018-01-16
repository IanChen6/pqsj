# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     
   Description :
   Author :       ianchen
   date：          
-------------------------------------------------
   Change Activity:
                   2017/11/22:
-------------------------------------------------
"""

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from guoshui import guoshui
from get_db import job_finish
from log_ging.log_01 import *
import json
import time
import redis
import os
import sys

redis_cli=redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
logger = create_logger(path=os.path.dirname(sys.argv[0]).split('/')[-1])


def run_test(user, pwd, batchid, batchyear, batchmonth,companyid, customerid,host,port,db):
    print("++++++++++++++++++++++++++++++++++++")
    print('jobs[ts_id=%s] running....' % batchid)
    time.sleep(2)
    try:
        gs = guoshui(user,pwd,batchid,batchyear, batchmonth,companyid, customerid,logger)
        gs.excute_spider()
        # logger.removeHandler()
    except Exception as e:
        logger.info("something wrong during crawling")
        logger.warn(e)
    print('jobs[ts_id=%s] done' % batchid)
    result = True
    return result
while True:
    # ss=redis_cli.lindex("list",0)
    ss=redis_cli.lpop("szgslist")
    if ss is not None:
    # print(redis_cli.lpop("list"))
        sd=json.loads(ss)
        run_test(sd["1"],sd["2"],sd["3"],sd["4"],sd["5"],sd["6"],sd["7"],sd["8"],sd["9"],sd["10"])
    else:
        time.sleep(20)
        print("no task waited")