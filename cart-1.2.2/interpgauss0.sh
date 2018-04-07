#!/bin/sh
cat gauss0.dat | ./interp 512 512 gaussout.dat > gaussout0.dat
cat difgauss0.dat | ./interp 512 512 gaussout.dat > difgaussout0.dat
