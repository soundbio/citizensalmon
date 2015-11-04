
import os, sys
lib_path = os.path.abspath(os.path.join('..', 'PcaSycData'))
sys.path.append(lib_path)

from multipledispatch import dispatch
import numpy as np
import population as PopApi

class AllelesPCA(object):

    __population = None

    def __init__(self, popapi):
        self.__population = popapi
        return

    def popmean(self, pop):
        mean = None
        if pop == None:
            alleles = self.__population.alleles()
        else:
            alleles = self.__population.alleles(pop)
        for allele in alleles:
            if mean == None:
                mean = allele
                continue
            map(int.add, mean, allele)
            continue
        return np.array(mean) / len(alleles)

