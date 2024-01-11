def program1():
    text="""
def aStarAlgo(start_node, stop_node):
 
 open_set = set(start_node) 
 closed_set = set()
 g = {} #store distance from starting node
 parents = {}
 # parents contains an adjacency map of all #nodes
 #ditance of starting node from itself is zero
g[start_node] = 0
 #start_node is root node i.e it has no parent nodes
 #so start_node is set to its own parent node
 parents[start_node] = start_node
 
 while len(open_set) > 0:
 n = None
 #node with lowest f() is found
 for v in open_set:
 if n == None or g[v]+heuristic(v)< g[n] + heuristic(n):
 n = v
 
 if n == stop_node or Graph_nodes[n] == None:
 pass
 else:
 for (m, weight) in get_neighbors(n):
 #nodes 'm' not in first and last set are added to first
 #n is set its parent
 if m not in open_set and m not in closed_set:
 open_set.add(m)
 parents[m] = n
 g[m] = g[n] + weight
 #for each node m,compare its distance from start i.e g(m) to the
 #from start through n node
 else:
 if g[m] > g[n] + weight:
 #update g(m)
 g[m] = g[n] + weight
 #change parent of m to n
 parents[m] = n
 
 #if m in closed set,remove and add to open
 if m in closed_set:
 closed_set.remove(m)
 open_set.add(m)
if n == None:
 print('Path does not exist!')
 return None
 # if the current node is the stop_node then we
 # begin reconstructin the path from it to the start_node
 if n == stop_node:
 path = []
 while parents[n] != n:
 path.append(n)
 n = parents[n]
 path.append(start_node)
 path.reverse() 
 print('Path found: {}'.format(path))
 return path
 # remove n from the open_list, and add it to closed_list
 # because all of his neighbors were inspected
 open_set.remove(n)
 closed_set.add(n)
 print('Path does not exist!')
 return None
#define fuction to return neighbor and its distance from the passed node
def get_neighbors(v):
 if v in Graph_nodes:
 return Graph_nodes[v]
 else:
 return None
#for simplicity we ll consider heuristic distances given and this function returns heuristic 
#distance for all nodes
def heuristic(n):
 H_dist = {
 'A': 11,
 'B': 6,
 'C': 99,
'D': 1,
 'E': 7,
 'G': 0,
 }
 return H_dist[n]
#Describe your graph here 
Graph_nodes = {
 'A': [('B', 2), ('E', 3)],
 'B': [('C', 1),('G', 9)],
 'C': None,
 'E': [('D', 6)],
 'D': [('G', 1)],
}
aStarAlgo('A', 'G')
"""
    print(text)


def program2():
    text="""
class Graph:
 def __init__(self, graph, heuristicNodeList, startNode): #instantiate graph object with graph 
topology, heuristic values, start node
 
 self.graph = graph
 self.H=heuristicNodeList
 self.start=startNode
 self.parent={}
 self.status={}
 self.solutionGraph={}
 
 def applyAOStar(self): # starts a recursive AO* algorithm
 self.aoStar(self.start, False)
 def getNeighbors(self, v): # gets the Neighbors of a given node
 return self.graph.get(v,'')
 
 def getStatus(self,v): # return the status of a given node
 return self.status.get(v,0)
 
 def setStatus(self,v, val): # set the status of a given node
 self.status[v]=val
 
 def getHeuristicNodeValue(self, n):
 return self.H.get(n,0) # always return the heuristic value of a given node
 def setHeuristicNodeValue(self, n, value):
 self.H[n]=value # set the revised heuristic value of a given node 
 
 
 def printSolution(self):
 print("FOR GRAPH SOLUTION, TRAVERSE THE GRAPH FROM THE START
 NODE:",self.start)
 print("------------------------------------------------------------")
 print(self.solutionGraph)
 print("------------------------------------------------------------")
 
 def computeMinimumCostChildNodes(self, v): # Computes the Minimum Cost of child nodes of 
a given node v 
 minimumCost=0
 costToChildNodeListDict={}
 costToChildNodeListDict[minimumCost]=[]
 flag=True
 for nodeInfoTupleList in self.getNeighbors(v): # iterate over all the set of child node/s
 cost=0
 nodeList=[]
 for c, weight in nodeInfoTupleList:
 cost=cost+self.getHeuristicNodeValue(c)+weight
 nodeList.append(c)
 
 
 if flag==True: # initialize Minimum Cost with the cost of first set of child 
node/s 
 minimumCost=cost
 costToChildNodeListDict[minimumCost]=nodeList # set the Minimum Cost child 
node/s
 flag=False
 else: # checking the Minimum Cost nodes with the current Minimum Cost 
 if minimumCost>cost:
 minimumCost=cost
 costToChildNodeListDict[minimumCost]=nodeList # set the Minimum Cost child 
node/s
 
 
 return minimumCost, costToChildNodeListDict[minimumCost] # return Minimum Cost and 
Minimum Cost child node/s
def aoStar(self, v, backTracking): # AO* algorithm for a start node and backTracking status 
flag
 
 print("HEURISTIC VALUES :", self.H)
 print("SOLUTION GRAPH :", self.solutionGraph)
 print("PROCESSING NODE :", v)
 print("-----------------------------------------------------------------------------------------")
 
 
 if self.getStatus(v) >= 0: # if status node v >= 0, compute Minimum Cost nodes of v
 minimumCost, childNodeList = self.computeMinimumCostChildNodes(v)
 print(minimumCost, childNodeList)
 self.setHeuristicNodeValue(v, minimumCost)
 self.setStatus(v,len(childNodeList))
 
 solved=True # check the Minimum Cost nodes of v are solved 
 for childNode in childNodeList:
 self.parent[childNode]=v
 if self.getStatus(childNode)!=-1:
 solved=solved & False
 
 if solved==True: # if the Minimum Cost nodes of v are solved, set the current node 
status as solved(-1)
 self.setStatus(v,-1) 
 self.solutionGraph[v]=childNodeList # update the solution graph with the solved nodes 
which may be a part of solution 
 
 
 if v!=self.start: # check the current node is the start node for backtracking the current 
node value 
 self.aoStar(self.parent[v], True) # backtracking the current node value with backtracking 
status set to true
 
 if backTracking==False: # check the current call is not for backtracking 
for childNode in childNodeList: # for each Minimum Cost child node
 self.setStatus(childNode,0) # set the status of child node to 0(needs exploration)
 self.aoStar(childNode, False) # Minimum Cost child node is further explored with 
backtracking status as false
 
h1 = {'A': 1, 'B': 6, 'C': 2, 'D': 12, 'E': 2, 'F': 1, 'G': 5, 'H': 7, 'I': 7, 'J': 1}
graph1 = {
 'A': [[('B', 1), ('C', 1)], [('D', 1)]],
 'B': [[('G', 1)], [('H', 1)]],
 'C': [[('J', 1)]],
 'D': [[('E', 1), ('F', 1)]],
 'G': [[('I', 1)]] 
}
G1= Graph(graph1, h1, 'A')
G1.applyAOStar() 
G1.printSolution()
"""

    print(text)


def program3():
    text="""
import numpy as np
import pandas as pd
# Loading Data from a CSV File
data = pd.DataFrame(data=pd.read_csv('finds.csv'))
# Separating concept features from Target
concepts = np.array(data.iloc[:,0:-1])
# Isolating target into a separate DataFrame
target = np.array(data.iloc[:,-1])
def learn(concepts, target):
 specific_h=[0,0,0,0,0,0,0]
 print ('s0',specific_h)
 specific_h = concepts[0].copy()
 print('s1',specific_h)
 general_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
 print('g0',general_h)
 for i, h in enumerate(concepts):
 if target[i] == "Yes":
 for x in range(len(specific_h)):
 # Change values in S & G only if values change
 if h[x] != specific_h[x]:
 specific_h[x] = '?'
 general_h[x][x] = '?'
 print(f"s{x}",specific_h)
 print(f"g{x}",general_h)
 
 if target[i] == "No":
 for x in range(len(specific_h)):
 
 # For negative hyposthesis change values only in G
 if h[x] != specific_h[x]:
 general_h[x][x] = specific_h[x]
 else:
 general_h[x][x] = '?'
# find indices where we have empty rows, meaning those that are unchanged
 indices = [i for i,val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?', '?']]
 for i in indices:
 # remove those rows from general_h
 general_h.remove(['?', '?', '?', '?', '?', '?', '?'])
 print('i',indices) 
 # Return final values
 return specific_h,general_h
s_final, g_final = learn(concepts, target)
"""

    print(text)


def program4():
    text="""
import csv
import math
import random
# Class Node which will be used while classify a test-instance using the tree which was built 
#earlier
class Node():
 value = ""
 children = []
 def __init__(self, val, dictionary):
 self.value = val
 if (isinstance(dictionary, dict)):
 self.children = dictionary.keys()
# Majority Function which tells which class has more entries in given data-set
def majorClass(attributes, data, target):
 freq = {}
 index = attributes.index(target)
 for tuple in data:
 if tuple[index] in freq:
 freq[tuple[index]] += 1
 else:
 freq[tuple[index]] = 1
 
 max = 0
 major = ""
 for key in freq.keys():
 if freq[key]>max:
 max = freq[key]
 major = key
 return major
# Calculates the entropy of the data given the target attribute
def entropy(attributes, data, targetAttr):
 freq = {}
 dataEntropy = 0.0
 i = 0
 for entry in attributes:
 if (targetAttr == entry):
 break
 i = i + 1
 i = i - 1
 for entry in data:
 if entry[i] in freq:
 freq[entry[i]] += 1.0
 else:
 freq[entry[i]] = 1.0
 for freq in freq.values():
 dataEntropy += (-freq/len(data)) * math.log(freq/len(data), 2) 
 
 return dataEntropy
# Calculates the information gain (reduction in entropy) in the data when a particular #attribute is 
chosen for splitting the data.
def info_gain(attributes, data, attr, targetAttr):
 freq = {}
 subsetEntropy = 0.0
 i = attributes.index(attr)
 for entry in data:
 if entry[i] in freq:
 freq[entry[i]] += 1.0
 else:
 freq[entry[i]] = 1.0
 for val in freq.keys():
 valProb = freq[val] / sum(freq.values())
 dataSubset = [entry for entry in data if entry[i] == val]
 
 subsetEntropy += valProb * entropy(attributes, dataSubset, targetAttr)
 return (entropy(attributes, data, targetAttr) - subsetEntropy)
# This function chooses the attribute among the remaining attributes which has the #maximum 
#information gain.
def attr_choose(data, attributes, target):
 best = attributes[0]
 maxGain = 0;
 for attr in attributes:
 newGain = info_gain(attributes, data, attr, target) 
 if newGain>maxGain:
 maxGain = newGain
 best = attr
 return best
# This function will get unique values for that particular attribute from the given data
def get_values(data, attributes, attr):
 index = attributes.index(attr)
 values = []
 for entry in data:
 if entry[index] not in values:
 values.append(entry[index])
 return values
# This function will get all the rows of the data where the chosen "best" attribute has a #value "val"
def get_data(data, attributes, best, val):
 new_data = [[]]
 index = attributes.index(best)
 for entry in data:
 if (entry[index] == val):
 newEntry = []
 for i in range(0,len(entry)):
if(i != index):
 newEntry.append(entry[i])
 new_data.append(newEntry)
 new_data.remove([]) 
 return new_data
# This function is used to build the decision tree using the given data, attributes and the #target 
attributes. It returns the decision tree in the end.
def build_tree(data, attributes, target):
 data = data[:]
 vals = [record[attributes.index(target)] for record in data]
 default = majorClass(attributes, data, target)
 if not data or (len(attributes) - 1) <= 0:
 return default
 elif vals.count(vals[0]) == len(vals):
 return vals[0]
 else:
 best = attr_choose(data, attributes, target)
 tree = {best:{}}
 for val in get_values(data, attributes, best):
 new_data = get_data(data, attributes, best, val)
 newAttr = attributes[:]
 newAttr.remove(best)
 subtree = build_tree(new_data, newAttr, target)
 tree[best][val] = subtree
 
 return tree
#Main function
def execute_decision_tree():
 
 data = []
 #load file
 with open("playtennis.csv") as tsv:
 for line in csv.reader(tsv): 
 data.append(tuple(line))
 print("Number of records:",len(data))
 #set attributes
 attributes=['outlook','temperature','humidity','wind','play']
 target = attributes[-1]
#set training data
 acc = []
 training_set = [x for i, x in enumerate(data)]
 tree = build_tree( training_set, attributes, target )
 #execute algorithm on test data
 results = []
 test_set = [('rainy','mild','high','strong')]
 for entry in test_set:
 tempDict = tree.copy()
 result = ""
 while(isinstance(tempDict, dict)):
 root = Node(next(iter(tempDict)), tempDict[next(iter(tempDict))])
 tempDict = tempDict[next(iter(tempDict))]
 index = attributes.index(root.value)
 value = entry[index]
 if(value in tempDict.keys()):
 child = Node(value, tempDict[value])
 result = tempDict[value]
 tempDict = tempDict[value]
 else:
 result = "Null"
 break
 if result != "Null":
 results.append(result == entry[-1])
 print(result)
 
if __name__ == "__main__":
 execute_decision_tree()

"""
    print(text)


def program5():
    text="""
import matplotlib.pyplot as plt
import numpy as np
import time
X = np.array(([2, 9], [1, 5], [3, 6]), dtype=float)
y = np.array(([92], [86], [89]), dtype=float)
X = X / np.amax(X, axis=0) # maximum of X array longitudinally
y = y / 100
# Sigmoid Function
start = time.time() # start time
def sigmoid(x):
 return 1 / (1 + np.exp(-x))
# Derivative of Sigmoid Function
def derivatives_sigmoid(x):
 return x * (1 - x)
# Variable initialization
epoch = 700 # Setting training iterations
lr = 0.1 # Setting learning rate
inputlayer_neurons = 2 # number of features in data set
hiddenlayer_neurons = 3 # number of hidden layers neurons
output_neurons = 1 # number of neurons at output layer
# weight and bias initialization
wh = np.random.uniform(size=(inputlayer_neurons, hiddenlayer_neurons))
bh = np.random.uniform(size=(1, hiddenlayer_neurons))
wout = np.random.uniform(size=(hiddenlayer_neurons, output_neurons))
bout = np.random.uniform(size=(1, output_neurons))
# draws a random range of numbers uniformly of dim x*y
for i in range(epoch):
 # Forward Propogation
 hinp1 = np.dot(X, wh)
 hinp = hinp1 + bh
 hlayer_act = sigmoid(hinp)
 outinp1 = np.dot(hlayer_act, wout)
 outinp = outinp1 + bout
 output = sigmoid(outinp)
 # Backpropagation
 EO = y - output
 outgrad = derivatives_sigmoid(output)
 d_output = EO * outgrad
 EH = d_output.dot(wout.T)
 hiddengrad = derivatives_sigmoid(hlayer_act) 
# how much hidden layer wts contributed to error
 d_hiddenlayer = EH * hiddengrad
 wout += hlayer_act.T.dot(d_output) * lr # dotproduct of nextlayererror and currentlayerop
 # bout += np.sum(d_output, axis=0,keepdims=True) *lr
 wh += X.T.dot(d_hiddenlayer) * lr
 # bh += np.sum(d_hiddenlayer, axis=0,keepdims=True) *lr
 end = time.time()
print("Input: \n" + str(X))
print("Actual Output: \n" + str(y))
print("Predicted Output: \n", output)
print("Elapsed time is {}".format(end - start))

"""
    print(text)


def program6():
    text="""
import csv
import random
import math
def loadCsv(filename):
lines = csv.reader(open(filename, "r"))
dataset = list(lines)
for i in range(len(dataset)):
dataset[i] = [float(x) for x in dataset[i]]
return dataset
def splitDataset(dataset, splitRatio):
trainSize = int(len(dataset) * splitRatio)
trainSet = []
copy = list(dataset)
while len(trainSet) < trainSize:
index = random.randrange(len(copy))
trainSet.append(copy.pop(index))
return [trainSet, copy]
def separateByClass(dataset):
separated = {}
for i in range(len(dataset)):
vector = dataset[i]
if (vector[-1] not in separated):
separated[vector[-1]] = []
separated[vector[-1]].append(vector)
return separated
def mean(numbers):
return sum(numbers)/float(len(numbers))
def stdev(numbers):
avg = mean(numbers)
variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
return math.sqrt(variance)
def summarize(dataset):
summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
del summaries[-1]
return summaries
def summarizeByClass(dataset):
separated = separateByClass(dataset)
summaries = {}
for classValue, instances in separated.items():
summaries[classValue] = summarize(instances)
return summaries
def calculateProbability(x, mean, stdev):
exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent
def calculateClassProbabilities(summaries, inputVector):
probabilities = {}
for classValue, classSummaries in summaries.items():
probabilities[classValue] = 1
for i in range(len(classSummaries)):
mean, stdev = classSummaries[i]
x = inputVector[i]
probabilities[classValue] *= calculateProbability(x, mean, stdev)
return probabilities
def predict(summaries, inputVector):
probabilities = calculateClassProbabilities(summaries, inputVector)
bestLabel, bestProb = None, -1
for classValue, probability in probabilities.items():
if bestLabel is None or probability > bestProb:
bestProb = probability
bestLabel = classValue
return bestLabel
def getPredictions(summaries, testSet):
predictions = []
for i in range(len(testSet)):
result = predict(summaries, testSet[i])
predictions.append(result)
return predictions
def getAccuracy(testSet, predictions):
correct = 0
for i in range(len(testSet)):
if testSet[i][-1] == predictions[i]:
correct += 1
return (float(correct)/float(len(testSet))) * 100.0
def main():
filename = 'NaiveBayesDiabetes.csv'
dataset = loadCsv(filename)
trainingSet=dataset
testSet=loadCsv('NaiveBayesDiabetes1.csv')
print('Records in training data={1} and test data={2} rows'.format(len(dataset), 
len(trainingSet), len(testSet)))
# prepare model
summaries = summarizeByClass(trainingSet)
# test model
predictions = getPredictions(summaries, testSet)
print(predictions)
accuracy = getAccuracy(testSet, predictions)
print("Accuracy:",accuracy,"%")
main()

"""
    print(text)

def program7():
    text="""
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
# import some data to play with
iris = datasets.load_iris()
X = pd.DataFrame(iris.data)
X.columns = ['Sepal_Length','Sepal_Width','Petal_Length','Petal_Width']
y = pd.DataFrame(iris.target)
y.columns = ['Targets']
# Build the K Means Model
model = KMeans(n_clusters=3)
# model.labels_ : Gives cluster no for which samples belongs to
model.fit(X) 
# Visualise the clustering results
plt.figure(figsize=(14,14))
colormap = np.array(['red', 'lime', 'black'])
# Plot the Original Classifications using Petal features
plt.subplot(2, 2, 1)
plt.scatter(X.Petal_Length, X.Petal_Width, c=colormap[y.Targets], s=40)
plt.title('Real Clusters')
plt.xlabel('Petal Length')
plt.ylabel('Petal Width')
plt.show()
# Plot the Models Classifications
plt.figure(figsize=(14,14))
plt.subplot(2, 2, 2)
plt.scatter(X.Petal_Length, X.Petal_Width, c=colormap[model.labels_], s=40)
plt.title('K-Means Clustering')
plt.xlabel('Petal Length')
plt.ylabel('Petal Width')
plt.show()
# General EM for GMM
from sklearn import preprocessing
# transform your data such that its distribution will have a
# mean value 0 and standard deviation of 1.
scaler = preprocessing.StandardScaler()
scaler.fit(X)
xsa = scaler.transform(X)
xs = pd.DataFrame(xsa, columns = X.columns)
from sklearn.mixture import GaussianMixture
gmm = GaussianMixture(n_components=3)
gmm.fit(xs)
gmm_y = gmm.predict(xs)
plt.figure(figsize=(14,14))
plt.subplot(2, 2, 3)
plt.scatter(X.Petal_Length, X.Petal_Width, c=colormap[gmm_y], s=40)
plt.title('GMM Clustering')
plt.xlabel('Petal Length')
plt.ylabel('Petal Width')
plt.show()
print('Observation: The GMM using EM algorithm based clustering matched the true labels more 
closely than the Kmeans.')

"""

    print(text)


def program8():
    text="""
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets
# Load dataset
iris=datasets.load_iris()
print("Iris Data set loaded...")
# Split the data into train and test samples
x_train, x_test, y_train, y_test = train_test_split(iris.data,iris.target,test_size=0.1)
print("Dataset is split into training and testing...")
print("Size of trainng data and its label",x_train.shape,y_train.shape)
print("Size of trainng data and its label",x_test.shape, y_test.shape)
# Prints Label no. and their names
for i in range(len(iris.target_names)):
 print("Label", i , "-",str(iris.target_names[i]))
# Create object of KNN classifier
classifier = KNeighborsClassifier(n_neighbors=1)
# Perform Training
classifier.fit(x_train, y_train)
# Perform testing
y_pred=classifier.predict(x_test)
# Display the results
print("Results of Classification using K-nn with K=1 ")
for r in range(0,len(x_test)):
 print(" Sample:", str(x_test[r]), " Actual-label:", str(y_test[r]), " Predicted-label:",
str(y_pred[r]))
print("Classification Accuracy :" , classifier.score(x_test,y_test));
from sklearn.metrics import classification_report, confusion_matrix
print('Confusion Matrix')
print(confusion_matrix(y_test,y_pred))
print('Accuracy Metrics')
print(classification_report(y_test,y_pred))

"""
    print(text)


def program9():
    text="""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
def kernel(point,xmat, k):
 m,n = np.shape(xmat)
 weights = np.mat(np.eye((m))) # eye - identity matrix
 for j in range(m):
 diff = point - X[j]
 weights[j,j] = np.exp(diff*diff.T/(-2.0*k**2))
 return weights
def localWeight(point,xmat,ymat,k):
 wei = kernel(point,xmat,k)
 W = (X.T*(wei*X)).I*(X.T*(wei*ymat.T))
 return W
def localWeightRegression(xmat,ymat,k):
 m,n = np.shape(xmat)
 ypred = np.zeros(m)
 for i in range(m):
 ypred[i] = xmat[i]*localWeight(xmat[i],xmat,ymat,k)
 return ypred
def graphPlot(X,ypred):
 sortindex = X[:,1].argsort(0) #argsort - index of the smallest
 xsort = X[sortindex][:,0]
 fig = plt.figure()
 ax = fig.add_subplot(1,1,1)
 ax.scatter(bill,tip, color='green')
 ax.plot(xsort[:,1],ypred[sortindex], color = 'red', linewidth=5)
 plt.xlabel('Total bill')
 plt.ylabel('Tip')
 plt.show();
# load data points
data = pd.read_csv('Program9_dataset_tips.csv')
bill = np.array(data.total_bill) # We use only Bill amount and Tips data
tip = np.array(data.tip)
mbill = np.mat(bill) # .mat will convert nd array is converted in 2D array
mtip = np.mat(tip)
m= np.shape(mbill)[1]
one = np.mat(np.ones(m))
X = np.hstack((one.T,mbill.T)) # 244 rows, 2 cols
# increase k to get smooth curves
ypred = localWeightRegression(X,mtip,9)
graphPlot(X,ypred)

"""

    print(text)