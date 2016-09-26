'''
Created on 2016-6-28

@author: Administrator
'''

import matplotlib.pyplot as plt
import DecisionTree.trees as tree
import pickle

decisionNode = dict(boxstyle="round4", color='r') #定义判断结点形态
leafNode = dict(boxstyle="circle", color='b')     #定义叶结点形态
arrow_args = dict(arrowstyle="<-", color='g')           #定义箭头

def plotNode(nodeTxt,To,From,nodeType):
    '''
        nodeTxt:节点名字
        To:箭头指向的节点的坐标
        From:箭头源的坐标
        nodeType:节点的类型(判断节点，叶节点)
    '''
    createPlot.ax1.annotate(nodeTxt,xy=From,xycoords='axes fraction',
                            xytext=To,textcoords='axes fraction',
                            va='center',ha='center',bbox=nodeType,
                            arrowprops=arrow_args)

def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree.keys())[0]             #Python3的keys返回的不是列表
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs +=getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs
    
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth = 1+getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth>maxDepth:
            maxDepth = thisDepth
    return maxDepth

def plotMidText(To,From,txtString):
    #求出箭头中点处的坐标
    xMid = (From[0]+To[0])/2.0
    yMid = (From[1]+To[1])/2.0
    #设置箭头中点处的String
    createPlot.ax1.text(xMid,yMid,txtString)
    
def plotTree(myTree,From,nodeTxt):
    leafNum = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    #此处用了全局变量plotTree.xOff等
    To = (plotTree.xOff+(1.0+float(leafNum))/2/plotTree.totalW,plotTree.yOff)
    plotMidText(To, From,nodeTxt)
    plotNode(firstStr, To, From, decisionNode)
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    secondDict = myTree[firstStr]
    for key in secondDict.keys():                  
        if type(secondDict[key]).__name__=='dict':  #如果该节点还是决策节点
            plotTree(secondDict[key], To, str(key))
        else:                                       #该节点是叶节点
            plotTree.xOff = plotTree.xOff + 1/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff,plotTree.yOff), To, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff),To, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD      #递归完后要返回上一父节点

def createPlot(myTree):
#     fig = plt.figure(1,facecolor='white')
#     fig.clf()
    plt.figure(1,facecolor='white')
#     plt.axis([0,2,0,2])
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    axprops = dict(xticks=[],yticks=[])
    #frameon设置是否显示方框，axprops设置是否显示坐标轴上的数据
    createPlot.ax1 = plt.subplot(111,frameon=False,**axprops)
    plotTree.totalW = float(getNumLeafs(myTree))
    plotTree.totalD = float(getTreeDepth(myTree))
    plotTree.xOff = -0.5/plotTree.totalW;
    plotTree.yOff = 1.0
    plotTree(myTree, (0.5,1.0), '')
    plt.show()

def classify(inputTree,featLabels,testVec):
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__=='dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel

def storeTree(inputTree,filename):
    fw = open(filename,'wb')            #pickle读写是以二进制文件存储的，所以要加b
    pickle.dump(inputTree,fw)
    fw.close()
    
def grabTree(filename):
    fr = open(filename,'rb')
    return pickle.load(fr)

#利用测试数据生成决策树字典
# dataSet,labels = tree.createDataSet()
# myTree = tree.createTree(dataSet, labels)

#存储树
# storeTree(myTree, 'tree.txt')

#读取树
myTree = grabTree('tree.txt')

#创建决策树的可视化
createPlot(myTree)

#测试数据
testlabel = ['有钱','没钱','年龄','有房子','有工作']
testVec = ['是','否','中年','是','否']
print(classify(myTree, testlabel, testVec))
    
    
    