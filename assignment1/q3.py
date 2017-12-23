import sys
import math as m
file1=sys.argv[1]
file2=sys.argv[2]
data2=[]
labels2=[]
input1 = open(file1).read().split('\n')
input2 = open(file2).read().split('\n')
data = []
labels = []
#split by newline
def commasplit(data,input1,labels):
	for i in input1:
		flag=0
		tlist = []
		l = 0
		'''split by ,'''
		splitline = i.split(',')
		for j in range(len(splitline)):
			'''get label'''
			if j == 6:
				l = splitline[j]
			else:
				'''append to list'''
				tlist.append(splitline[j])
		data.append(tlist)
		labels.append(l)
commasplit(data,input1,labels)
del(data[11251])	
data = data[1:]
labels = labels[1:]

def convert(data):
	for row in data:
		l1 = len(data[0])-1
		l2 = len(data[0])-2
		'''assign values to strings'''
		if(row[l1]=='low'):
			row[l1]='0'
		elif row[l1]=='medium':
			row[l1]='1'
		elif row[l1]=='high':
			row[l1]='2'
		if row[l2]=='marketing':
			row[l2]='0'
		elif row[l2]=='IT':
			row[l2]='1'
		elif row[l2]=='hr':
			row[l2]='2'
		elif row[l2]=='technical':
			row[l2]='3'
		elif row[l2]=='support':
			row[l2]='4'
		elif row[l2]=='management':
			row[l2]='5'
		elif row[l2]=='sales':
			row[l2]='6'
		elif row[l2]=='product_mng':
			row[l2]='7'
		elif row[l2]=='accounting':
			row[l2]='8'
		elif row[l2]=='RandD':
			row[l2]='9'

convert(data)
'''append labels to data'''
for i in range(len(data)):
	data[i].append(labels[i])

'''convert to float'''
for row in range(len(data)):
	for i in range(len(data[row])):
		data[row][i]=float(data[row][i])

'''commasplit2(data2,input2,labels2)'''
for i in input2:
	tlist = []
	'''split by ,'''
	splitline = i.split(',')
	for j in range(len(splitline)):
		'''append to list'''
		tlist.append(splitline[j])
	data2.append(tlist)

del(data2[len(data2)-1])
data2 = data2[1:]
def convert2(data):	
	for row in data:
		l1 = len(data[0])-1
		l2 = len(data[0])-2
		'''assign values to strings'''
		if(row[l1]=='low\r'):
			row[l1]='0'
		elif row[l1]=='medium\r':
			row[l1]='1'
		elif row[l1]=='high\r':
			row[l1]='2'
		if row[l2]=='marketing':
			row[l2]='0'
		elif row[l2]=='IT':
			row[l2]='1'
		elif row[l2]=='hr':
			row[l2]='2'
		elif row[l2]=='technical':
			row[l2]='3'
		elif row[l2]=='support':
			row[l2]='4'
		elif row[l2]=='management':
			row[l2]='5'
		elif row[l2]=='sales':
			row[l2]='6'
		elif row[l2]=='product_mng':
			row[l2]='7'
		elif row[l2]=='accounting':
			row[l2]='8'
		elif row[l2]=='RandD':
			row[l2]='9'

convert2(data2)
'''convert to float'''		
for row in range(len(data2)):
	for i in range(len(data2[row])):
		'''convert to float'''
		data2[row][i]=float(data2[row][i])

unique=[]
'''get unique elements in a column'''
for i in range(len(data[0])-1):
	temp1=set([row[i] for row in data])
	unique.append(temp1)

def calentropy(groups):
	entropy=0.0
	size=len(groups[0])+len(groups[1])

	for group in groups:
		l0=0
		l1=0
		for row in group:
			if row[-1]==0:
				l0+=1
			elif row[-1]==1:
				l1+=1
		p=l0+l1
		if l0==0 or l1==0:
			entropy=entropy+0
		else:
			p1=(l0*1.0)/p
			p2=(l1*1.0)/p
			entropy+=(len(group)*1.0/size)*(-p1*(m.log(p1,2))-p2*(m.log(p2,2)))
	return entropy		
					
def nodesplit(index,val,data):
	left=[]
	right=[]
	flag=0
	'''  discrete vs continuous data '''
	for row in data:
		if index==0 or index==1 or index==3:
			flag=1
			''' append to left'''
			if(row[index]<=val):
				fl=1
				left.append(row)
			else:
				''' append to right'''
				fl=-1
				right.append(row)
		else:
			flag=0
			'''discrete append to left'''
			if row[index]==val:
				fl=1
				left.append(row)
			else:
				'''append to right'''
				fl=-1
				right.append(row)
	return left,right


def getnode(data):
	escore=1000
	egroups=None
	eindex=1000
	evalue=1000

	for i in range(len(data[0])-1):
		value=unique[i]
		for j in value:
			'''get groups split by value'''
			groups=nodesplit(i,j,data)
			entropy=calentropy(groups)
			'''update entropy'''
			if entropy < escore:
				escore=entropy
				egroups=groups
				eindex=i
				evalue=j
	return {'index':eindex,'value':evalue,'groups':egroups}

def build(data,depth,nrows):
	'''build tree'''
	root = getnode(data)
	split(root,depth,nrows,1)
	return root

def split(node,depth,nrows,d):
	'''test'''
	left = node['groups'][0]
	right = node['groups'][1]
	flag=0
	del(node['groups'])
	if not left or not right:
		'''test'''
		flag=1
		node['left']=terminal(left+right)
		node['right']=node['left']
		return
	if d>=depth:
		'''test'''
		flag=1
		node['left']=terminal(left)
		node['right']=terminal(right)
		return
	if len(left) <= nrows:
		flag=1
		node['left'] = terminal(left)
	else:
		flag=0
		node['left'] = getnode(left)
		split(node['left'],depth,nrows,d+1)
	if len(right) <= nrows:
		flag=1
		node['right'] = terminal(right)
	else:
		flag=0
		node['right'] = getnode(right)
		split(node['right'],depth,nrows,d+1)

def terminal(group):
	''' get label '''	
	output = [row[-1] for row in group]
	'''get most occurent value'''
	return max(set(output),key = output.count)


def predict(node,row):
	''' for continus data'''
	if node['index']==0 or node['index']==1 or node['index']==3:
		flag=1
		if row[node['index']] <= node['value']:
			if isinstance(node['left'], dict):
				return predict(node['left'], row)
			else:
				flag=-1
				return node['left']
		else:
			flag=0
			if isinstance(node['right'], dict):
				return predict(node['right'], row)
			else:
				flag=-1
				return node['right']
	else:
		''' for discrete data '''
		if row[node['index']] == node['value']:
			flag=1
			if isinstance(node['left'], dict):
				return predict(node['left'], row)
			else:
				flag=-1
				return node['left']
		else:
			flag=0
			if isinstance(node['right'], dict):
				return predict(node['right'], row)
			else:
				flga=-1
				return node['right']
		

def calculate(data):
	count=0
	for row in data:
		#print row
		out = predict(root,row)
		print int(out)
		#if(out!=row[-1]):
		#	count+=1
	#print(count)
		
				
root=build(data,20,70)
calculate(data2)	
			

