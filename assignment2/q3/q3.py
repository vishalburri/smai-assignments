from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from numpy import genfromtxt
import numpy as np


X_train = genfromtxt('notMNIST_train_data.csv', delimiter=',')
y_train = genfromtxt('notMNIST_train_labels.csv', delimiter=',')
X_test = genfromtxt('notMNIST_test_data.csv', delimiter=',')
y_test = genfromtxt('notMNIST_test_labels.csv', delimiter=',')


''' l1 regularisation '''
ski1 = LogisticRegression(penalty='l1',C=0.0001)
ski1.fit(X_train,y_train)
w1 = ski1.coef_
''' find column and row sizes for resizing '''
col_size1 = np.sqrt(len(w1[0]))
row_size1 = np.sqrt(len(w1[0]))
''' reshape w1'''
w1 = np.array(w1)
w1 = np.reshape(w1,(int(row_size1),int(col_size1)))
print w1
''' l2 regularisation '''
ski2 = LogisticRegression(penalty='l2',C=0.0001)
ski2.fit(X_train,y_train)
w2 = ski2.coef_
col_size2 = np.sqrt(len(w2[0]))
row_size2 = np.sqrt(len(w2[0]))
''' reshape w2 '''
w2 = np.array(w2)
w2 = np.reshape(w2,(int(row_size1),int(col_size1)))
print w2

plot1 = plt.subplot(1,2,1)

plot2 = plt.subplot(1,2,2)

''' plot images for l1 regularisation'''

plot1.imshow(w1,interpolation='nearest',cmap='gray')
plot1.set_title('L1 Loss')

''' plot image for l2 regularisation'''
plot2.imshow(w2,interpolation='nearest',cmap='gray')
plot2.set_title('L2 Loss')
plt.show()
