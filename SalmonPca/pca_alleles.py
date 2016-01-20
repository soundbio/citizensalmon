
import os, sys
lib_path = os.path.abspath(os.path.join('..', 'PcaSycData'))
sys.path.append(lib_path)

from multipledispatch import dispatch
import numpy as np
import population as PopApi
import scipy

class AllelesPCA(object):

    __population = None
    __means = {}   # popmean cache
    __vars = {}    # popvar cache
    __covars = {}  # covarmat cache

    def __init__(self, popapi):
        self.__population = popapi
        return

    def popmean(self, pop):
        popname = 'none'
        if pop == None:
            if 'none' in self.__means:
                return self.__means['none'] # return cached value
            alleles = self.__population.alleles()
        else:
            popname = pop
            if pop in self.__means:
                return self.__means[pop]    # return cached value
            alleles = self.__population.alleles(pop)

        mean = None
        initialized = False
        for allele in alleles:
            if not initialized:
                initialized = True
                mean = np.array(allele, dtype=np.float32, copy=False)
                continue
            mean += np.array(allele, dtype=np.float32, copy=False)
            continue

        ret = mean / len(alleles)
        self.__means[popname] = ret     # cache result
        return ret

    def popvar(self, pop):
        popname = 'none'
        if pop == None:
            if 'none' in self.__vars:
                return self.__vars['none']  # return cached value
            alleles = self.__population.alleles()
        else:
            popname = pop
            if pop in self.__vars:
                return self.__vars[pop]     # return cached value
            alleles = self.__population.alleles(pop)

        mean = self.popmean(pop)

        varsum = None
        initialized = False
        for allele in alleles:
            if not initialized:
                initialized = True
                var = np.array(allele, dtype=np.float32, copy=False) - mean
                varsum = np.inner(var, var)
                continue
            var = np.array(allele, dtype=np.float32, copy=False) - mean
            varsum = varsum + np.inner(var, var)
            continue

        self.__vars[popname] = varsum   # cache result
        return varsum

    def covarmat(self, pop):
        popname = 'none'
        if pop == None:
            if 'none' in self.__covars:
                return self.__covars['none']  # return cached value
            alleles = self.__population.alleles()
        else:
            popname = pop
            if pop in self.__covars:
                return self.__covars[pop]     # return cached value
            alleles = self.__population.alleles(pop)

        mean = self.popmean(pop)
        meanlen = len(mean)

        # calculate covariance matrix of alleles
        covar = np.zeros(shape=(meanlen,meanlen))
        for allele in alleles:
            try:
                avar = allele - mean
                covar = covar + np.outer(avar,avar)
            except:
                ex = sys.exc_info()[0]
            continue

        # cache result
        self.__covars[pop] = covar
        return covar

    def principleAxes(self, pop):
        covar = self.covarmat(pop)

        evals, evects = scipy.sparse.linalg.eigsh(covar)
        eigentuples = zip(evals, evects)
        return eigentuples


    def popvarcloud(self, pop):
        if pop == None:
            alleles = self.__population.alleles()
        else:
            alleles = self.__population.alleles(pop)

        mean = self.popmean(pop)

        varcloud = [None] * len(alleles)
        kdx = 0
        for allele in alleles:
            varcloud[kdx] = np.array(allele, dtype=np.float32, copy=False) - mean
            kdx = kdx + 1
            continue

        return varcloud


    def fst(self, pop, refpop):
        """if this isn't Fst, it's Fst-like"""

        if pop == refpop:
            return 0

        refvar = self.popvar(refpop)

        if refpop == None:
            ralleles = self.__population.alleles()
        else:
            ralleles = self.__population.alleles(pop)

        if pop == None:
            alleles = self.__population.alleles()
        else:
            alleles = self.__population.alleles(pop)

        diffvar = 0
        for rallele in ralleles:
            for allele in alleles:
                diff = np.array(allele, dtype=np.float32, copy=False) - np.array(rallele, dtype=np.float32, copy=False)
                diffvar = diffvar + np.inner(diff, diff)

        diffvar = diffvar / len(ralleles) / len(alleles)
        return (refvar - diffvar)/refvar
