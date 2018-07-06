#!/bin/sh
cat cart-1.2.2/bc0.dat | ./interp 2000 2000 bcout.dat > cart-1.2.2/bcout0.dat
cat cart-1.2.2/difbc0.dat | ./interp 2000 2000 bcout.dat > cart-1.2.2/difbcout0.dat
