'''
Created on 2016-4-16

@author: Administrator
'''
import os
import math
def ImportData(flag):
    if flag==1:
        f=open('trainIris.txt','r')#读取训练数据
        text = f.readlines()
        f.close()
    else:
        f=open('testIris.txt','r')#读取测试数据
        text = f.readlines()
        f.close()
    return text

def main():
    #Iris的4种属性
    v1 = [0,0,0]
    v2 = [0,0,0]
    v3 = [0,0,0]
    v4 = [0,0,0]
    text = ImportData(1)
    for line in text:
        vector = line.split()
        v1[int(vector[4])-1]+=float(vector[0])
        v2[int(vector[4])-1]+=float(vector[1])
        v3[int(vector[4])-1]+=float(vector[2])
        v4[int(vector[4])-1]+=float(vector[3])
    class1 = [v1[0]/25,v2[0]/25,v3[0]/25,v4[0]/25]
    class2 = [v1[1]/25,v2[1]/25,v3[1]/25,v4[1]/25]
    class3 = [v1[2]/25,v2[2]/25,v3[2]/25,v4[2]/25]
    clength1 = pow(class1[0],2)+pow(class1[1],2)+pow(class1[2],2)+pow(class1[3],2)
    clength2 = pow(class2[0],2)+pow(class2[1],2)+pow(class2[2],2)+pow(class2[3],2)
    clength3 = pow(class3[0],2)+pow(class3[1],2)+pow(class3[2],2)+pow(class3[3],2)
    print(class1,'长度',clength1)
    print(class2,'长度',clength2)
    print(class3,'长度',clength3)
    text = ImportData(2)
    true = 0
    for line in text:
        print(line)
        vector = line.split()
        for i in range(len(vector)-1):
            vector[i] = float(vector[i])
        vector[len(vector)-1] = int(vector[len(vector)-1])
        #用夹角的余弦值计算相似度
        sim1 = 0
        sim2 = 0
        sim3 = 0
        vlength = 0
        for i in range(len(vector)-1):
            sim1 += class1[i]*vector[i]
            sim2 += class2[i]*vector[i]
            sim3 += class3[i]*vector[i]
            vlength += pow(vector[i],2)
        sim1 = sim1/(math.sqrt(vlength)*math.sqrt(clength1))
        sim2 = sim2/(math.sqrt(vlength)*math.sqrt(clength2))
        sim3 = sim3/(math.sqrt(vlength)*math.sqrt(clength3))
        print('sim1',sim1,'sim2',sim2,'sim3',sim3)
        sim = max(sim1,sim2,sim3)
        flag = 0
        if sim==sim1:
            flag=1
        elif sim==sim2:
            flag=2
        else:
            flag=3
        if flag==vector[len(vector)-1]:
            true = true+1
    print('正确率',true/75)
if __name__ == '__main__':
    main()