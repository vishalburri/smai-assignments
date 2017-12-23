#!/usr/bin/env python
import sys
import os
import numpy as np
import re

class FeatureVector(object):

	def __init__(self,vocabsize,numdata):
		self.vocabsize = vocabsize
		self.z=0
		self.X =  np.zeros((numdata,self.vocabsize), dtype=np.int)
		self.Y =  np.zeros((numdata,), dtype=np.int)
		self.n=0

	def make_featurevector(self, input, classid):
		for j in input:
			''' split by space '''
			for i in j.split(' '):
				flag=1
				if i in word:
					self.X[self.n][word[i]]+=1
				else:
					self.X[self.n][word['UNK']]+=1

		self.Y[self.n]=classid
		self.n=self.n+1

class KNN(object):

	def __init__(self,trainVec,testVec):

		self.X_train = trainVec.X
		self.z=0
		self.Y_train = trainVec.Y
		self.X_test = testVec.X
		self.Y_test = testVec.Y
		
		self.metric = Metrics('accuracy')

	def classify(self, nn=1):

		final =['galsworthy','galsworthy_2','mill','shelley','thackerey','thackerey_2','wordsmith_prose','cia','johnfranklinjameson','diplomaticcorr']
	
		for i in range(self.X_test.shape[0]):
			""" find first k elements in sorted order"""
			dist_list=[]
			for j in range(self.X_train.shape[0]):	
				""" euclidien distance for each vector"""
				dist=np.linalg.norm(self.X_test[i]-self.X_train[j])
				dist_list.append((j,dist))

			dist_list=sorted(dist_list,key=lambda x:x[1])
			k=5
			'''sort and find most repeated author'''
			output=[self.Y_train[dist_list[j][0]] for j in range(k)]
			predicted=max(set(output),key=output.count)
			print final[predicted-1]
				


class Metrics(object):
	def __init__(self,metric):
		self.metric = metric

	def score(self):
		if self.metric == 'accuracy':
			return self.accuracy()
		elif self.metric == 'f1':
			return self.f1_score()

	def get_confmatrix(self,y_pred,y_test):
		return
	def accuracy(self):
		return

	def f1_score(self):
		return

if __name__ == '__main__':

#	datadir = './datasets/q4/'
	traindir = sys.argv[1]
	testdir = sys.argv[2]
	classes =['galsworthy/','galsworthy_2/','mill/','shelley/','thackerey/','thackerey_2/','wordsmith_prose/','cia/','johnfranklinjameson/','diplomaticcorr/']
	inputdir = [traindir,testdir]
	
	trainsize=0
	testsize=0
	word={}
	ind=0
	for cl in classes:
		listing=os.listdir(traindir+cl)
		'''store words in a dictionary'''
		for fn in listing:
			trainsize+=1
			f = open(traindir+cl+fn,'r')
			f=f.read()
			'''regex for removing tags'''
			l=re.findall('<s>(.+)<\\\\s>',f)
			l = [re.sub('[^a-zA-Z ]',' ',line) for line in l]
			for line in l:
				'''store each word in dictionary'''
				for j in line.split(' '):

					if j not in word:
						word[j]=ind
						ind+=1

	word['UNK']=ind
	vocabsize=len(word)
	
	for cl in classes:
		"""find test data size"""
		lis=os.listdir(testdir+cl)
		for fn in lis:
			'''increment testsize'''
			testsize=testsize+1
	
	trainVec = FeatureVector(vocabsize, trainsize)
	testVec = FeatureVector(vocabsize,testsize)
	for idir in inputdir:
		classid = 1
		for c in classes:
			listing = os.listdir(idir+c)
			for filename in listing:
				f = open(idir+c+filename,'r')
				'''regex for removing tags'''
				lines = re.findall('<s>(.*)<\\\\s>', f.read())
				'''remove , '''
				lines = [re.sub('[^a-zA-Z ]',' ',line) for line in lines]	
				if len(lines) ==0:
					continue
				if idir == traindir:
					trainVec.make_featurevector(lines,classid)
				else:
					testVec.make_featurevector(lines,classid)
			classid += 1
	knn = KNN(trainVec,testVec)
	knn.classify()
