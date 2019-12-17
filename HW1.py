import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE
import pylab
import numpy as np
import math

########################## Question 1 ##############################
#  creates a bag of words from the csv file given and runs the TSNE function to see the results.

corpus=list()

with open("items.csv") as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        corpus.append(row[0])


vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)
X= TSNE(n_components=2).fit_transform(X.toarray())
pylab.scatter(X[:, 0], X[:, 1], 1)
pylab.show()

########################## Question 2.a ##############################
#   builds a matrix which shows how often two ideas are placed in the same cluster
#
#
matrix_x = np.zeros((10, 10))

with open("matrix_assignment.csv") as f:
    next(f)
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        for m in range(0, 10):
            for k in range(0, m):
                for i in range(1, len(row)):
                    x = eval(row[i])
                    if m+1 in x and k+1 in x:
                        matrix_x[m, k] = matrix_x[m,k]+1

########################## Question 2.b ##############################
#  for input idea ID, gives output the idea which is most similar and the idea which is most different
#

idea = input("Type your idea ID: ")
print(idea)
min = math.inf
max=0
min_index=0
max_index=0

for j in range(0,int(idea)-1):
    if matrix_x[int(idea)-1][j]<min:
        min=matrix_x[int(idea)-1][j]
        min_index=j+1
    if matrix_x[int(idea)-1][j]>max:
        max=matrix_x[int(idea)-1][j]
        max_index=j+1
for j in range(int(idea),10):
    if matrix_x[j][int(idea)-1]<min:
        min=matrix_x[j][int(idea)-1]
        min_index=j+1
    if matrix_x[j][int(idea)-1]>max:
        max=matrix_x[j][int(idea)-1]
        max_index=j+1

print('Most Similar Idea: ' ,max_index)
print("Most Different Idea: ",min_index)


