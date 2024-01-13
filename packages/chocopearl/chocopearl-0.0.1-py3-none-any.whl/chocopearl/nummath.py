from numpy import sqrt
import numpy as np
import warnings


# Binomial o combinatoria de k en n
def binomial(n,k):
    """
    first parameter n
    second parameter k
    so that n>k>=0
    
    """
    if n%1!=0 or k%1!=0 or n<k or n<0 or k<0:
        warnings.warn('binomial parameters error1')
    
    else:
        binom=0
        
        if k==0 or k==n:
            binom=1
        else: 
            binom= int(binomial(n-1,k-1)*n/k)
        return binom
    
#horner
def horner(coef, x):
	'''
	coeficientes de mayor orden a menor orden
	
	'''
	xset= np.asarray(x)
	p=np.zeros(xset.shape)
	for a in coef:
		p=p*xset + a
	return p