from genpop_data import GenPopData
from pca_synth_data import PcaSynthData

if True:
    psd = PcaSynthData(5, 3.5, 2, 800)
    psd.test()
else:
    gpd = GenPopData("genepop_western_alaska_chinook_RAD.txt")
    fishies = gpd.fishies()
    alleles = gpd.alleles()

    #popalleles = []
    #for pop in gpd.popnames:
    #    popallels.append({pop : []})
    #    for fish in gpd.alleles(pop,
