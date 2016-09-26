'''
Created on 2016-7-24

@author: Administrator
'''
from math import exp
from numpy import *
import matplotlib.pyplot as plt

def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open('testSet.txt','r')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat

def sigmoid(z):
    return 1/(1+exp(-z))

def gradientAscent(dataMat,labelMat):       #梯度上升方法
    dataMatrix = mat(dataMat)
    classLabel = mat(labelMat).transpose()
    m,n = shape(dataMatrix)     #m为行数（数据的条数），n为列数（特征数量）
    weights = ones((n,1))       #此处记得添加括号，不然会报错
    num_iters = 500             #迭代次数
    alpha = 0.01                #学习素率
    for i in range(num_iters):
        h = sigmoid(dataMatrix*weights)
        error = classLabel-h
        #此处要主机classLabel-h和h-classLabel的区别
        #当为classLabel-h时为梯度上升，h-classLabel为梯度下降
        weights += alpha*dataMatrix.transpose()*error
    return weights
    
def plotBestFit(weight,dataMat,labelMat):
    x1 = []; y1 = []
    x0 = []; y0 = []
    for i in range(len(dataMat)):
        if(labelMat[i]==1):
            x1.append(dataMat[i][1])
            y1.append(dataMat[i][2])
        else:
            x0.append(dataMat[i][1])
            y0.append(dataMat[i][2])
    plt.figure()
    plt.subplot(1,1,1)
    plt.scatter(x1,y1,s=30,c='red',marker='s',label='1')
    plt.scatter(x0,y0,s=30,c='green',marker='o',label='0')
    x = arange(-3,3,0.1)
    y = (-weight[0]-weight[1]*x)/weight[2]
    plt.plot(x,y)
    '''
    Location String   Location Code
    ===============   =============
    'best'            0
    'upper right'     1
    'upper left'      2
    'lower left'      3
    'lower right'     4
    'right'           5
    'center left'     6
    'center right'    7
    'lower center'    8
    'upper center'    9
    'center'          10
    ===============   =============
    '''
    plt.legend(loc=0)
    plt.xlabel('x');plt.ylabel('y')
    plt.show()

def stoGradAscent(dataArr,labelArr,num_iters=150):       #改进的随机梯度上升算法
    m,n = shape(dataArr)
    weights = ones(n)
    for j in range(num_iters):
        for i in range(m):
            alpha = 4/(1.0+i+j)+0.01
            randIndex = int(random.uniform(0,m-i))      #每次随机选择一个样本
            h = sigmoid(sum(dataArr[randIndex])*weights)
            error = labelArr[randIndex]-h
            weights += alpha*error*dataArr[randIndex]
    return weights

#可视化分界线
dataMat,labelMat = loadDataSet()
# weight = gradientAscent(dataMat, labelMat)        #梯度上升算法
weight = stoGradAscent(array(dataMat), labelMat)    #随机梯度上升算法
plotBestFit(weight, dataMat, labelMat)
