import math
import pandas as pd
import numpy as np

#imports
url = 'https://github.com/rosenfa/ai/blob/master/mytrain.csv?raw=true'
train_data = np.array(pd.read_csv(url,  header=0, error_bad_lines=False))
url = 'https://github.com/rosenfa/ai/blob/master/mytest.csv?raw=true'
test_data = np.array(pd.read_csv(url,  header=0, error_bad_lines=False))

#calculate euclidean distance, given 2 points
def euclideanDistance(instance1, instance2, length):
   distance = 0
   for x in range(length):
         num1=float(instance1[x])
         num2=float(instance2[x])
         distance = distance + pow(num1-num2, 2)
   return math.sqrt(distance)

#calculate hamming distance, given 2 points
def hammingDistance(instance1, instance2, length):
  distance = 0
  for x in range(length):
        num1=float(instance1[x])
        num2=float(instance2[x])
        if num2 != num1:
          distance += 1
  return distance

#calculate manhattan distance, given 2 points
def manhattanDistance(instance1, instance2, length):
   distance = 0
   for x in range(length):
         num1=float(instance1[x])
         num2=float(instance2[x])
         distance = distance + abs(num1-num2)
   return math.sqrt(distance)

#Given a list of distances and a value of k, determine if the given point is M or F
def prediction(distances, k):
  distances.sort(key=lambda x: x.dist) 
  m = 0
  f = 0
  for i in range(k):
    if distances[i].tag == 'M':
      m+=1
    else:
      f+=1
  if m > f:
    return 'M'
  else:
    return 'F'
    
class distClass:
    dist = -1 #distance of current point from test point
    tag = '-' #tag of current point

#Runner function to compete all distances for a given value of k
def compute(k):
  #Number of correct predictions for each distance function
  correct_euc = 0
  correct_ham = 0
  correct_man = 0

  #For each point in the test data, create a list of distances for every point in train data
  for i in test_data:

    eucDistances = []
    hamDistances = []
    manDistances = [] 

    for j in train_data:

      label=j[-1]

      #Compute distances
      d_euc=euclideanDistance(i,j,29)
      d_ham=hammingDistance(i,j,29)
      d_man=manhattanDistance(i,j,29)

      #Instantiate objects
      obj_euc = distClass()
      obj_euc.dist=d_euc
      obj_euc.tag=label
      obj_ham = distClass()
      obj_ham.dist=d_ham
      obj_ham.tag=label
      obj_man = distClass()
      obj_man.dist=d_man
      obj_man.tag=label

      #Add objects representing distances for this point to the list of all distances
      eucDistances.append(obj_euc)
      hamDistances.append(obj_ham)
      manDistances.append(obj_man)

    #Given the complete list of distances for a test point, make a class prediction, for a value of k
    res_euc = prediction(eucDistances, k)
    res_ham = prediction(hamDistances, k)
    res_man = prediction(manDistances, k)

    #If the prediction made was correct, add to total
    if res_euc == i[-1]:
      correct_euc += 1
    if res_ham == i[-1]:
      correct_ham += 1
    if res_man == i[-1]:
      correct_man += 1

  #Calculate accuracy based on total correct predictions from all test points
  accuracy_euc = correct_euc /100
  accuracy_ham = correct_ham /100
  accuracy_man = correct_man /100
  return accuracy_euc, accuracy_ham, accuracy_man

#Print results
print('euclidean, hamming and manhattan distances for k=1, respectively:')
print(compute(1))
print('\neuclidean, hamming and manhattan distances for k=7, respectively:')
print(compute(7))
print('\neuclidean, hamming and manhattan distances for k=15, respectively:')
print(compute(15))

#Results for k=1, k=7, and k=15, respectively
#Euclidean: .5,.74, .7
#Hamming: .61, .55, .57
#Manhattan: .61, .63, .69