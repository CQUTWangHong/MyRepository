# -*- coding: utf-8 -*-
import xgboost as xgb
import numpy as np
import pandas as pd
import time

start = time.time()

dataset = pd.read_csv("train.csv")
train = dataset.iloc[:,1:].values
labels = dataset.iloc[:,:1].values

tests = pd.read_csv("test.csv")
test = tests.iloc[:,:].values
# print test
params = {
'booster':'gbtree',
'objective':'multi:softmax',
'num_class':10,
'gamma':0.05,
'max_depth':12,
'subsample':0.4,
'colsample_bytree':0.7,
'silent':1,
'eta':0.005,
'seed':710,
'nthread':2
}

offset = 35000
# 迭代次数
num_rounds = 500
# 测试集
xgtest = xgb.DMatrix(test)
# 训练集
xgtrain = xgb.DMatrix(train[:offset,:],label = labels[:offset])
# 验证集
xgval = xgb.DMatrix(train[offset:,:],label = labels[offset:])

watchlist = [(xgtrain,'train'),(xgval,'val')]

model = xgb.train(params.items(),xgtrain,num_rounds,watchlist,early_stopping_rounds = 100)

preds = model.predict(xgtest,ntree_limit = model.best_iteration)

# numpy自带的写文件函数，所写的数据要是numpy.array
# 其中fmt参数为数据的格式，delimiter为分隔符，header为列名，comments为列名前的注释
np.savetxt('result.txt',np.c_[range(1,len(test)+1),preds],
	fmt = '%d',delimiter=',',header='ImageID,Label',comments='')

end = time.time()
Cost_time = end-start
print Cost_time