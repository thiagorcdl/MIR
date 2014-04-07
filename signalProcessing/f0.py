#!/usr/bin/python

#
#	Computes magnitude spectrum to find fundamental frequency
#
#	Author: Thiago Lima
#

import numpy as np
import matplotlib.pylab as plt
import scipy.io.wavfile as wv

(samprate,wave)= wv.read("qbh_examples.wav")
sampsize = wave.size
samprate = 22050
magnt = [0.0 for x in xrange(sampsize)] 
window = 2**10
nWin = int(np.ceil(sampsize/float(window))) # windows to cover half spectr
bins = [0 for x in xrange(nWin)] 	# Bins with peak for each window
freq = [0.0 for x in xrange(sampsize)] 	# Frq with peak for each window
fb = np.linspace(0,samprate,window)
wft = []

for win in xrange(nWin):
	thisW = win*window
	bins[win] = thisW
	# Calculates FFT for window
	wft.extend(np.fft.fft(wave[thisW:thisW+window],window))
	for f in xrange(window):
		this = thisW+f
		# Gets magnitude
		magnt[this] = np.sqrt(wft[this].imag**2 + wft[this].real**2)/sampsize
		# Compares peaks
		bins[win] = this if magnt[this] > magnt[bins[win]] else bins[win]
	#Assigns freq related to the peak to everyone in window	
	for f in xrange(window):
		this = thisW+f
		freq[this] = fb[bins[win]-thisW]
	#print "F0 candidate for window %d: %.3f" % (win,fb[bins[win]-thisW])

#plt.plot(np.linspace(0,samprate,sampsize),magnt)
#plt.show()
plt.plot(np.linspace(0,40,sampsize),freq)
plt.show()
