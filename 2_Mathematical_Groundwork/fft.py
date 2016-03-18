#!/usr/bin/env python

#todo:
#ditrad4
#difrad4
#allow non-N lists
#streaming FFTs
#in place FFT to reduce memory usage

import cmath
from numpy import fft

def ditrad2(x,N):
    """DIT radix-2 FFT
    x: list of N values to perform FFT on, can be real or imaginary
    N: int, a power of 2 number, i.e. N=2^m"""
    #copy list so the input list is not modified
    ox=x[:]
    #base case
    if N==1: return ox
    even=ditrad2(ox[0:N:2],N/2)    #Perform A DIT FFT of size N/2 on the first half of the values
    odd=ditrad2(ox[1:N:2],N/2)    #Perform A DIT FFT of size N/2 on the second half of the values
    #Perform buttefly operations to integrate N/2 FFTs into a N FFT
    for k in range(N/2):
        ox[k]=even[k]+cmath.exp(-2.j*cmath.pi*k/N)*odd[k]
        ox[k+(N/2)]=even[k]-cmath.exp(-2.j*cmath.pi*k/N)*odd[k]
    return ox

def difrad2(x,N):
    """DIF radix-2 FFT
    x: list of N values to perform FFT on, can be real or imaginary
    N: int, a power of 2 number, i.e. N=2^m"""
    #copy list so the input list is not modified
    ox=x[:]
    #base case
    if N==1: return ox
    #Perform buttefly operations on size N FFT before recursing down to N/2 FFTs
    for k in range(N/2):
        ox[k]=x[k]+x[k+(N/2)]   #the first half is the sum, no twiddles factors
        ox[k+(N/2)]=(x[k]-x[k+(N/2)])*cmath.exp(-2.j*cmath.pi*k/N) #the twiddle factor is applied to the difference
    even=difrad2(ox[:N/2],N/2)    #Perform A DIT FFT of size N/2 on the first half of the values
    odd=difrad2(ox[N/2:],N/2)    #Perform A DIT FFT of size N/2 on the second half of the values
    #interleave the outputs of the N/2 FFTs
    return [val for pair in zip(even,odd) for val in pair]

def testfft(x):
    N = len(x)
    if N <= 1: return x
    even = testfft(x[0::2])
    odd =  testfft(x[1::2])
    return [even[k] + cmath.exp(-2j*cmath.pi*k/N)*odd[k] for k in xrange(N/2)] + [even[k] - cmath.exp(-2j*cmath.pi*k/N)*odd[k] for k in xrange(N/2)]

if __name__ == "__main__":
    y=[10., 5., 2., 0.2, 1.3, 1.2, 1.6, 2.8]
    #y=[1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]

    print y
    print testfft(y)
    print fft.fft(y)
    print ditrad2(y,8)
    print difrad2(y,8)
    print y

