#!/usr/bin/python

#
#	Generates random data based on PDF,
#	Uses Naive Bayes to classify them.
#
#	Author: Thiago Lima
#

import numpy as np
#import matplotlib.pylab as plt
import matplotlib.pyplot as plt

# Generates training set based on the randExp()
def genSet():
	trSet = [[0.0 for i in range (100)] for i in range(3)]
	for label in range(2):
		for i in range(50):
			tmp = np.random.random_sample()
			trSet[0][i+label*50] = (-20 - label*10) * np.log(1 - tmp)
			tmp = np.random.random_sample()
			trSet[1][i+label*50] = (-15 - label*15) * np.log(1 - tmp)
			trSet[2][i+label*50] = label+1
	return trSet

# Extracts statistics from the training set
def learn(trSet):
	# stats[label][feature][variance,mean]
	stats = [[[0.0 for i in range(2)] for i in range(3)] for i in range(2)]
	for label in range(2):
		i = label * 50
		for feat in range(2):
			stats[label][feat][0] = np.var(trSet[feat][i:i+49]) # Variance
			stats[label][feat][1] = np.mean(trSet[feat][i:i+49])# Mean
	stats[0][2][0] = stats[1][2][0] = 0.5
	return stats

# Uses the values from Cummulative Probability Density Function
def classify(trSet):
	# PCDF
	# p(k) = (-1/theta) * log(1-k)
	prob = [[0.0 for i in range(3)] for i in range(2)]
	clsf = [0.0 for i in range(100)]
	for obj in range(100):
		for label in range(2):
			# For each feature k, calculates P(k|label)
			for feat in range(2):
				k = trSet[feat][obj]
				if not feat: # feature x
					mean = 20 + label*10	# 20 for label 0, 30 for label 1
				else:
					mean = 15 + label*15	# 15 for label 0, 30 for label 1
				prob[label][feat] =  -1.0/mean * np.log(1 - k)
			# Uses Naive Bayes and just multiplies the probabilities:
			prob[label][2] = 0.5 * prob[label][0] * prob[label][1]
		clsf[obj] = 1.0 if prob[0][2] > prob[1][2] else 2.0
	return clsf

# Uses the Gaussian probability to classify the data
def classifyG(trSet,stats):
	# Gaussian:
	# p(k|c) = 1/sqrt(2pi*Var^2) ^ (-(k - Mean)^2 / 2Var^2)
	prob = [[0.0 for i in range(3)] for i in range(2)]
	clsf = [0.0 for i in range(100)]
	for obj in range(100):
		for label in range(2):
			# For each feature k, calculates P(k|label)
			for feat in range(2):
				k = trSet[feat][obj]
				mean = stats[label][feat][1]
				varsqr = stats[label][feat][0]
				power = (-(k - mean)**2.0) / (2.0*varsqr)
				base = 1.0 / np.sqrt(2.0*np.pi*varsqr)
				prob[label][feat] =  base ** power
			# Uses Naive Bayes and just multiplies the probabilities:
			prob[label][2] = 0.5 * prob[label][0] * prob[label][1]
		clsf[obj] = 1.0 if prob[0][2] > prob[1][2] else 2.0
	return clsf

# Calculates number of correctly classified objects and error
def results(trSet,clsf):
	hit1 = hit2 = 0
	for obj in range(50):
		hit1 += 1 if obj <50 and clsf[obj]==1 else 0
	acc = hit1/50.0
	print "\n# Correctly classified for Class 1: %d" % hit1
	print "# Accuracy for Class 1: %.3f\n" % acc
	for obj in range(50,100):
		hit2 += 1 if obj >=50 and clsf[obj]==2 else 0
	acc = hit2/50.0
	print "# Correctly classified for Class 2: %d" % hit2
	print "# Accuracy for Class 1: %.3f\n" % acc
	acc = (hit2+hit1)/100.0
	print "# Correctly classified: %d" % (hit2+hit1,)
	print "# Accuracy: %.3f" % acc
	print "# Error: %.3f\n" % (1-acc,)


trSet = genSet()
plt.scatter(trSet[0][:49],trSet[1][:49], marker="h",color="red")
plt.scatter(trSet[0][50:],trSet[1][50:], marker="x")
plt.show()

## Part 2 ##
clsf = classify(trSet)
print "\n### Exp PDF ###"
results(trSet,clsf)

## Part 3 ##
stats = learn(trSet)
clsf = classifyG(trSet,stats)
print "\n### Gaussian ###"
results(trSet,clsf)
