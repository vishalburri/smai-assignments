import numpy
import sys
from sklearn.linear_model import Ridge
file1 = sys.argv[1]
file2 = sys.argv[2]
raw_data1 = open(file1,'rt')
data1 = numpy.loadtxt(raw_data1,delimiter=",")
raw_data2 = open(file2,'rt')
data2 = numpy.loadtxt(raw_data2,delimiter=",")

X1 = numpy.copy(data1[:,0:data1.shape[1]-1])
y1= data1[:,data1.shape[1]-1:]
X2 = numpy.copy(data2[:,0:data2.shape[1]])
model = Ridge( alpha=0.01,normalize=False)
final = model.fit(X1,y1.ravel()).predict(X2)	
count=0
for i in range(final.shape[0]):
	if final[i]>0.5:
		final[i]=1
	else:
		final[i]=0
	print int(final[i])
