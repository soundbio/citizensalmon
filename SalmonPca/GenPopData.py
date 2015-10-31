""" Class to read GenPop data """
import string
import fileinput
import re
from collections import defaultdict

class GenPopData(object):
    """class to read and massage GenPop data for PCA"""

    __fp = 0
    __snpnames = []
    __popnames = []
    __fishies = []
    __snps = []

    def __alleles(self):
        """__alleles"""
        allele0 = []
        allele1 = []
        for snp in self.__snps:
            allele0.append(snp[0:2])
            allele1.append(snp[2:4])
        return [allele0, allele1]

    def __read(self):
        """__read"""
        section = 'head'
        pop = ''
        individual = ''
        fish = None

        while True:
            line = self.__fp.readline()
            if line == '':
                break

            if section == 'fishies':

                if line.startswith('Pop'):
                    line = self.__fp.readline()
                    if line == '':
                        raise 'bummer!'
                    pop = line[0:re.search('\\d', line).start()]
                    self.__popnames.append(pop)

                if re.search('4\\d', line) != 0:

                    # save old sample
                    if not fish is None:
                        fish['alleles'] = self.__alleles()
                        self.__fishies.append(fish)

                    # new sample
                    self.__snps = []
                    individual = line[0:re.search(',\\t', line).start()]
                    fish = {'pop' : pop, 'individual' : individual}
                    fish.setdefault('alleles', [])
                    line = line[re.search(',\t', line).start()+2:]

                line = line.strip(' \t\r\n')
                self.__snps.extend(line.split('\t'))
                continue

            if section == 'snpnames':

                if line.startswith('Pop'):
                    section = 'fishies'
                    line.strip()
                    self.__fp.seek(-len(line)-1, 1)
                    continue
                self.__snpnames.append(line)
                continue

            if section == 'head':

                if line.startswith(':'):
                    section = 'snpnames'
                continue


    def __init__(self, genpopFilepath):
        self.__fp = open(genpopFilepath)
        self.__read()
        self.__fp.close()

    def Popnames(self):
        """Popnames"""
        return self.__popnames

    def Snpnames(self):
        """Snpnames"""
        return self.__snpnames

    def Fishies(self):
        """Fishies"""
        return self.__fishies

    def PopAlleles(self, pop):
        """PopAlleles"""
        alleles = []
        for fish in self.__fishies:
            if fish['pop'] != pop:
                continue
            alleles.extend(fish['alleles'])
        return alleles

    def Alleles(self):
        """Alleles"""
        alleles = []
        for pop in self.__popnames:
            alleles.extend(self.PopAlleles(pop))
        return alleles
