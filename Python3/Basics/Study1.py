'''
Created on 2016-6-12

@author: Administrator
'''
import gzip
import urllib.request
# data = urllib.request.urlopen('http://www.baidu.com').read()
# date = gzip.decompress(data).decode('utf-8')
# print(date)

# values = {"username":"zhudiao2048","password":"12345qw"}
# data = urllib.parse.urlencode(values).encode(encoding='UTF8')
# url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
# req = urllib.request.Request(url,data)
# response = urllib.request.urlopen(req)
# print(response.read())

url = 'http://www.douban.com/'
webPage=urllib.request.urlopen(url)
data = webPage.read()
data = data.decode('UTF-8')
print(data)
print(type(webPage))
print(webPage.geturl())
# print(webPage.info())
# print(webPage.getcode())
