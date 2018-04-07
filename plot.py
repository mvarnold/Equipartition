import numpy as np
import matplotlib.pyplot as plt

def main(x):

dat = np.loadtxt('cart-1.2.2/out2.dat')
plt.plot(dat[0],dat[1])


if __name__ == '__main__':
    main( )	