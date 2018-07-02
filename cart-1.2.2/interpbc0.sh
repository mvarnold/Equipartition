#!/bin/sh
cat /Users/Winston/Dropbox/Equipartition/cart-1.2.2/bc0.dat | ./interp 2000 2000 bcout.dat > /Users/Winston/Dropbox/Equipartition/cart-1.2.2/bcout0.dat
cat /Users/Winston/Dropbox/Equipartition/cart-1.2.2/difbc0.dat | ./interp 2000 2000 bcout.dat > /Users/Winston/Dropbox/Equipartition/cart-1.2.2/difbcout0.dat
