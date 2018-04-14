"""Distribution Generator

Description:
	Generates 2-d distributions for Cart.c

Usage:
  dist_gen.py [--n=<N> --dist_type=<dist> --dimx=<dx> --dimy=<dy> --pixel=<pixel> --plot=<plot>]

  3dxy.py 	  -h | --help 

Options:
  -h --help                         Show this screen.
  -N <N> --n=<N>                    Number of Points [default: 50000]
  -d <dist> --dist_type=<dist>      Distribution Type [default: exp]
  -x <dx> --dimx=<dx>               Number of Pixels in x dimension
                                    [default: 1024]
  -y <dy> --dimy=<dy>               Number of Pixels in x dimension
                                    [default: 1024]
  -p <pixel> --pixel=<pixel>        Pixel Gap for partition [default: 300]
  -P <plot> --plot =<plot>          Display figure [default: True]
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
	global dimx
	global dimy
	global pixel_gap
	'''process all command line arguments and return relevant values.'''
	n = int(args['--n'])
	dist_type = args['--dist_type']
	dimx = int(args['--dimx'])
	dimy = int(args['--dimy'])
	pixel_gap= int(args['--pixel'])
	plot = args['--plot']
	print(plot)
	return n,dist_type,dimx,dimy,pixel_gap,plot

def hot_firebreaks(max_x,max_y):
	""" Create data file for firebreak xy position"""
	HOT = np.genfromtxt("optimal_forests/optimal_forest_L64_DL.csv",delimiter=",")
	
	HOT_data= np.zeros([1,2])
	for i,x in enumerate(HOT):
	    for j,y in enumerate(x):
	        if y==0:
	            HOT_data = np.append(HOT_data,np.array([[i,j]]),axis=0)
	HOT_data=HOT_data[1:,:]
	x = HOT_data[:,0]
	y = HOT_data[:,1]
	x *= 1/64
	x = x*(dimx-2*pixel_gap)+pixel_gap
	y *=1/64
	y = y*(dimy-2*pixel_gap)+pixel_gap
	np.savetxt('cart-1.2.2/'+'xy'+str(dimx)+str(dimy)+'hot1.dat',np.c_[x,y],fmt='%10.8f %10.8f')
	return

def generate_dist(n,dist_type):

	if dist_type == 'exp':
		x = stats.expon.rvs(size = n)
		x *= 1/np.max(x)
		x=x*(dimx-2*pixel_gap)+pixel_gap
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
	elif dist_type == "hot":
		sig=10
		#x = np.sqrt(2*sig)*sp.erfinv(2*np.random.rand(n)+1)#*(dimx-2*pixel_gap)+pixel_gap
		#y = np.sqrt(2*sig)*sp.erfinv(2*np.random.rand(n)+1)#*(dimy-2*pixel_gap)+pixel_gap
		
		x = np.abs(stats.norm.rvs(size = n,scale=64))
		max_x=np.max(x)
		x *= 1/np.max(x)
		x=x*(dimx-2*pixel_gap)+pixel_gap
		
		y = np.abs(stats.norm.rvs(size = n,scale=64))
		max_y=np.max(y)
		y *=1/np.max(y)
		y = y*(dimy-2*pixel_gap)+pixel_gap

		hot_firebreaks(max_x,max_y)
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

  ##### maybe take this from command line

def main():
	# Get command line arguments
	n,dist_type,dimx,dimy,pixel_gap,plot = process_args(docopt.docopt(__doc__))
	print(n,dist_type)
	filename = str(dimx)+str(dimy)+dist_type+'.dat'
	x,y = generate_dist(n,dist_type)
	np.savetxt('cart-1.2.2/'+'xy'+filename,np.c_[x,y],fmt='%10.8f %10.8f')
	H,xedges,yedges,ave_density = find_density(x,y,dimx,dimy,pixel_gap)
	np.savetxt('cart-1.2.2/'+'H'+filename,np.c_[x,y],fmt='%10.8f %10.8f')
	data = generate_array(H,xedges,yedges,dimx,dimy,pixel_gap,ave_density)
	output_data(data,filename)
	print('Data file created in directory cart-1.2.1/'+filename)

	# plot things

	if plot == 'True':
		plt.plot(x,y,',')
		#plt.xlim([0,10])
		#plt.ylim([0,10])
		plt.show()





if __name__ == '__main__':
    main()