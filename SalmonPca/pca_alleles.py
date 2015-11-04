
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
        if pop == None:
            alleles = self.__population.alleles()
        else:
            alleles = self.__population.alleles(pop)

        mean = None
        initialized = False
        for allele in alleles:
            if not initialized:
                initialized = True
                mean = np.array(allele)
                continue
            mean += np.array(allele)
            continue
        mean = mean.astype(np.float32)
        return mean / len(alleles)

