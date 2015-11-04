# generate a set of vector data with three principal components on x, y and z axes respectively

import os, sys
lib_path = os.path.abspath(os.path.join('..', 'PcaSycData'))
sys.path.append(lib_path)

from population import Population as PopApi
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import numpy as np
import random
import time
from math import sqrt

class PcaSynthData(PopApi):

    __a = 0
    __b = 0
    __c = 0
    __N = 800        # number of vectors to generate (800 default)
    __data = None

    def __init__(self, a, b, c, N):
        PopApi.__init__(self, None)

        self.__a = a
        self.__b = b
        self.__c = c
        self.__N = N
        self.__data = self.__surface(self.__a, self.__b, self.__c, N)

        # empty argument defaults to using time for seed
        random.seed(time.time())

    """
    Equation for 'squashed' football (ellipsoid) with long axis along x, fat axis along y and squashed axis along z:
    1 = x*x/a/a + y*y/b/b + z*z/c/c, where a > b > c > 0
    """

    # synthetic allele data for three populations
    # the occurance of particular alleles are determined by the pole of an ellipsoid 
    # which is closest to a randomly chosen point on is surface.

    def __surface(self, a, b, c, n):
        """ surface generates points randomly placed on the surface of an ellipsoid """
        A2 = a*a
        B2 = b*b
        C2 = c*c

        data = []
        idx = 0
        while idx in range(0,n):
            idx += 1
            x = random.uniform(-a, a)
            xa = 1 - x*x/A2
            x2 = b * sqrt(xa)
            y = random.uniform(-x2, x2)
            z = c * sqrt(xa - y*y/B2)
            if random.uniform(-1,1) < 0 :
                z = -z
            data.append((x,y,z))
        return data

    def __synthesizeData(self):
        """ generate snps from ellipsoid data """

        try:
            self._snpnames.append('01')
            self._snpnames.append('02')
            self._snpnames.append('03')

            idx = 0
            fishies = []

            for point in self.__data:
                snp = "04"  # invalid!

                aa = Math.abs(point[0]) # abs x-coordinate
                ab = Math.abs(point[1]) # abs y-coordinate
                ac = Math.abs(point[2]) # abs z-coordinate

                if aa >= ab:
                    # a >= b
                    if ab >= ac:
                        # a > b and b > c
                        snp = "01"
                    # a >= b and c > b
                    elif aa > ac:
                        snp = "03"
                # b > a
                elif ac >= aa:
                    # c >= a > b
                    snp = "03"
                else:
                    # a > b and a > c
                    snp = 01

                if snp == '04':
                    raise Exception('bummer! Bad SNP!')

                if snp not in self._popnames:
                    self._popnames.append(snp)

                self._snps.extend([snp,snp])

                fish = {'pop' : snp, 'fishname' : str(idx), 'alleles' : self._alleles()}
                self._fishies.append(fish)

                idx = idx + 1
                continue

        except Exception, ex:
            raise # re-throw


    def plot(self):
        """ plot ellipsoid """

        # ripped from: 
        #   http://stackoverflow.com/questions/21161884/plotting-a-3d-surface-from-a-list-of-tuples-in-matplotlib?rq=1

        x, y, z = zip(*self.__data)
        z = map(float, z)

        # figure plus cubic plot volume
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_xlim3d(-6,6)
        ax.set_ylim3d(-6,6)
        ax.set_zlim3d(-6,6)

        # scatter plot
        ax.scatter(x,y,z)

        # plot 'em
        plt.show()

    def test(self):
        self.__data = self.__surface(self.__a, self.__b, self.__c, self.__N)
        self.__synthesizeData()
        #for datum in self._snps:

        self.plot();
    