import numpy 
import sys
file1 = sys.argv[1]
file2 = sys.argv[2]
raw_data=open(file1,'rt')
data=numpy.loadtxt(raw_data,delimiter=",")

raw_data2=open(file2,'rt')
data2=numpy.loadtxt(raw_data2,delimiter=",")
val1=[]
val2=[]
for row in data:
	val1.append(row[0])
	row[0]=1
for row in data2:
	val2.append(row[0])
#	row[0]=1

	
datafinal=numpy.copy(data[:,0:data.shape[1]])	
def trainweights(data,lrate,epoch,b):
	weights=[0.0 for i in range(len(data[0]))]
	c=0
	while(True):
		c+=1
		toterror=0
		for i in range(data.shape[0]):
			row=datafinal[i]
			if val1[i]==0:
				row=-1*datafinal[i]
			fvalue=numpy.dot(weights,row)
			if fvalue<=b:
				weights=weights+row
				toterror=1
		
			
		if(toterror==0 or c==5000):
			break
	return weights

def calculate(weights,data,b):
	count=0
	i=0
	for row in data:
		
		fvalue=numpy.dot(weights[1:],row)+weights[0]*1
		i+=1
		if fvalue>=0:
			print 1
		else:
			print 0
		
	return count/float((data.shape[0])) * 100.0

def trainbatch(data,lrate,epoch,b):	
	weights=[0.0 for i in range(len(data[0]))]
	c=0
	while(True):
		c+=1
		count=[0]*len(data[0])
		toterror=0
		for i in range(data.shape[0]):
			row=datafinal[i]
			if val1[i]==0:
				row=-1*datafinal[i]
			fvalue=numpy.dot(weights,row)
			if(fvalue<=b):
				count=numpy.add(count,row)
				toterror=1
			
		
		if(toterror==0 or c==5000):
			break
		else:
			weights=weights+count
		
	return weights
		
			
lrate=1
epoch=100
weights = trainweights(data,lrate,epoch,0)
result = calculate(weights,data2,0.0)
weights = trainweights(data,lrate,epoch,0.5)
result=calculate(weights,data2,0.0)
weights = trainbatch(data,lrate,epoch,0.0)
result = calculate(weights,data2,0.0)
weights = trainbatch(data,lrate,epoch,0.5)
result = calculate(weights,data2,0.0)

