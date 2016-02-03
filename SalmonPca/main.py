import os, sys
lib_path = os.path.abspath(os.path.join('..', 'PcaSycData'))
sys.path.append(lib_path)

from pca_synth_data import PcaSynthData
from pca_alleles import AllelesPCA
from population import Population

if False:
    psd = PcaSynthData(5, 3.5, 2, 800)
    psd.test()
elif True:
    apop = Population(None)

    # read and process data in GenePop file 'genepop_western_alaska_chinook_RAD.txt'
    #apop.fromGenePop("genepop_western_alaska_chinook_RAD.txt")

    #save to pickle file
    #apop.toFile('alaska_chinook.pickle')

    # once data are pickled, we no longer need GenePopData 
    # to retrieve data from the original data file
    apop.fromFile('alaska_chinook.pickle')

    """
    # get fish information by population
    fishies = apop.fishies()                    # list of all fish (and alleles) in file
    fishies = apop.fishies(apop.popnames()[2])  # list of all fish (and alleles) in third population

    # get alleles by population
    alleles = apop.alleles()                   	# all alleles of all populations
    alleles = apop.alleles(apop.popnames()[2]) 	# all alleles in third population
    """

    apca = AllelesPCA(apop)
    # mean = apca.popmean(apop.popnames()[2])
    # covar = apca.covarmat(apop.popnames()[2])
    # pca = apca.principleAxes(apop.popnames()[2])
    maxeignenvalue, eigenvector = apca.eigenstuffPowerMethod(apop.popnames()[2])

    maxidx = 0
    maxelement = 0
    for idx in range(0, eigenvector.shape[0]-1):
        if maxelement < eigenvector[idx]:
            maxelement = eigenvector[idx]
            maxidx = idx

    print maxeignenvalue, maxidx/4, apop.snpnames[maxidx/4]