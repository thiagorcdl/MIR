#!/usr/bin/python

#
#	Generates sinusoids
#	Computes DFT and compares with NumPy's FFT
#
#	Author: Thiago Lima
#

import numpy as np
import matplotlib.pylab as plt

## arr[0][bin] = real
## arr[1][bin] = img
## arr[2][bin] = x for plotting

# Creates sinusoid
def sinus(frq,amp,pha,win,sr):
	# frq == 1? 2pi/360 : frq*2pi/360
	step = frq * 2 * np.pi/sr
	angle = pha
	arr = [[ 0 for x in range(win)] for x in range(3)]
	for bi in xrange(win):
		arr[0][bi] = amp * np.cos(angle)
		arr[1][bi] = amp * np.sin(angle)
		arr[2][bi] = 0.0 + bi/sr
		angle += step
	return arr

# Calculates DFT of a matrix arr[2][window]
def dft(arr,win):
	new = [[ 0 for x in range(win)] for x in range(3)]
	for k in xrange(win):
		sumR = 0
		sumI = 0
		for x in xrange(win):
			angle = 2 * np.pi * x * k / win
			sumR += arr[0][x] * np.cos(angle) + arr[1][x] * np.sin(angle)
			sumI += -arr[0][x] * np.sin(angle)+ arr[1][x] * np.cos(angle)
		new[0][k] = sumR
		new[1][k] = sumI
		new[2][k] = arr[2][k]
	return new

# Calculates window with minimum magnitude difference
def amdf(arr,win):
	minK = 1
	sumD = [ 0 for x in range(win)]
	for off in xrange(1,win):
		for bi in xrange(win-off):
			sumD[off] += abs(arr[bi] - arr[bi+off])
		minK = minK if sumD[minK] <= sumD[off] else off
		if sumD[off] < 10**-6:
			return off
	return minK

# Combines two sinusoids
def comb(s1,s2,win):
	new = [[ 0 for x in range(win)] for x in range(3)]
	for i in xrange(win):
		new[0][i] = s1[0][i]+s2[0][i]
		new[1][i] = s1[1][i]+s2[1][i]
		new[2][i] = s1[2][i]
	return new

sr = 2.0**8
window = 2**9
sin1 = sinus(2,25.0,4.0,window,sr)
sin2 = sinus(5,13.0,0.0,window,sr)
sin3 = sinus(10,30.0,-0.5*np.pi,window,sr)
st = comb(comb(sin1,sin2,window),sin3,window) # Combined sinusoid
minK = amdf(st[1],window)
fFrq = sr/minK
print "Bin window for fundamental Frequency: %d\nFundamental Frequency: %.3fHz\n" % (minK,fFrq)

sft = dft(st,window)  			# Result of my DFT
new = [1j for x in xrange(window)] 
magMy = [0.0 for x in xrange(window)] 	# Magnitude for my result
magPy = [0.0 for x in xrange(window)] 	# Magnt for Python's result

for i in xrange(window):
	new[i] = complex(st[0][i],st[1][i])
pft = np.fft.fft(new,window)
for i in xrange(window):
	magMy[i] = np.sqrt(sft[1][i]**2 + sft[0][i]**2)/window
for i in xrange(window):
	magPy[i] = np.sqrt(pft[i].imag**2 + pft[i].real**2)/window

#plt.plot(sin1[2],sin1[1])
#plt.plot(sin2[2],sin2[1])
#plt.plot(sin3[2],sin3[1])
plt.plot(np.linspace(0,sr,window),magMy)
plt.plot(np.linspace(0,sr,window),magPy)
plt.show()
