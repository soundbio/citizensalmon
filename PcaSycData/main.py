from genepop_data import GenePopData
from population import Population

# example use reading GenePop data and into a Population object

# once data are pickled, we no longer need GenePopData 
# to retrieve data from the original data file
apop = Population(None)

# read data from gemepop format file
apop.fromGenePop("genepop_western_alaska_chinook_RAD.txt")

# save allele data to pickle file for quicker read
apop.toFile('alaska_chinook.pickle')

# read alleles from pickle file
apop.fromFile('alaska_chinook.pickle')

# get fish information by population
fishies = apop.fishies()                    # list of all fish (and alleles) in file
fishies = apop.fishies(apop.popnames()[2])  # list of all fish (and alleles) in third population

# get alleles by population
alleles = apop.alleles()                   	# all alleles of all populations
alleles = apop.alleles(apop.popnames()[2]) 	# all alleles in third population
