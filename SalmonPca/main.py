from genpop_data import GenPopData
from pca_synth_data import PcaSynthData

if False:
    psd = PcaSynthData(5, 3.5, 2, 800)
    psd.test()
else:
    # read and process data in GenPop file 'genepop_western_alaska_chinook_RAD.txt'
    gpd = GenPopData("genepop_western_alaska_chinook_RAD.txt")

    fishies = gpd.fishies()                     # list of all fish (and alleles) in file
    fishies = gpd.fishies(gpd.popnames()[2])    # list of all fish (and alleles) in third population

    alleles = gpd.alleles()                     # all alleles of all populations
    alleles = gpd.alleles(gpd.popnames()[2])    # all alleles in third population
