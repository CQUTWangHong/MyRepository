'''
start from 2016-4-18
finish up with 2016-4-28
@author: Striver
'''
#coding:utf-8

import os
import jieba
import time
from Test.SQLConnect import MyDB
from Test.BloomFilter import BloomFilter
from math import log
from math import sqrt
mydatabase = MyDB(host="localhost",user="sa",passwd="12345wh",db="Python")
mydatabase.ConnectDB()
class emotionclassfy:
    def __init__(self):
        pass
    def ImportStopWords(self):                          #导入停用词表到list
        filename = "停用词表2.txt"                    
        f = open(filename,'r')
        self.stopwords = f.readlines()                   #这样读取文件会在每行末尾加上\n
        for i in range(0,len(self.stopwords)):
            self.stopwords[i] = self.stopwords[i].rstrip('\n')#各行去掉'\n'
        f.close()
    
    def Pretreatment(self):#预处理
    #     sql1 = "if  object_id('nkeyword') is not null" +"\n"+"drop table nkeyword"
    #     sql2 = "if  object_id('pkeyword') is not null" +"\n"+"drop table pkeyword"
        sql1 = "delete from pCollect"
        sql2 = "delete from nCollect"
        sql3 = "delete from nkeyword"
        sql4 = "delete from pkeyword"
    #     mydatabase.ExeUpdateQuery(sql1)
    #     mydatabase.ExeUpdateQuery(sql2)
    #     mydatabase.ExeUpdateQuery(sql3)
    #     mydatabase.ExeUpdateQuery(sql4)
    #     mydatabase.commit()
    
    def Participle(self):                      #分词
        self.NTrainSet=mydatabase.ExeQuery("select * from nTrain")
        self.PTrainSet=mydatabase.ExeQuery("select * from pTrain")
        for row in self.NTrainSet:
            #此处要将从sqlserver里的中文数据转化为unicode编码
            Words = jieba.cut(row[0].encode('latin-1').decode('gbk'))
            for item in Words:
                if item not in self.stopwords:
                    sql = "insert into nCollect(word) values('%s')" %(item)
                    mydatabase.ExeUpdateQuery(sql)
        for row in self.PTrainSet:
            #此处要将从sqlserver里的中文数据转化为unicode编码
            Words = jieba.cut(row[0].encode('latin-1').decode('gbk'))
            for item in Words:
                if item not in self.stopwords:
                    sql = "insert into pCollect(word) values('%s')" %(item)
                    mydatabase.ExeUpdateQuery(sql)
    
    def GenerateDic(self):
        sql1 = "select word  from nCollect group by word"
        sql2 = "select word  from pCollect group by word"
        self.nkeywords = mydatabase.ExeQuery(sql1)
        self.pkeywords = mydatabase.ExeQuery(sql2)
    
    def CalculatorIDF(self):
        #统计IDF(耗时最长,约3300s)
        for keyword in self.nkeywords:
            count = 0
            KeyWord=keyword[0].encode('latin-1').decode('gbk')
            print(KeyWord)
            for row in self.NTrainSet:
                Words = jieba.cut(row[0].encode('latin-1').decode('gbk'))
                if KeyWord in Words:
                    count=count+1
                    continue
            count = log(295/count+0.5)
            print(count)
            sql = "insert into nkeyword(word,DF) values('%s',%s)" %(keyword[0].encode('latin-1').decode('gbk'),count)
            mydatabase.ExeUpdateQuery(sql)
             
        for keyword in self.pkeywords:
            count = 0
            KeyWord=keyword[0].encode('latin-1').decode('gbk')
            print(KeyWord)
            for row in self.PTrainSet:
                Words = jieba.cut(row[0].encode('latin-1').decode('gbk'))
                if KeyWord in Words:
                    count=count+1
                    continue
            count = log(1012/count+0.5)
            print(count)
            sql = "insert into pkeyword(word,DF) values('%s',%s)" %(keyword[0].encode('latin-1').decode('gbk'),count)
            mydatabase.ExeUpdateQuery(sql)
    
    def CalculatorTF(self):#统计TF
        filename1 = "NTF.txt"
        filename2 = "PTF.txt"
        f1 = open(filename1,'w')#计算消极训练集的TF
        for row in self.NTrainSet:
            #此处要将从sqlserver里的中文数据转化为unicode编码
            Words = jieba.cut(row[0].encode('latin-1').decode('gbk'))
            Words = list(Words)
            for keyword in self.nkeywords:
                KeyWord=keyword[0].encode('latin-1').decode('gbk')
                count = Words.count(KeyWord)
                if len(Words)!=0:
                    if count == 0:
                        f1.write(str(0)+' ')
                    else:
                        f1.write(str(count/len(Words))+' ')
                else:
                    f1.write('0 ')
            f1.write('\n')
        f1.close()
        f2 = open(filename2,'w')#计算积极训练集的TF
        for row in self.PTrainSet:
            #此处要将从sqlserver里的中文数据转化为unicode编码
            Words = jieba.cut(row[0].encode('latin-1').decode('gbk'))
            Words = list(Words)
            for keyword in self.pkeywords:
                KeyWord=keyword[0].encode('latin-1').decode('gbk')
                count = Words.count(KeyWord)
                if len(Words)!=0:
                    if count == 0:
                        f2.write(str(0)+' ')
                    else:
                        f2.write(str(count/len(Words))+' ')
                else:
                    f2.write('0 ')
            f2.write('\n')
        f2.close()
    def CategoryVector(self):#计算积极和消极类的特征向量以及它们的模长
        #计算消极的类的特征向量
        filename1 = "NTF.txt"
        filename2 = "PTF.txt"
        FeatureVector = []
        f3 = open(filename1,'r')
        Text = f3.readlines()
        for Vector in Text:
            FeatureVector.append(Vector.strip().split())
        self.ClassVector1 = []
        for i in range(2180):
            sum = 0
            for j in range(295):
                if FeatureVector[j][i] == '0':
                    sum=sum+int(FeatureVector[j][i])
                else:
                    sum=sum+float(FeatureVector[j][i])
            self.ClassVector1.append(sum/295)
        f3.close()
        #计算消极类别向量的模长
        sql = 'select DF from nkeyword'
        TF1 = mydatabase.ExeQuery(sql)
        count = 0
        for row in TF1:
            self.ClassVector1[count]*=1000*row[0]
            count=count+1
        self.Class1length = 0
        for i in self.ClassVector1:
            self.Class1length+=pow(i, 2)
        Class1length=sqrt(self.Class1length)
        print('消极类的特征向量',self.ClassVector1)
        #计算积极的类的特征向量
        FeatureVector = []
        f4 = open(filename2,'r')
        Text = f4.readlines()
        for Vector in Text:
            FeatureVector.append(Vector.strip().split())
        self.ClassVector2 = []
        for i in range(4706):
            sum = 0
            for j in range(1012):
                if FeatureVector[j][i] == '0':
                    sum=sum+int(FeatureVector[j][i])
                else:
                    sum=sum+float(FeatureVector[j][i])
            self.ClassVector2.append(sum/1012)
        f4.close()
        #计算积极类向量的模长
        sql = 'select DF from pkeyword'
        TF2 = mydatabase.ExeQuery(sql)
        count = 0
        for row in TF2:
            self.ClassVector2[count]*=1000*row[0]
            count=count+1
        self.Class2length = 0
        for i in self.ClassVector2:
            self.Class2length+=pow(i, 2)
        self.Class2length=sqrt(self.Class2length)
        print('积极类特征向量',self.ClassVector2)
    def Test(self):#将测试集的特征向量写入文件
        filename3 = 'NTestVectorforN.txt'
        filename4 = 'NTestVectorforP.txt'
        filename5 = 'PTestVectorforN.txt'
        filename6 = 'PTestVectorforP.txt'
        f5 = open(filename3,'w')
        f6 = open(filename4,'w')
        sql = 'select * from ntest'
        NTestSet = mydatabase.ExeQuery(sql)
        for row in NTestSet:
            Words = jieba.cut(row[0].encode('latin-1').decode('gbk'))
            Words = list(Words)
            for keyword in self.nkeywords:
                KeyWord=keyword[0].encode('latin-1').decode('gbk')
                count = Words.count(KeyWord)
                if len(Words)!=0:
                    if count == 0:
                        f5.write(str(0)+' ')
                    else:
                        f5.write(str(count/len(Words))+' ')
                else:
                    f5.write('0 ')
            for keyword in self.pkeywords:
                KeyWord=keyword[0].encode('latin-1').decode('gbk')
                count = Words.count(KeyWord)
                if len(Words)!=0:
                    if count == 0:
                        f6.write(str(0)+' ')
                    else:
                        f6.write(str(count/len(Words))+' ')
                else:
                    f6.write('0 ')
            f5.write('\n')
            f6.write('\n')
        f5.close()
        f6.close()
    
        #将测试集从文件导入列表
        ntest = open(filename5,'r')
        nText = ntest.readlines()
        nVectors = []
        for Vector in nText:
            nVectors.append(Vector.strip().split())
            
        ptest = open(filename6,'r')
        pText = ptest.readlines()
        pVectors = []
        for Vector in pText:
            pVectors.append(Vector.strip().split())
        #记录测试集的模长
        nlength = []
        for i in range(41):
            temp = 0
            for j in range(2180):
                temp += pow(float(nVectors[i][j]), 2)
            nlength.append(sqrt(temp))
            
        plength = []
        for i in range(41):
            temp = 0
            for j in range(4706):
                temp += pow(float(pVectors[i][j]), 2)
            plength.append(sqrt(temp))
        #计算测试集的特征向量与类别的相识度
        VectorProduct1 = []
        for i in range(41):
            temp = 0
            for j in range(2180):
                temp += float(nVectors[i][j])*self.ClassVector1[j]
            if(self.Class1length*nlength[i]==0):
                temp = 0
            else:
                temp=temp/(self.Class1length*nlength[i])
            VectorProduct1.append(temp)
        VectorProduct2 = []
        for i in range(41):
            temp = 0
            for j in range(4706):
                temp += float(pVectors[i][j])*self.ClassVector2[j]
            if(self.Class2length*plength[i]==0):
                temp = 0
            else:
                temp=temp/(self.Class2length*plength[i])
            VectorProduct2.append(temp)
        count1 = 0
        count2 = 0
        for i in range(41):
            if VectorProduct1[i]<=VectorProduct2[i]:
                count1+=1
            else:
                count2+=1
        print('消极测试集的正确率',count1/41,'错误个数',count2)
        
        #将积极测试集的特征向量写入文件
    #     f7 = open(filename5,'w')
    #     f8 = open(filename6,'w')
    #     sql = 'select * from ptest'
    #     PTestSet = mydatabase.ExeQuery(sql)
    #     for row in PTestSet:
    #         Words = jieba.cut(row[0].encode('latin-1').decode('gbk'))
    #         Words = list(Words)
    #         for keyword in nkeywords:
    #             KeyWord=keyword[0].encode('latin-1').decode('gbk')
    #             count = Words.count(KeyWord)
    #             if len(Words)!=0:
    #                 if count == 0:
    #                     f7.write(str(0)+' ')
    #                 else:
    #                     f7.write(str(count/len(Words))+' ')
    #             else:
    #                 f7.write('0 ')
    #         for keyword in pkeywords:
    #             KeyWord=keyword[0].encode('latin-1').decode('gbk')
    #             count = Words.count(KeyWord)
    #             if len(Words)!=0:
    #                 if count == 0:
    #                     f8.write(str(0)+' ')
    #                 else:
    #                     f8.write(str(count/len(Words))+' ')
    #             else:
    #                 f8.write('0 ')
    #         f7.write('\n')
    #         f8.write('\n')
    #     f7.close()
    #     f8.close()
    mydatabase.commit()
    mydatabase.close()
    
start = time.clock()#计算程序运行时间
test = emotionclassfy()#定义emotionclassfy对象
test.Pretreatment()#预处理
test.ImportStopWords()#导入停用词
test.Participle()#分词
test.GenerateDic()#生成词典
test.CalculatorIDF()#计算词典的IDF值
test.CalculatorTF()#计算训练集的TF值
test.CategoryVector()#利用质心向量分类算法得到积极类和消极类的特征向量
test.Test()#测试案例
end = time.clock()
print("时间",(end-start),"s")