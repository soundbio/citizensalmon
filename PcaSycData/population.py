# Population provides interface to population allele data
from multipledispatch import dispatch
import cPickle
import string
import fileinput
import re
from collections import defaultdict

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
        if snp == '00': 
            return ret
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

    def toPickle(self, outfile):
        with open(outfile, 'wb', 1) as fp:
            cPickle.dump(self._snpnames, fp)
            cPickle.dump(self._popnames, fp)
            cPickle.dump(self._fishnames, fp)
            idx = 0
            while idx < len(self._fishies):
                fish = self._fishies[idx]
                cPickle.dump(fish['pop'], fp)
                cPickle.dump(fish['fishname'], fp)
                nalleles = len(fish['alleles'])
                cPickle.dump(nalleles, fp)
                jdx = 0
                while jdx < nalleles:
                    allele = fish['alleles'][jdx]
                    cPickle.dump(allele, fp)
                    jdx = jdx + 1
                idx = idx + 1
            fp.flush()
        return

    def fromPickle(self, infile):
        self._snpnames = []
        self._popnames = []
        self._fishnames = []
        self._fishies = []
        self._snps = []

        with open(infile, 'rb', 1) as fp:
            self._snpnames = cPickle.load(fp)
            self._popnames = cPickle.load(fp)
            self._fishnames = cPickle.load(fp)

            idx = 0
            self._fishies = []
            while idx < len(self._fishnames):
                fish = {'pop' : cPickle.load(fp), 'fishname' : cPickle.load(fp)}
                fish.setdefault('alleles', [])
                nalleles = cPickle.load(fp)
                jdx = 0
                while jdx < nalleles:
                    fish['alleles'].append(cPickle.load(fp))
                    jdx = jdx + 1
                self._fishies.append(fish)
                idx = idx + 1
        return

    def fromGenePop(self, filepath):
        """fromGenePop"""
        self._snpnames = []
        self._popnames = []
        self._fishnames = []
        self._fishies = []
        self._snps = []

        with open(filepath, 'r', 1) as fp:
            self.__read(fp)

    def __read(self, fp):
        """__read"""
        section = 'head'
        pop = ''
        fishinfo = ''
        fish = None
        nopop = True

        while True:
            if nopop:
                line = fp.readline()
                if line == '':
                    if not fish is None:
                        fish['alleles'] = self._alleles()
                        self._fishies.append(fish)
                    break
            else:
                nopop = True

            if section == 'snpdata':

                if line.startswith('Pop'):
                    line = fp.readline()
                    if line == '':
                        raise 'bummer!'
                    pop = line[0:re.search(r'\d', line).start()]
                    self._popnames.append(pop)

                if re.search(r'4\d', line) != 0:

                    # save old sample
                    if not fish is None:
                        fish['alleles'] = self._alleles()
                        self._fishies.append(fish)

                    # new sample
                    self._snps = []
                    fishname = line[0:re.search(r',\t', line).start()]
                    self._fishnames.append(fishname)
                    fish = {'pop' : pop, 'fishname' : fishname}
                    fish.setdefault('alleles', [])
                    line = line[re.search(r',\t', line).start()+2:]

                line = line.strip(' \t\r\n')
                self._snps.extend(line.split('\t'))
                continue

            if section == 'snpnames':

                if line.startswith('Pop'):
                    section = 'snpdata'
                    nopop = False
                    continue
                self._snpnames.append(line.strip(' \t\r\n'))
                continue

            if section == 'head':

                if line.startswith(':'):
                    section = 'snpnames'
                continue

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

