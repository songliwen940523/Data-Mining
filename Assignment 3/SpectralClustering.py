#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import *

import Kmedoids
import FastKmedoidsForBigData

'''
函数功能：
谱聚类算法，输入数据为data，构建邻接矩阵时所用的kNN算法的参数为n，kmedoids聚类时参数为k，
kmedoids算法类型为kmedoidtype，输出聚类结果clusters
数据结构：
data为mat结构，每一列代表一个数据，clusters为list结构，对应每个数据所属聚类的下标
'''

def spectralClustering(data, n, k, kmedoidstype):
    datanum = size(data, 1)
    #构建距离矩阵
    distgraph = mat(zeros([datanum, datanum]))
    for i in range(datanum):
        for j in range(i + 1, datanum):
            dist = linalg.norm(data[:, i] - data[:, j])
            distgraph[i, j] = dist
            distgraph[j, i] = dist

    #构建邻接矩阵
    adjgraph = mat(zeros([datanum, datanum]))
    for i in range(datanum):
        distances = distgraph[i, :]
        #取最近的n+1个数据，将距离写入邻接矩阵
        indices = argsort(distances)
        for count in range(1, n + 1):
            adjgraph[i, indices[0, count]] = 1
            adjgraph[indices[0, count], i] = 1

    #构建对角矩阵
    diaglist = []
    for i in range(datanum):
        diaglist.append(sum(adjgraph[:, i]))
    diagmat = diag(diaglist)

    L = diagmat - adjgraph #拉普拉斯矩阵
    M = linalg.inv(diagmat) * L
    evals, evcts = linalg.eig(M) #求特征值和特征向量
    indices = argsort(evals) #计算特征值从小到大排列的下标
    evals = evals[indices]
    evcts = evcts[:, indices]
    minevcts = evcts[:, 1:(k+1)] #取最小的k个特征向量（不包括最小的）
    redata = minevcts.T #降维
    print u'降维结束，开始kmedoids聚类...'

    #kmedoids聚类
    if(kmedoidstype == 'normal'):
        clusters = Kmedoids.kmedoids(redata, k)
    elif(kmedoidstype == 'fast'):
        clusters = FastKmedoidsForBigData.fastKmedoidsForBigData(redata, k)

    return clusters