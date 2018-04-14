#!/bin/sh
cat HOT_gaussian0.dat | ./interp 512 512 HOT_gaussianout.dat > HOT_gaussianout0.dat
cat difHOT_gaussian0.dat | ./interp 512 512 HOT_gaussianout.dat > difHOT_gaussianout0.dat
