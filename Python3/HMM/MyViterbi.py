'''
Created on 2016-8-9
@author: Administrator
数据来自维基百科
'''
states = ('Healthy', 'Fever')                           #隐状态
observations = ('normal', 'cold', 'dizzy')              #观察序列
start_probability = {'Healthy': 0.6, 'Fever': 0.4}      #初始概率
transition_probability = {                              #传递概率
    'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},
    'Fever' : {'Healthy': 0.4, 'Fever': 0.6}
}
emission_probability = {                                #发射概率
    'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
    'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
}
def InitialState():             #初始状态
    return [start_probability.get(state)*emission_probability.get(state).get(observations[0]) for state in states]

def Viterbi(prob,i):
    p = []
    newpath = []
    for j in states:            #j代表要计算的这天的概率
        (temp,state) = max([(prob[i-1][states.index(state)]*transition_probability[state][j]*emission_probability[j][observations[i]],state) for state in states])
        p.append(temp)
        newpath.append(state)
    return p,newpath
def main():
    prob = []
    path = []
    prob.append(InitialState())             #添加第一天两种情况的概率
    for i in range(1,len(observations)):    #从第一天往后
        (p,newpath) = Viterbi(prob,i)
        prob.append(p)
        path.append(newpath)
    print(prob)
#     print(path)
    result = []
    if prob[-1][0]<prob[-1][1]:
        result.append('Fever')
    else:
        result.append('Healthy')
    for i in range(1,len(path)+1):
        if result[-1]=='Fever':
            result.append(path[-i][1])
        else:
            result.append(path[-i][0])
    for i in range(1,len(result)+1):
        print(result[-i])
#     for p in prob:
#         if p[0]>p[1]:
#             print('第',prob.index(p)+1,'天为健康')
#         else:
#             print('第',prob.index(p)+1,'天为生病')
if __name__ == '__main__':
    main()