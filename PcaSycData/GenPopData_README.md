genpop_data.py, population.py and main.py script files are used in conjunction with GenPop formated data such as 'genepop_western_alaska_chinook_RAD.txt'.

The GenPopData class in 'genpop_data.py' reads SNP data from the Chinook GenPop file and repackages the SNP's listed for each fish into two 'alleles' per fish. Data for each fish are packaged into a fish object containing population id, fish id and allele data. GenPopData can also return collections of alleles by population id or the entire collection. (See main.py for example code.)

Because SNPs in GenPop formatted data are reported as digits 1-4 ("01", "02", 03", "04") each representing a single nucleotide A,T,G or C (not necessarily in that order), the GenPopData class expands each SNP into four bits: "01" -> [1,0,0,0], "02" -> [0,1,0,0], "03" -> [0,0,1,0] and "04" -> [0,0,0,1]. This expansion is necessary so that vector arithmetic can be performed on the resulting alleles without mixing between SNP's.

Information can be retrieved from the GenPopData class as lists of fish objects (population id, fish id, alleles) organized by population or for the entire data set. Similarly, collections of alleles can be retrieved by population or the entire data set. The latter will be inputs to PCA analysis.
