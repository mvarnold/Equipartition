"""Distribution Generator

Description:
	Generates 2-d distributions for Cart.c

Usage:
  dist_gen.py [--n=<N>]

  3dxy.py 	  -h | --help 

Options:
  -h --help                         Show this screen.

  -N <n>							Number of Points

  --dist_type=<dist>
"""

# Michael Arnold
# 10/10/17
import scipy.special as sp
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.datasets import load_breast_cancer as bc
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from scipy.stats import gaussian_kde
import docopt
import sys,os
sys.setrecursionlimit(10000)


def process_args(args):
	'''process all command line arguments and return relevant values.'''
	n = int(args['--n'])

	return n


def find_density(p_x,dimx,dimy,pixel_gap):
	'''finds spatial density in grid'''
	ave_density = np.average(p_x)
	return ave_density

def generate_array(p_x,dimx,dimy,pixel_gap,ave_density):
	'''make array of data in correct dimensions to feed to cart.c'''
	data = np.ones([dimx,dimy])
	data *= ave_density
	for i,x in enumerate(p_x):
		for j,y in enumerate(x):
			data[i+pixel_gap,j+pixel_gap] = y
	return data

def output_data(data,filename):
	'''Setup the output file and return for writing.'''
	

	np.savetxt('cart-1.2.2/'+filename,data,fmt='%10.8f')
	return

n = process_args(docopt.docopt(__doc__))
dimx,dimy = n,n ##### maybe take this from command line
pixel_gap = int(n/3)

def main():
	# Get command line arguments
	
	
	n = process_args(docopt.docopt(__doc__))

	filename = str(dimx)+str(dimy)+'bc.dat'

	# Blatantly copy Dave's ipynb
	X, Y = bc(return_X_y=True)
	

	scaler = StandardScaler()
	X_tr = scaler.fit_transform(X)
	pca = PCA(n_components=2)
	pca.fit(X_tr)
	
	X_2d = pca.transform(X_tr)
	x = X_2d[:,0]
	y = X_2d[:,1]
	kernel = gaussian_kde(X_2d.T)


	xmin, xmax = min(X_2d[:,0]), max(X_2d[:,0])
	ymin, ymax = min(X_2d[:,1]), max(X_2d[:,1])



	nx = dimx-(2*pixel_gap)
	xx, yy = np.mgrid[xmin:xmax:np.complex(0,nx), ymin:ymax:np.complex(0,nx)]
	
	pos = np.vstack([xx.ravel(), yy.ravel()])
	p_x = np.reshape(kernel(pos), xx.shape)
	p_x = np.fliplr(np.rot90(p_x,k=3))
	# end blatant copy

	x *= 1/(np.max(x)-np.min(x))
	x-= np.min(x)
	x = x*(dimx-2*pixel_gap)+pixel_gap
	y *=1/(np.max(y)-np.min(y))
	y-=np.min(y)
	y = y*(dimy-2*pixel_gap)+pixel_gap
	np.savetxt('cart-1.2.2/'+'xy'+filename,np.c_[x,y],fmt='%10.8f %10.8f')
	ave_density = find_density(p_x,dimx,dimy,pixel_gap)
	
	#np.savetxt('cart-1.2.2/'+'H'+filename,np.c_[x,y],fmt='%10.8f %10.8f')
	data = generate_array(p_x,dimx,dimy,pixel_gap,ave_density)
	output_data(data,filename)

	# plot things
	plt.plot(x,y,'.')
	#plt.xlim([0,10])
	#plt.ylim([0,10])
	plt.show()

if __name__ == '__main__':
    main()