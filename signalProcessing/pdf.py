#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

#
#	Computes PDF, invert the samples,
#	calculates mean and std deviation values.
#
#	Author: Thiago Lima
#

#	Cummulative probability density function 
#	If  y = 1-e^(-kx)  then  x = (-1/theta) * log(1-y)	#
def randExp(theta, n):
	x = np.random.random_sample(n)
	for y in xrange(n):
		x[y] = (-1/theta) * np.log(1 - x[y])
	return x

numSamples = 2 ** 10

## Part 1 ##
# Plot ePDF
samp = np.linspace(0, 99, numSamples)
before = 0.1*np.power(np.exp(1),-0.1*samp)
plt.plot(samp, before)
plt.show()

## Part 2 ##
# Inverse sampling
numSamples = 100
samp = np.linspace(0, 99, numSamples)
invSamp = randExp(0.1, numSamples)
plt.plot(samp, sorted(invSamp,reverse=True))
print "Standard deviation: %f" % np.std(invSamp)
print "Mean: %f" % (sum(invSamp)/numSamples)
plt.show()

## Part 3 ##
for p in range(4,1,-1):
	numSamples = 10**p
	invSamp = randExp(0.1, numSamples)
	plt.hist(sorted(invSamp,reverse=True), normed=1,bins = 100)	
	plt.show()
