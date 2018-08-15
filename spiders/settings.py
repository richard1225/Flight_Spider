
import pymysql
import pymysql.cursors
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "www.csair.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}

class OperateDB():
    def __init__(self):
        # Connect to the database
        self.connection = pymysql.connect(host='127.0.0.1',
                                    user='root',
                                    password='richardtt',
                                    db='flight',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

    def insert(self, sql):
        self.connection.cursor().execute(sql)
        self.connection.commit()


    def query(self, sql):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
    
    def close(self):
        self.connection.close()