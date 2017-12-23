import numpy 
import sys
file1 = sys.argv[1]
file2 = sys.argv[2]
data=numpy.genfromtxt(file1,delimiter=',',dtype=int)
data2=numpy.genfromtxt(file2,delimiter=',',dtype=int)
datalabel=[]
for row in data:
	row[0]=1
datafinal=numpy.copy(data[:,0:data.shape[1]-1])
datalabel=data[:,data.shape[1]-1:]
#datafinal=numpy.copy(data)
def trainweights(data,lrate,epoch,b):
	weights=numpy.zeros(data.shape[1]-1)
	for i in range(epoch):
		error=1
		for j in range(0,datafinal.shape[0]):
			row=datafinal[j]
			if(datalabel[j]==2):
				row=-1*datafinal[j]
			fvalue=numpy.dot(row,weights)
			if fvalue<=b:
				weights=weights+(lrate)*((b-fvalue)/numpy.dot(row,row))*row
				error=0
		if error==1:
			break
	return weights
def trainweights1(data,lrate,epoch,b):
	weights=numpy.zeros(data.shape[1]-1)
	for i in range(epoch):
		error=1
		for j in range(0,datafinal.shape[0]):
			row=datafinal[j]
			if(datalabel[j]==2):
				row=-1*datafinal[j]
			fvalue=numpy.dot(row,weights)
			if fvalue<=b:
				weights=weights+(1.0/(i+1))*((b-fvalue)/numpy.dot(row,row))*row
				error=0
		if error==1:
			break
	return weights

def calculate(weights,data,b):
	count=0
	for row in data:
		row[0]=1
		fvalue=numpy.dot(weights,row[0:len(row)])
		if fvalue>=0:
			print '4'			
		elif fvalue<0 :
			print '2'
		
			
	return count
				
			
lrate=1
epoch=100
weights = trainweights(data,lrate,epoch,0.5)
result = calculate(weights,data2,0.0)
weights = trainweights1(data,lrate,epoch,0.5)
result = calculate(weights,data2,0.0)

