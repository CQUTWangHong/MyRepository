'''
Created on 2016-4-11

@author: Administrator
'''
import pymssql
import sys

class MyDB:
    '''对pymssql的简单封装'''
    def __init__(self,host,user,passwd,db):
        '''初始化变量'''
        self.host=host
        self.user=user
        self.passwd=passwd
        self.db=db
    def ConnectDB(self):
        '''获取连接信息'''
        if not self.db:
            raise(NameError,'没有设置数据库信息')
        #连接数据库
        self.connect=pymssql.connect(host=self.host,user=self.user,password=self.passwd,database=self.db,charset='utf8')
        self.cur = self.connect.cursor()
        if not self.cur:
            raise('连接数据库失败')
        else:
            return self.cur
    def ExeQuery(self,sql):
        '''执行sql的查询语句'''
        self.cur.execute(sql)
        resList = self.cur.fetchall()
        return resList
    def ExeUpdateQuery(self,sql):
        '''执行sql的更新语句'''
        self.cur.execute(sql)
    def commit(self):
        self.connect.commit()
    def close(self):
        #查询完毕后必须关闭连接
        self.connect.close()
def main():
    '''程序入口'''
    ms = MyDB(host="localhost",user="sa",passwd="12345wh",db="Python")
if __name__ == '__main__':
    main()