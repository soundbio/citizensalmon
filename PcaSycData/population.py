# Population provides interface to population allele data
from multipledispatch import dispatch
import json

class Population(object):
    """container for population allele data"""

    _snpnames = []
    _popnames = []
    _fishnames = []
    _fishies = []
    _snps = []

    __snptobinCallback = None

    # initialization
    def __init__(self, snptobinCallback):
        if snptobinCallback != None:
            self.__snptobinCallback = snptobinCallback
        else:
            self.__snptobinCallback = self.__snptobin
        return

    # implementation -- override this for different file types
    def __snptobin(self, snp):
        ret = [0,0,0,0]
        ret[int(snp)-1] = 1
        return ret

    def _alleles(self):
        """__alleles"""
        snpcount = len(self._snps)
        allele0 = snpcount * 4 * [None]
        allele1 = snpcount * 4 * [None]
        idx = 0
        for snp in self._snps:
            allele0[idx:idx+4] = self.__snptobinCallback(snp[0:2])
            allele1[idx:idx+4] = self.__snptobinCallback(snp[2:4])
            idx = idx + 4
        return [allele0, allele1]

    def toFile(self, outfile):
        with open(outfile, 'w', 1) as fp:
            json.dump(self._snpnames, fp)
            json.dump(self._popnames, fp)
            json.dump(self._fishnames, fp)
            json.dump(self._fishies, fp)
            #pickle.dump(self._snpnames, fp)
            #pickle.dump(self._popnames, fp)
            #pickle.dump(self._fishnames, fp)
            #pickle.dump(self._fishies, fp)

        return

    def fromFile(self, infile):
        with open(infile, 'r', 1) as fp:
            self._snpnames = json.load(fp)
            self._popnames = json.load(fp)
            self._fishnames = json.load(fp)
            self._fishies = json.load(fp)
            #self._snpnames = pickle.load(fp)
            #self._popnames = pickle.load(fp)
            #self._fishnames = pickle.load(fp)
            #self._fishies = pickle.load(fp)

        return

    def popnames(self):
        """popnames"""
        return self._popnames

    def snpnames(self):
        """snpnames"""
        return self._snpnames

    def fishnames(self):
        return self._fishnames

    @dispatch(str, str)
    def fishies(self, pop, fishname):
        """fishies by population and fishname"""
        for fish in self._fishies:
            if fish['pop'] != pop:
                continue
            if fish['fishname'] != fishname:
                continue
        return fish

    @dispatch(str)
    def fishies(self, pop):
        """fishies by population"""
        popfishies = []
        for fish in self._fishies:
            if fish['pop'] != pop:
                continue
            popfishies.append(fish)
        return popfishies

    @dispatch()
    def fishies(self):
        """fishies"""
        return self._fishies

    @dispatch(str, str)
    def alleles(self, pop, fishname):
        """alleles by population and fishname"""
        alleles = []
        for fish in self._fishies:
            if fish['pop'] != pop:
                continue
            if fish['fishname'] != fishname:
                continue
            alleles.extend(fish['alleles'])
        return alleles

    @dispatch(str)
    def alleles(self, pop):
        """alleles by population"""
        alleles = []
        for fish in self._fishies:
            if fish['pop'] != pop:
                continue
            # add both alleles to the result set
            alleles.extend(fish['alleles'])
        return alleles

    @dispatch()
    def alleles(self):
        """alleles"""
        alleles = []
        for pop in self._popnames:
            alleles.extend(self.alleles(pop))
        return alleles

