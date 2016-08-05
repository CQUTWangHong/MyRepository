
'''
Created on 2016-6-27

@author: Administrator
'''
from math import log

def createDataSet():
    dataSet = [[u'青年', u'否', u'否', u'一般', u'拒绝'],
               [u'青年', u'否', u'否', u'好', u'拒绝'],
               [u'青年', u'是', u'否', u'好', u'同意'],
               [u'青年', u'是', u'是', u'一般', u'同意'],
               [u'青年', u'否', u'否', u'一般', u'拒绝'],
               [u'中年', u'否', u'否', u'一般', u'拒绝'],
               [u'中年', u'否', u'否', u'好', u'拒绝'],
               [u'中年', u'是', u'是', u'好', u'同意'],
               [u'中年', u'否', u'是', u'非常好', u'同意'],
               [u'中年', u'否', u'是', u'非常好', u'同意'],
               [u'老年', u'否', u'是', u'非常好', u'同意'],
               [u'老年', u'否', u'是', u'好', u'同意'],
               [u'老年', u'是', u'否', u'好', u'同意'],
               [u'老年', u'是', u'否', u'非常好', u'同意'],
               [u'老年', u'否', u'否', u'一般', u'拒绝'],
               ]
    labels = [u'年龄', u'有工作', u'有房子', u'信贷情况']
    #change to discrete values
    return dataSet, labels

def calcEntropy(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    Entropy = 0.0
    for key in labelCounts:                     #此处计算的是经验熵H(D)
        prob = float(labelCounts[key])/numEntries
        Entropy += -1*prob*log(prob,2)
    return Entropy

def splitDataSet(dataSet,axis,value):       #此函数作用在于选择特征axis等于value时的所有数据（除了value）
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet
    
def chooseBestFeatureTosplit(dataSet):
    numFeatures = len(dataSet[0])-1         #统计特征的数量
    ExperEntropy = calcEntropy(dataSet)     #先算出数据集的经验熵
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]  #得到所有的第i组特征
        uniqueVals = set(featList)                      #得到不同的特征（去重）
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)#得到第i个特征等于value的训练数据
            prob = len(subDataSet)/float(len(dataSet))  #得到|Di|/|D|
            newEntropy += prob*calcEntropy(subDataSet)  #条件熵
        infoGain = ExperEntropy - newEntropy            #经验熵减去条件熵
        if(infoGain>bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i                             #得到最重要的特征
    return bestFeature

def majorityCnt(classList):                             #得到训练数据最多的类别
    classCount = []
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(),key=lambda f:f[1],reverse=True)
    return sortedClassCount

def createTree(dataSet,labels):         #labels为所有特征的名字,不是每行数据的类别
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList): #查看所有训练数据是否是同一类别
        return classList[0]
    if len(dataSet[0])==1:                              #如果训练数据只有没有属性了（只剩类别）
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureTosplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])                               #删除使用了的特征
    featValues = [example[bestFeat] for example in dataSet]     #选择最重要的所有特征
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree   

# if __name__ == '__main__':
#     dataSet,labels = createDataSet()
#     myTree = createTree(dataSet, labels)
#     print(myTree)

