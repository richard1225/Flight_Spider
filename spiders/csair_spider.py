#!-*- encoding:utf-8 -*-
"""
    site: 中国南方航空(China South)
"""
import sys
import time
import json
import hashlib
import settings
import requests
import traceback

reload(sys)
sys.setdefaultencoding('utf-8')

# 新建一个md5对象
hash_md5 = hashlib.md5()
SPDNAME = "csair"
COMNAME = "中国南方航空"
sqldb = settings.OperateDB()

APILIST = {
    "query": "https://b2c.csair.com/portal/minPrice/queryMinPriceInAirLines?jsoncallback=getMinPrice&inter=N&callback=getMinPrice&_=%s",
    "detail": "https://b2c.csair.com/B2C40/newTrips/static/main/page/booking/index.html?t=S&c1=%s&c2=%s&d1=%s&at=1&ct=0&it=0"
    #detail 三个参数 出发地, 目的地, 出发时间
}
class csairSpider():
    def __init__(self):
        pass

    def get_one(self, req_url):
        body = self.fetch_data(req_url)
        return self.parse(body)

    def parse(self, data):
        """
            @return json
        """
        try:
            data = data.split('getMinPrice(')[-1][:-1]
            return json.loads(data)
        except:
            print("parse Error: " + SPDNAME)
            traceback.print_exc()
        return

    def fetch_data(self, req_url):
        headers = settings.headers
        try:
            resp = requests.get(req_url)
            return resp.content
        except:
            print("request Error: " + SPDNAME)
            traceback.print_exc()
        return

    def pour_db(self, mjson):
        """
            灌库
        """
        mjson = mjson['FROMOFLIGHTS']
        for dep in mjson:
            name = dep['DEPCTIYNAME_ZH']
            for flight in dep['FLIGHT']:
                try:
                    depcity = name
                    arrcity = flight['ARRCTIYNAME_ZH']
                    price   = flight['MINPRICE']
                    depdate = flight['DEPDATE']
                    currency= flight['money']
                    company = COMNAME
                    detail_url = APILIST['detail']%(dep['DEPCITY'],flight['ARRCITY'],depdate)

                    h_md5 = hash_md5.copy()  # 复制一个对象，避免频繁创建对象消耗性能
                    h_md5.update((depcity + arrcity + depdate + company).encode('utf-8'))  # 需要将字符串进行编码，编码成二进制数据
                    fid = h_md5.hexdigest()  # 获取16进制的摘要

                    # 更新查询
                    sql = ("REPLACE INTO `prices_info` (`flight_id`, `depcity`, `arrcity`"
                          ", `price`, `depdate`, `currency`, `company`, `detail_url`) VALUES "
                          "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"%(fid,depcity,arrcity,price,depdate,currency,company,detail_url))
                    sqldb.insert(sql)
                except:
                    traceback.print_exc()
                    continue
        sqldb.close()

if __name__ == "__main__":
    spider = csairSpider()
    # 获取13位的时间戳
    now_time = int(time.time() * 1000)
    req_url = APILIST['query']%now_time

    # get json
    mjson = spider.get_one(req_url)
    spider.pour_db(mjson)
