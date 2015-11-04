from genepop_data import GenePopData
from population import Population

# example use of GenePopData and Population

# read and process data in GenePop file 'genepop_western_alaska_chinook_RAD.txt'
gpd = GenePopData("genepop_western_alaska_chinook_RAD.txt")

fishies = gpd.fishies()                     # list of all fish (and alleles) in file
fishies = gpd.fishies(gpd.popnames()[2])    # list of all fish (and alleles) in third population

alleles = gpd.alleles()                     # all alleles of all populations
alleles = gpd.alleles(gpd.popnames()[2])    # all alleles in third population

#save to pickle file
gpd.toFile('alaska_chinook.pickle')


# once data are pickled, we no longer need GenePopData 
# to retrieve data from the original data file
apop = Population(None)
apop.fromFile('alaska_chinook.pickle')

fishies = apop.fishies()                    # list of all fish (and alleles) in file
fishies = apop.fishies(apop.popnames()[2])  # list of all fish (and alleles) in third population

alleles = apop.alleles()                   	# all alleles of all populations
alleles = apop.alleles(apop.popnames()[2]) 	# all alleles in third population
