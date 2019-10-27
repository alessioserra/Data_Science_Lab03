import csv
from mlxtend.frequent_patterns import fpgrowth as fpgrowth, association_rules, apriori
import pandas as pd

# EXERCISE 1
# initialize dataset
dataset = []

with open("online_retail.csv") as file:
    for row in csv.reader(file):
        # InvoiceNo without "C"
        if "C" not in row[0]:
            temp = []
            for column in row:
                temp.append(column)
            dataset.append(temp)

# clean headers
dataset.pop(0)

# EXERCISE 2
invoices = {}

for el in dataset:
    if el[0] not in invoices.keys():
        # new list for that code, initialize with first element
        list = [el[2]]
        invoices[el[0]] = list
    else:
        # add element to the list
        if el[2] not in invoices[el[0]]:
            invoices[el[0]].append(el[2])

# EXERCISE 3
# empty matrix
pa_matrix = []

# empty Set ( Set to not have duplicates)
itemsList = set()

for code in invoices.keys():
    itemsList.update(set(invoices[code]))

# NxM Matrix
M = len(itemsList)
N = len(invoices.keys())

for rows in invoices.keys():
    # row for that InvoiceNo
    row = []

    for element in itemsList:
        if element in invoices[rows]:
            row.append(1)
        else:
            row.append(0)

    pa_matrix.append(row)

print("Computing matrix finished")
df = pd.DataFrame(data=pa_matrix, columns=itemsList)

# EXERCISE 4
fi = fpgrowth(df, 0.05)
print(len(fi))
print(fi.to_string())

# EXERCISE 5
fi2 = fpgrowth(df, 0.02)
print(len(fi2))
print(fi2.to_string())

# EXERCISE 6/7
a_r = association_rules(fi2, metric='confidence', min_threshold=0.85, support_only=False)
print("\n"+str(a_r))

# EXERCISE 8
ap = apriori(df, 0.05)
print(len(ap))
print(ap.to_string())
