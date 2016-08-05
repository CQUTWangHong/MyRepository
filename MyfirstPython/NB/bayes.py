'''
Created on 2016-7-2

@author: Administrator
'''
# -*- coding: utf-8 -*-
import random
import numpy as np

def textParse(Sentence):
    import re
    listOfTokens = re.split(r'\W*',Sentence)
    return [word.lower() for word in listOfTokens if len(word)>0]

def createVocabulary(docList):                  #多个文本列表构成的列表
    Vocab = set([])
    for doc in docList:
            Vocab = Vocab | set(doc)  #两个集合的并集
    return Vocab

def word2num(wordList,VocabSet):
    '''
    采用的文本词袋模型(bag of word)
    '''
    num = []
    for word in VocabSet:
        num.append(wordList.count(word))
    return num

def trainNB(trainMatrix,trainLabel):
    '''
    此算法实现了朴素贝叶斯算法
    利用了Numpy库的相同长度array数组可以直接相加减乘除的功能
    '''
    numTrainDoc = len(trainMatrix)      #训练的文本数
    numWord = len(trainMatrix[0])       #每篇文本的向量长度
    previousProb = sum(trainLabel)/numTrainDoc
    #拉普拉斯平滑处理，初始化时各项都为1
    p1Vect = np.ones(numWord)
    p0Vect = np.ones(numWord)
    for i in range(numTrainDoc):
        if(trainLabel[i]==1):
            p1Vect += trainMatrix[i]
        else:
            p0Vect += trainMatrix[i]
    p1Vect = p1Vect/sum(p1Vect)
    p0Vect = p0Vect/sum(p0Vect)
    return previousProb,p1Vect,p0Vect
    
def classify(testDoc,preProb,p1Vec,p0Vec):
    Prob1 = 1
    Prob0 = 1
    index = np.where(np.array(testDoc)!=0)
    testDoc = testDoc[index]
    numWord = len(testDoc)
    p1Vec = p1Vec[index]
    p0Vec = p0Vec[index]
    for i in range(numWord):
        Prob1 = Prob1 * pow(p1Vec[i], testDoc[i])
        Prob0 = Prob0 * pow(p0Vec[i], testDoc[i])
    if Prob1>Prob0:
        return 1
    else:
        return 0
    
def spamTrain():
    '''
    此函数为测试算法性能的函数
    其中包括数据处理，训练算法，测试算法等步骤
    '''
    docList = []
    classList = []
    vocabSet = []                       #词汇表
    for i in range(1,26):               #构建词汇表
        wordList = textParse(open('email/spam/%d.txt' %i).read())
        docList.append(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' %i).read())
        docList.append(wordList)
        classList.append(0)
    vocabSet = createVocabulary(docList)        #创建词汇表
    trainingSet = []
    testSet = []
    testLabel = []
    for i in range(10):
        randindex = int(random.uniform(0,50-i))   #随机取一个0到50之间的数
        testSet.append(word2num(docList[randindex], vocabSet))
        del(docList[randindex])         #词汇表中删除该记录
        testLabel.append(classList[randindex])
        del(classList[randindex])
    for wordList in docList:
        trainingSet.append(word2num(wordList,vocabSet))
    preProb,p1Vec,p0Vec= trainNB(np.array(trainingSet),classList)
    errorCount = 0
    print('训练完成')
    for doc in testSet:
        if classify(np.array(doc), preProb, p1Vec, p0Vec) != testLabel[testSet.index(doc)]:
            errorCount += 1
    print('测试完成')
    print('错误个数',errorCount)
spamTrain()
        
        
        
        
        
        
        
        