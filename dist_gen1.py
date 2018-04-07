"""Distribution Generator

Description:
	Generates 2-d distributions for Cart.c

Usage:
  dist_gen.py [--n=<N> --dist_type=<dist>]

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
import docopt
import sys,os
sys.setrecursionlimit(10000)


def process_args(args):
	'''process all command line arguments and return relevant values.'''
	n = int(args['--n'])
	dist_type = args['--dist_type']
	

	return n,dist_type

def generate_dist(n,dist_type):
	if dist_type == 'exp':
		x = stats.expon.rvs(size = n)
		x *= 1/np.max(x)
		x =x*(dimx-2*pixel_gap)+pixel_gap
		y = stats.expon.rvs(size = n)
		y *=1/np.max(y)
		y = y*(dimy-2*pixel_gap)+pixel_gap
		return x,y
	## add distribution types
	elif dist_type == "gaussian":
		sig=10
		#x = np.sqrt(2*sig)*sp.erfinv(2*np.random.rand(n)+1)#*(dimx-2*pixel_gap)+pixel_gap
		#y = np.sqrt(2*sig)*sp.erfinv(2*np.random.rand(n)+1)#*(dimy-2*pixel_gap)+pixel_gap
		x = np.abs(stats.norm.rvs(size = n))
		x *= 1/np.max(x)
		x=x*(dimx-2*pixel_gap)+pixel_gap
		
		y = np.abs(stats.norm.rvs(size = n))
		y *=1/np.max(y)
		y = y*(dimy-2*pixel_gap)+pixel_gap
		return x,y
	else:
		print("Error: distribution not recognized")


def find_density(x,y,dimx,dimy,pixel_gap):
	'''finds spatial density in grid'''
	nx,ny = dimx-(2*pixel_gap),dimy-(2*pixel_gap) # change to be number of pixels
	H,xedges,yedges = np.histogram2d(x/np.max(x),y/np.max(y),bins=[nx,ny])
	ave_density = np.average(H)
	return H,xedges,yedges,ave_density

def generate_array(H,xedges,yedges,dimx,dimy,pixel_gap,ave_density):
	'''make array of data in correct dimensions to feed to cart.c'''
	data = np.ones([dimx,dimy])
	data *= ave_density
	for i,x in enumerate(H):
		for j,y in enumerate(x):
			data[i+pixel_gap,j+pixel_gap] = y
	return data

def output_data(data,filename):
	'''Setup the output file and return for writing.'''
	

	np.savetxt('cart-1.2.2/'+filename,data,fmt='%10.8f')


dimx,dimy = 512,512  ##### maybe take this from command line
pixel_gap = 200

def main():
	# Get command line arguments
	
	
	n,dist_type = process_args(docopt.docopt(__doc__))
	filename = str(dimx)+str(dimy)+dist_type+'.dat'
	x,y = generate_dist(n,dist_type)
	np.savetxt('cart-1.2.2/'+'xy'+filename,np.c_[x,y],fmt='%10.8f %10.8f')
	H,xedges,yedges,ave_density = find_density(x,y,dimx,dimy,pixel_gap)
	np.savetxt('cart-1.2.2/'+'H'+filename,np.c_[x,y],fmt='%10.8f %10.8f')
	data = generate_array(H,xedges,yedges,dimx,dimy,pixel_gap,ave_density)
	output_data(data,filename)

	# plot things
	plt.plot(x,y,',')
	#plt.xlim([0,10])
	#plt.ylim([0,10])
	plt.show()





if __name__ == '__main__':
    main()