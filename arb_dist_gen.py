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
	else:
		print("Error: distribution not recognized")