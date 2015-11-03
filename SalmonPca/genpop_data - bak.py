""" Class to read GenPop data """
from multipledispatch import dispatch
import itertools
import string
import fileinput
import re
from collections import defaultdict

class GenPopData(object):
    """class to read and massage GenPop data for PCA"""

    __fp = 0
    __snpnames = []
    __popnames = []
    __fishnames = []
    __fishies = []
    __snps = []
    __fsts = None

    def __snptobin(self, snp):
        ret = [0,0,0,0]
        ret[int(snp)-1] = 1
        return ret

    def __alleles(self):
        """__alleles"""
        snpcount = len(self.__snps)
        allele0 = snpcount * 4 * [None]
        allele1 = snpcount * 4 * [None]
        idx = 0
        for snp in self.__snps:
            #allele0.append(snp[0:2])
            #allele1.append(snp[2:4])
            allele0[idx:idx+4] = self.__snptobin(snp[0:2])
            allele1[idx:idx+4] = self.__snptobin(snp[2:4])
            idx = idx + 4
        return [allele0, allele1]

    def __read(self):
        """__read"""
        section = 'head'
        pop = ''
        fishinfo = ''
        fish = None
        nopop = True

        while True:
            if nopop:
                line = self.__fp.readline()
                if line == '':
                    break
            else:
                nopop = True

            if section == 'fishies':

                if line.startswith('Pop'):
                    line = self.__fp.readline()
                    if line == '':
                        raise 'bummer!'
                    pop = line[0:re.search(r'\d', line).start()]
                    self.__popnames.append(pop)

                if re.search(r'4\d', line) != 0:

                    # save old sample
                    if not fish is None:
                        fish['alleles'] = self.__alleles()
                        self.__fishies.append(fish)

                    # new sample
                    self.__snps = []
                    fishname = line[0:re.search(r',\t', line).start()]
                    self.__fishnames.append(fishname)
                    fish = {'pop' : pop, 'fishname' : fishname}
                    fish.setdefault('alleles', [])
                    line = line[re.search(r',\t', line).start()+2:]

                line = line.strip(' \t\r\n')
                self.__snps.extend(line.split('\t'))
                continue

            if section == 'snpnames':

                if line.startswith('Pop'):
                    section = 'fishies'
                    nopop = False
                    continue
                self.__snpnames.append(line.strip(' \t\n'))
                continue

            if section == 'head':

                if line.startswith(':'):
                    section = 'snpnames'
                continue


    def __init__(self, genpopFilepath):
        self.__fp = open(genpopFilepath)
        self.__read()
        self.__fp.close()

    def popnames(self):
        """popnames"""
        return self.__popnames

    def snpnames(self):
        """snpnames"""
        return self.__snpnames

    def fishnames(self):
        return self.__fishnames

    def __popmean(alleles):
        return sum(alleles)/len(alleles)

    @dispatch(str,str)
    def fst(self, pop0, pop1):
        # return cached values
        if self.__fsts == None or self.__fsts[pop] == None:
            self.__fsts = {pop : map(self.__popmean, self.alleles(pop))}
        return self.__fsts['pop']

    @dispatch(str)
    def var(self, pop):
        # return cached values
        if self.__fsts == None or self.__fsts[pop] == None:
            self.__fsts = {pop : map(self.__popmean, self.alleles(pop))}
        return self.__fsts['pop']

    def var(self):
        # return cached values
        if self.__fsts == None or self.__fsts['pop'] == None:
            popmean = map(self.__popmean, self.alleles)
            vars = []
            for allele in self.alleles:
                vars
            self.__fsts = {'pop' : {'mean' : popmean, 'var' : popvar}}
        return self.__fsts['pop']

    @dispatch(str)
    def fishies(self, pop):
        """fishies"""
        popfishies = []
        for fish in self.__fishies:
            if fish['pop'] != pop:
                continue
            popfishies.extend(fish)
        return popfishies

    @dispatch()
    def fishies(self):
        """fishies"""
        return self.__fishies

    @dispatch(str, str)
    def alleles(self, pop, fishname):
        """alleles"""
        alleles = []
        for fish in self.__fishies:
            if fish['pop'] != pop:
                continue
            if fish['fishname'] != fishname:
                continue
            alleles.extend(fish['alleles'])
        return alleles

    @dispatch(str)
    def alleles(self, pop):
        """alleles"""
        alleles = []
        for fish in self.__fishies:
            if fish['pop'] != pop:
                continue
            alleles.extend(fish['alleles'])
        return alleles

    @dispatch()
    def alleles(self):
        """alleles"""
        alleles = []
        for pop in self.__popnames:
            alleles.extend(self.alleles(pop))
        return alleles
