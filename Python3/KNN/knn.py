'''
Created on 2016-6-19

@author: Administrator
'''
#代码来自机器学习实战
#此脚本是基于矩阵库numpy进行knn算法的实现
#如果不用矩阵来计算，将会有大量的冗长的代码，例如CC.IrisTest.py所示
from numpy import *
from os import listdir
import matplotlib
import matplotlib.pyplot as plt

def classify0(inx,dataSet,labels,k):#注意此处的dataSet必须为array数组,不能为矩阵
    dataSetSize = dataSet.shape[0]  #得到训练数据的个数
    diffMat = tile(inx,(dataSetSize,1))-dataSet#目标数据与训练数据相减
    sqDiffMat = diffMat**2;         #差的平方
    sqDistances = sqDiffMat.sum(axis=1)#平方和
    distance = sqDistances**0.5     #开根号
    sortedDisIndicies = distance.argsort()#返回数组值从小到大的索引值
    classCount = {}
    for i in range(k):              #选择前k个最近的点
        voteIlabel = labels[sortedDisIndicies[i]]
        classCount[voteIlabel] =  classCount.get(voteIlabel,0)+1
    #字典按value逆排序
    sortedClassCount = sorted(classCount.items(),key=lambda f:f[1],reverse=True)
    return sortedClassCount[0][0]

def file2Matrix(filename):              #读取文件数据到矩阵
    fr = open(filename)
    arrayOfLines = fr.readlines()
    rowOflines = len(arrayOfLines)
    returnMat = zeros((rowOflines,3))
    classLabelVector = []
    index = 0
    for line in arrayOfLines:
        line = line.strip()         #去除每行末尾的\n
        listLine = line.split('\t')
        returnMat[index,:] = listLine[0:3]
        classLabelVector.append(int(listLine[-1]))
        index+=1
    return returnMat,classLabelVector

def FeatureNormalization(dataSet):  #特征归一化用到公式newVals=(oldVals-min)/(max-min)
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals-minVals
    m = len(dataSet)
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1))
    return normDataSet

def ClassTest():                #选取10%的数据测试
    dataSet,Labels = file2Matrix('datingTestSet2.txt')
    normMat = FeatureNormalization(dataSet)
    Ratio = 0.1
    m = len(normMat)
    numTestVec = int(m*Ratio)   #所有数据中选取10%
    errorCount = 0
    for i in range(numTestVec):
        result = classify0(normMat[i,:], normMat[numTestVec:m,:],Labels[numTestVec:m],5)
        if(result!=Labels[i]):
            errorCount+=1
    print('错误个数',errorCount)
    print('错误率',errorCount/numTestVec)
    
def img2Vector(filename):           #将32*32的像素矩阵存入1*1024的向量
    returnVector = zeros((1,1024))
    fr = open(filename)
    lines = fr.readlines()
    count = 0
    for line in lines:
        line = line.strip()
        for i in range(32):
            returnVector[0,32*count+i] = int(line[i])
        count += 1
    return returnVector

def handWritingClassTest():     #手写数字识别测试代码,由于特征值都在0-1,不需要归一化
    hwLabels = []
    trainFileList = listdir('trainingDigits')
    mTrain = len(trainFileList)
    trainingMat = zeros((mTrain,1024))
    for i in range(mTrain):
        filenameStr = trainFileList[i]
        label = int(filenameStr[0])         #取文件名的第一个字符作为类标签
        hwLabels.append(label)
        #将所有图片的像素矩阵存入mTrain*1024维的矩阵
        trainingMat[i,:] = img2Vector('trainingDigits/%s' % filenameStr)
    testFileList = listdir('testDigits')
    errorcount = 0
    mTest = len(testFileList)
    for i in range(mTest):
        filenameStr = testFileList[i]
        label = int(filenameStr[0])
        testVector = img2Vector('testDigits/%s' % filenameStr)
        TestResult = classify0(testVector, trainingMat, hwLabels, 3)
        if(TestResult!=label):
            errorcount += 1
    print('错误个数',errorcount)
    print('错误率',errorcount/mTest)
handWritingClassTest()
def test():
    # k近邻算法
    # dataSet = array([[1,1.1],[1.1,1],[0,0],[-0.1,0.1]])
    # labels = ['1','1','-1','-1']
    # result=classify0([0.1,0.7], dataSet, labels, 3)
    # print(result)
    
    # 加载数据文件并转化成矩阵
    Matrix,Labels = file2Matrix('datingTestSet2.txt')
    fig = plt.figure()
    # ax = fig.add_subplot(1,2,1)
    # scatter函数第三个参数是设置散点的大小size,第四个参数是设置散点的颜色color（但是还不清楚到底是怎么设置的）
    plt.subplot(1,2,1)
    plt.scatter(Matrix[:,0],Matrix[:,1],s=15*array(Labels),c=15*array(Labels))
    plt.subplot(1,2,2)
    index1 = where(array(Labels)==1)        #注意此处得到的index是一个元祖
    index2 = where(array(Labels)==2)
    index3 = where(array(Labels)==3)
    plt.scatter(Matrix[index1,0],Matrix[index1,1],marker = 'x', color = 'm', label='didntLike', s = 20)
    plt.scatter(Matrix[index2,0],Matrix[index2,1],marker = '+', color = 'c', label='Like', s = 30)
    plt.scatter(Matrix[index3,0],Matrix[index3,1],marker = 'o', color = 'r', label='VeryLike', s = 40)
    plt.xlabel('miles')
    plt.ylabel('gametime')
    plt.legend(loc = 'upper left')
    plt.show()
    normMat = FeatureNormalization(Matrix)
    print(normMat)