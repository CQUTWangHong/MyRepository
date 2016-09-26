# -*- coding:utf-8 -*-
'''
Created on 2016-8-19
@author: Administrator
'''
import re
import numpy as np
import jieba.posseg as posg
import pickle
'''17种状态
nr    人名识别另做处理
ns    地名
nt    机构团体
nz    专有名词
O     其它
'''
#13种不同状态集合
states = ['B-ns','M-ns','E-ns','S-ns',
          'B-nt','M-nt','E-nt','S-nt',
          'B-nz','M-nz','E-nz','S-nz','O']
#28种观测序列集合
observations = ['/a','/b','/c','/d','/f','/h','/i','/j','/k','/l','/m',
                '/n','/p','/q','/r','/s','/t','/u','/v','/w','/ad','/an',
                '/vd','/vn','/nr','/ns','/nt','/nz']
#13种状态的初始概率
start_prob = {'B-ns':0,'M-ns':0,'E-ns':0,'S-ns':0,
              'B-nt':0,'M-nt':0,'E-nt':0,'S-nt':0,
              'B-nz':0,'M-nz':0,'E-nz':0,'S-nz':0,'O':0}
#13*13的numpy矩阵
transition_prob = np.zeros((13,13))         #传递概率
#13*28的numpy矩阵
emission_prob = np.zeros((13,28))           #命中概率
#复合命名实体的词性序列对应的概率
POSandPro = {}
#特征词及其词性
FeatureWords = {}

def getSequence():     #统计状态转移概率
    fr = open('F:\java_workplace\PythonLearning\HMM\199801.txt','r')
    pattern1 = re.compile('\[(.*?)\]')#查找组合命名实体
    pattern2 = re.compile('\[(.*?)\]n(\S+)')#需要替换的词
    pattern3 = re.compile("/n(\S+)")#找到所有独立命名实体
    pattern4 = re.compile("/(\S+)")#找到所有词性
    for line in fr.readlines():
        if line != '\n':                #去除空行
            result1 = pattern1.finditer(line)
            length = []
            for m1 in result1:              #计算组合命名实体长度
                length.append(len(m1.group(1).split('  ')))
            result2 = pattern2.finditer(line)
            count = 0
            newLine = line
            for m2 in result2:              #替换组合命名实体
                word = m2.group()[-2:]
                string = ''
                if length[count]==2:
                    string = '/B-'+word+' /E-'+word
                elif length[count]>2:
                    string ='/B-'+word
                    for i in range(length[count]-2):
                        string = string+' /M-'+word
                    string = string+' /E-'+word
                else:
                    print('组合命名实体长度有误')
                line = line.replace(m2.group(), string)
                newLine = newLine.replace(m2.group(),m2.group()[1:-3])
                count += 1
            result3 = pattern3.finditer(line)
            for m3 in result3:
                line = line.replace(m3.group(),'/S-'+m3.group()[-2:])
            result4 = pattern4.finditer(line)
            sequenceSpeech = []
            for m4 in result4:              #得到词性序列
                sequenceSpeech.append(m4.group()[1:])
            newResult4 = pattern4.finditer(newLine)
            newSequenceSpeech = []
            for newM4 in newResult4:
                newSequenceSpeech.append(newM4.group())
            for i in range(len(sequenceSpeech)):
                if sequenceSpeech[i] not in states:
                    sequenceSpeech[i]='O'
                    
            #统计句子首个词性个数
            start_prob[sequenceSpeech[0]] += 1
            #统计状态转移个数
            for i in range(len(sequenceSpeech)-1):
                x = states.index(sequenceSpeech[i])
                y = states.index(sequenceSpeech[i+1])
                transition_prob[x][y] += 1
            #统计命中概率个数
            for i in range(len(sequenceSpeech)):
                if newSequenceSpeech[i] in observations:
                    x = states.index(sequenceSpeech[i])
                    y = observations.index(newSequenceSpeech[i])
                    emission_prob[x][y] += 1
    fr.close()

def getStartProb():
    sum = 0
    for key in start_prob:
        sum += start_prob[key]
    for key in start_prob:
        start_prob[key] = start_prob[key]/sum

def getTransition():
    for i in range(np.shape(transition_prob)[0]):
        sum = 0
        for j in range(np.shape(transition_prob)[1]):
            sum += transition_prob[i][j]
        for j in range(np.shape(transition_prob)[1]):
            transition_prob[i][j] = transition_prob[i][j]/sum
            
def getEmission():
    for i in range(np.shape(emission_prob)[0]):
        sum = 0
        for j in range(np.shape(emission_prob)[1]):
            sum += emission_prob[i][j]
        for j in range(np.shape(emission_prob)[1]):
            emission_prob[i][j] = emission_prob[i][j]/sum

def InitialState(observation):
    return [start_prob.get(state)*emission_prob[states.index(state)][observations.index(observation[0])] for state in states]

def Viterbi(prob,i,obse):
    p = []
    newpath = []
    for j in range(len(states)):            #j代表要计算的状态
        (temp,state) = max([(prob[i-1][k]*transition_prob[k][j]*emission_prob[j][observations.index(obse)],states[k]) for k in range(len(states))])
        p.append(temp)
        newpath.append(state)
    return p,newpath

def test(sentence):
    fw = open('F:/java_workplace/PythonLearning/HMM/result.txt','w',encoding='utf-8')
    observation = []                    #观测序列
    Words = []
    words = posg.cut(sentence)
    for word in words:
        word = str(word)
        if word[word.index('/'):] in observations:
            observation.append(word[word.index('/'):])
            Words.append(word[:word.index('/')])
    print(Words)
    print(observation)
    print('HMM识别结果:')
    #人名识别较为容易，因此独立开来识别
    nrindex = [i for i in range(len(observation)) if observation[i]=='/nr']
    if len(nrindex)>0:
        names = []
        name = Words[nrindex[0]]
        for i in range(len(nrindex)-1):
            if nrindex[i]+1 == nrindex[i+1]:
                name += Words[nrindex[i+1]]
            else:
                names.append(name)
                name = Words[nrindex[i+1]]
        names.append(name)
        for name in names:          #输出识别到的人名
            print(name,end='nr ') 
            fw.write(name)
        fw.write('nr ')
    prob = []                       #存储各种状态的概率
    path = []                       #存储正向路径
    prob.append(InitialState(observation))        #先获得初始化概率
    for i in range(1,len(observation)):
        (p,newpath) = Viterbi(prob,i,observation[i])
        prob.append(p)
        path.append(newpath)
    temp = []                       #存储最优逆向路径
    #添加最后的状态
    temp.append(states[prob[-1].index(max(prob[-1]))])
    for i in range(1,len(path)+1):
        temp.append(path[-i][states.index(temp[-1])])
    result1 = []                    #存储HMM的识别结果
    for i in range(1,len(temp)+1):
        result1.append(temp[-i])
#     print(result1)
    for i in range(len(result1)):
        if 'B' in result1[i] or 'M' in result1[i]:
            print(Words[i],end='')
            fw.write(Words[i])
        if 'E' in result1[i] or 'S' in result1[i]:
            print(Words[i],'  '+result1[i][-2:])
            fw.write(Words[i])
            fw.write(result1[i][-2:]+'\n')
    
    length = 0
    start = 0
    end = 0
    result2 = {}
    for i in range(len(observation)):
        match = ''
        flag = False
        for j in range(i,len(observation)):
            match += observation[j]
            temp = {}
            for POS in POSandPro:
                #如果词性匹配
                if match == POS[:-4] and Words[j] in FeatureWords:
                    #如果特征词词性与词性序列词性匹配
                    if POS[-3:-1] in FeatureWords[Words[j]]:
                        if match.count('/')>length:
                            length = match.count('/')
                            start = i
                            end = j+1
                            temp[POS[-3:-1]] = POSandPro[POS]
                            result2 = temp
                            flag = True
        if flag == True:
            NE = ''
            for i in range(start,end):
                NE += Words[i]
            print('结合规则相后:  ',NE,max(result2))
            fw.write(NE)
            fw.write(max(result2))   
    
def storeData():
    filename = 'F:/java_workplace/PythonLearning/HMM/trainData.txt'
    fw = open(filename,'wb')
    pickle.dump((start_prob,transition_prob,emission_prob,POSandPro,FeatureWords),fw)

def grabData():
    filename = 'F:/java_workplace/PythonLearning/HMM/trainData.txt'
    fr = open(filename,'rb')
    return pickle.load(fr)
    
def train():                        #基于统计方法HMM的识别
    getSequence()                   #得到词性序列
    getStartProb()                  #计算初始概率
    getTransition()                 #计算状态转移概率
    getEmission()                   #计算命中概率

def rule():                         #对HMM识别出的结果进行规则修正
    fr = open('F:\java_workplace\PythonLearning\HMM\199801.txt','r')
    pattern1 = re.compile('\[(.*?)\]n(\S+)')#需要替换的词
    pattern2 = re.compile("/(\S+)")#找到所有词性
    for line in fr.readlines():
        if line != '\n':
            result1 = pattern1.finditer(line)
            for m1 in result1:
                #KeyWord为特征词
                KeyWord = m1.group(1).split()[-1][:m1.group(1).split()[-1].index('/')]
                if KeyWord in FeatureWords:
                    FeatureWords[KeyWord].add(m1.group()[-2:])
                else:
                    FeatureWords[KeyWord] = {m1.group()[-2:]}
                result2 = pattern2.finditer(m1.group(1))
                POS = ''
                for m2 in result2:
                    POS += m2.group()
                POS += '['+m1.group()[-2:]+']'
                if POS in POSandPro:
                    POSandPro[POS] += 1
                else:
                    POSandPro[POS] = 1
    fr.close()
    sum = 0
    for key in POSandPro:
        sum += POSandPro[key]
    for key in POSandPro:
        POSandPro[key] = POSandPro[key]/sum
def main():
    sentence = '哈尔滨工业大学'
#     train()
#     rule()
#     storeData()                     #存储训练后得到的数据
    #声明为全局变量
    global start_prob,transition_prob,emission_prob,POSandPro,FeatureWords
    #读取训练完的数据
    (start_prob,transition_prob,emission_prob,POSandPro,FeatureWords) = grabData()
    #测试
    test(sentence)
#     print(start_prob)
#     print(transition_prob)
#     print(emission_prob)
# print('I will run')
main()
# print('I am runned')