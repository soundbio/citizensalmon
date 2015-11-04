""" Class to read GenPop data """
from population import Population as PopApi
import string
import fileinput
import re
from collections import defaultdict

class GenPopData(PopApi):
    """class to read and massage GenPop data for PCA"""

    # initialization
    def __init__(self, genpopFilepath):
        PopApi.__init__(self, None)
        with open(genpopFilepath, 'r', 1) as fp:
            self.__read(fp)

    # implementation
    def __snptobin(self, snp):
        ret = [0,0,0,0]
        ret[int(snp)-1] = 1
        return ret

    #def __alleles(self):
    #    """__alleles"""
    #    snpcount = len(self.__snps)
    #    allele0 = snpcount * 4 * [None]
    #    allele1 = snpcount * 4 * [None]
    #    idx = 0
    #    for snp in self.__snps:
    #        allele0[idx:idx+4] = PopApi._snptobin(snp[0:2])
    #        allele1[idx:idx+4] = PopApi._snptobin(snp[2:4])
    #        idx = idx + 4
    #    return [allele0, allele1]

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

