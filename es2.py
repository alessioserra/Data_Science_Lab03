# CODE BY Niccolò Cavagnero

import json
import timeit
import itertools

# EXERCISE 1/2/3
dataset = []
minsup = 0.09

with open("coco.json") as f:
    d = json.load(f)

itemList = []  # o build the DataFrame
for image in d:
    dataset.append(list(set(image["annotations"])))
    for annotation in set(image["annotations"]):
        itemList.append(annotation)

# Generates C1
def firstStep(dataset):
    output = set()
    for itemset in dataset:
        for item in itemset:
            if item not in output:
                output.add(item)
    return sorted(list(output))


# Generates C2
def secondStep(L1):
    return list(itertools.combinations(L1, 2))

# Return a list of itemsets, between candidates,
# whose support is > of minsup
def supPrune(dataset, candidates, minsup):
    rowList = []
    l = len(dataset)
    for candidate in candidates:
        for itemset in dataset:
            if set(candidate).issubset(itemset) or candidate in itemset:
                rowList.append(candidate)

    counter = []
    for candidate in candidates:
        counter.append((candidate, rowList.count(candidate)))
    output = [itemset for itemset, count in counter if count / l > minsup]
    supports.append([count / l for itemset, count in counter if count / l > minsup])
    return output


def aprioriPrune(frequentSets, Ck, k):
    output = []
    levelSets = []
    for ksets in frequentSets:
        for itemset in ksets:
            if len(itemset) == k - 1:
                levelSets.append(itemset)

    for candidate in Ck:
        flag = False
        for itemset in levelSets:
            if set(itemset).issubset(candidate):
                flag = True
        if flag == True:
            output.append(candidate)
    return output

def generation(Lk, k):
    output = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2];
            L2 = list(Lk[j])[:k - 2]
            L1.sort();
            L2.sort()
            if L1 == L2:  # if first k-2 elements are equal
                output.append(set(Lk[i]).union(Lk[j]))
    return output

def myApriori(dataset, minsup=0.1):
    frequentSets = []
    C1 = firstStep(dataset)
    L1 = supPrune(dataset, C1, minsup)
    L = [L1]
    C2 = secondStep(L1)
    L2 = supPrune(dataset, C2, minsup)
    L.append(L2)
    frequentSets.append(L2)
    k = 3
    while (len(L[k - 2]) > 0):
        print("Generation", k, "...")
        Ck = generation(L[k - 2], k)
        print("AprioriPruning", k, "...")
        Ck = aprioriPrune(frequentSets, Ck, k)
        print("SupPruning", k, "...")
        Lk = supPrune(dataset, Ck, minsup)
        frequentSets += Lk
        L.append(Lk)
        k += 1
    return L


supports = []
L = myApriori(dataset, minsup)
print(L)
print(supports)

# time = timeit.timeit(lambda: myApriori(dataset,minsup), number=1)
# print(time, "seconds needed for computation..")

# es4
import pandas as pd
from mlxtend.frequent_patterns import apriori

itemList = list(set(itemList))
matrix = []
for itemset in dataset:
    row = []
    for item in itemList:
        if item in itemset:
            row.append(1)
        else:
            row.append(0)
    matrix.append(row)
print("Matrix computed...")
dataFrame = pd.DataFrame(data=matrix, columns=itemList)
print("DataFrame prepared...")
# apriori = apriori(dataFrame,minsup)
print(apriori)

myAprioriTime = timeit.timeit(lambda: myApriori(dataset, minsup), number=1)
print("myApriori() computed in", myAprioriTime)
aprioriTime = timeit.timeit(lambda: apriori(dataFrame, minsup), number=1)
print("apriori() computed in", aprioriTime)