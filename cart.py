from math import log
import operator
import treePlotter

"""
函数说明:计算给定数据集的香农熵

Parameters:
    dataSet - 数据集
Returns:
    shannonEnt - 经验熵农熵
Modify:
    2018-04-18
"""
def calcShannonEnt(dataSet):
    numEntires = len(dataSet)                       #返回数据集的行数
    labelCounts = {}                                #保存每个标签(Label)出现次数的字典
    for featVec in dataSet:                         #对每组特征向量进行统计
        currentLabel = featVec[-1]                  #提取标签(Label)信息
        if currentLabel not in labelCounts.keys():  #如果标签(Label)没有放入统计次数的字典,添加进去
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1                #Label计数
    shannonEnt = 0.0                                #经验熵(香农熵)
    for key in labelCounts:                            #计算香农熵
        prob = float(labelCounts[key]) / numEntires    #选择该标签(Label)的概率
        shannonEnt -= prob * log(prob, 2)            #利用公式计算
    return shannonEnt                                #返回经验熵(香农熵)

def splitDataSet(dataSet, axis, value):
    """
    输入：数据集，选择维度，选择值
    输出：划分数据集
    描述：按照给定特征划分数据集；去除选择维度中等于选择值的项
    """
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reduceFeatVec = featVec[:axis]
            reduceFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reduceFeatVec)
    return retDataSet
    """
    输入：数据集
    输出：最好的划分维度
    描述：选择最好的数据集划分维度
    """
def chooseBestFeatureToSplit(dataSet):

    numFeatures = len(dataSet[0]) - 1
    bestGini = 999999.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        gini = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            subProb = len(splitDataSet(subDataSet, -1, 'N')) / float(len(subDataSet))
            gini += prob * (1.0 - pow(subProb, 2) - pow(1 - subProb, 2))
        if (gini < bestGini):
            bestGini = gini
            bestFeature = i
    return bestFeature
def majorityCnt(classList):
    """
    输入：分类类别列表
    输出：子节点的分类
    描述：数据集已经处理了所有属性，但是类标签依然不是唯一的，
          采用多数判决的方法决定该子节点的分类
    """
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reversed=True)
    return sortedClassCount[0][0]

def createTree(dataSet, labels):
    """
    输入：数据集，特征标签
    输出：决策树
    描述：递归构建决策树，利用上述的函数
    """
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        # 类别完全相同，停止划分
        return classList[0]
    if len(dataSet[0]) == 1:
        # 遍历完所有特征时返回出现次数最多的
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    # 得到列表包括节点所有的属性值
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree

def classify(inputTree, featLabels, testVec):
    """
    输入：决策树，分类标签，测试数据
    输出：决策结果
    描述：跑决策树
    """
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    classLabel = 'N'
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel
def classifyAll(inputTree, featLabels, testDataSet):
    """
    输入：决策树，分类标签，测试数据集
    输出：决策结果
    描述：跑决策树
    """
    classLabelAll = []
    for testVec in testDataSet:
        classLabelAll.append(classify(inputTree, featLabels, testVec))
    return classLabelAll

def storeTree(inputTree, filename):
    """
    输入：决策树，保存文件路径
    输出：
    描述：保存决策树到文件
    """
    import pickle
    fw = open(filename, 'wb')
    pickle.dump(inputTree, fw)
    fw.close()

def grabTree(filename):
    """
    输入：文件路径名
    输出：决策树
    描述：从文件读取决策树
    """
    import pickle
    fr = open(filename, 'rb')
    return pickle.load(fr)

def createDataSet():
    """
    outlook->  0: sunny | 1: overcast | 2: rain
    temperature-> 0: hot | 1: mild | 2: cool
    humidity-> 0: high | 1: normal
    windy-> 0: false | 1: true
    """
    dataSet = [[0, 0, 0, 0, 'no'],  # 数据集
               [0, 0, 0, 1, 'no'],  # 年龄，有工作，有房子，信贷情况，是否给贷款
               [0, 1, 0, 1, 'yes'],  # 年龄：0青年 1中年 2 老年
               [0, 1, 1, 0, 'yes'],  # 工作：0否 1是
               [0, 0, 0, 0, 'no'],  # 房子：0否 1是
               [1, 0, 0, 0, 'no'],  # 信贷情况：0一般 1好 2非常好
               [1, 0, 0, 1, 'no'],  # 是否给贷款：no否 yes 是
               [1, 1, 1, 1, 'yes']
              ]
    labels = ['Age', 'Work', 'House', 'Truth']  # 分类属性
    return dataSet, labels  # 返回数据集和分类属性

def createTestSet():
    """
    outlook->  0: sunny | 1: overcast | 2: rain
    temperature-> 0: hot | 1: mild | 2: cool
    humidity-> 0: high | 1: normal
    windy-> 0: false | 1: true
    """
    testSet = [ [1, 0, 1, 2,],
               [1, 0, 1, 2,],
               [2, 0, 1, 2, ],
               [2, 0, 1, 1, ],
               [2, 1, 0, 1, ],
               [2, 1, 0, 2, ],
               [2, 0, 0, 0, ]]
    return testSet

def main():
    dataSet, labels = createDataSet()
    labels_tmp = labels[:] # 拷贝，createTree会改变labels
    desicionTree = createTree(dataSet, labels_tmp)
    #storeTree(desicionTree, 'classifierStorage.txt')
    #desicionTree = grabTree('classifierStorage.txt')
    print('desicionTree:\n', desicionTree)
    treePlotter.createPlot(desicionTree)
    testSet = createTestSet()
    print('classifyResult:\n', classifyAll(desicionTree, labels, testSet))

if __name__ == '__main__':
    main()