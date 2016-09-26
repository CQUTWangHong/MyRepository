'''
Created on 2016-4-26

@author: Administrator
'''
#_*_coding:utf_8_
import BitVector
import os
import sys
# import time
# start = time.clock()
class SimpleHash():    
      
    def __init__(self, cap, seed):  
        self.cap = cap
        self.seed = seed
      
    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed*ret + ord(value[i])
        return (self.cap-1) & ret
  
class BloomFilter():
      
    def __init__(self, BIT_SIZE=1<<25):
        self.BIT_SIZE = 1 << 25
        self.seeds = [5, 7, 17, 13, 31, 37, 61 ,67]
        self.bitset = BitVector.BitVector(size=self.BIT_SIZE)#定义集合的大小为2的25次方
        self.hashFunc = []
    
        for i in range(len(self.seeds)):
            self.hashFunc.append(SimpleHash(self.BIT_SIZE, self.seeds[i]))  
        
    def insert(self, value):
        for f in self.hashFunc:
            loc = f.hash(value)
            self.bitset[loc] = 1  
    def isContains(self, value):  
        if value == None:  
            return False  
        ret = True
        for f in self.hashFunc:  
            loc = f.hash(value)  
            ret = ret & self.bitset[loc]  
        return ret  
  
def test():
    fd = open("urls.txt")
    bloomfilter = BloomFilter()
    while True:
        url = fd.readline()
        if url=='exit': #if url is equal exit break  
            break
        if bloomfilter.isContains(url) == False:
            bloomfilter.insert(url)
        else:
            print(url+'has exist')