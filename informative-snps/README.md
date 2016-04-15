### **Identify Most Informative SNPs**

#### Game Plan [as of 2016-04-14]

1. Create one vector per fish that is 4 elements per SNP *>>> the "SNP Vector"*
   - i.e., `[0, 0, 0, 0]`
   - The set of four represents one SNP
   - If a given SNP is not missing data, one of those values would be a `1`
   - Each element within the set of four corresponds to an `A`, `T`, `C`, or `G`
   - Probably use `numpy.int8` or `numpy.float16` for memory savings
2. Calculate the averages of those fish vectors
   - One for the total population
   - One for each of the subpopulations
   - These will be used for finding the Eigen vectors
3. Group the individual fish vectors into their subpopulations
4. For each subpopulation, with each member of that subpoplulation, take the differences between its SNP vector and each of the other individuals in the total fish population *>>> the "SNP difference vector"*
5. For each subpopulation, take those SNP difference vectors and run PCA:
   - Convert each SNP difference vector into a matrix by doing an outer product of itself
   - Add together all of those matricies
   - Find the Eigen vector with the largest Eigen value
   - *Good first guess:* difference between subpopulation average and total population average

#### Numbers to know

1. Number of SNPs: **10,944**
2. Number of indivudal fish: **~250**
3. Number of regions (*i.e., subpopulations*): **5**

#### Description of Files

*(Click filename to download from S3)*

1. [cjfas-2013-0502suppla.xlsx](http://citizensalmon.s3.amazonaws.com/larson/raw-data/cjfas-2013-0502suppla.xlsx) (80KB): *(description pending...)*
2. [cjfas-2013-0502supplb.docx](http://citizensalmon.s3.amazonaws.com/larson/raw-data/cjfas-2013-0502supplb.docx) (80KB): *(description pending...)*
3. [cjfas-2013-0502supplc.xlsx](http://citizensalmon.s3.amazonaws.com/larson/raw-data/cjfas-2013-0502supplc.xlsx) (12KB): *(description pending...)*
4. [cjfas-2013-0502suppld.xlsx](http://citizensalmon.s3.amazonaws.com/larson/raw-data/cjfas-2013-0502suppld.xlsx) (12KB): *(description pending...)*
5. [cjfas-2013-0502supple.docx](http://citizensalmon.s3.amazonaws.com/larson/raw-data/cjfas-2013-0502supple.docx) (25KB): *(description pending...)*
6. [cjfas-2013-0502supplf.xlsx](http://citizensalmon.s3.amazonaws.com/larson/raw-data/cjfas-2013-0502supplf.xlsx) (9KB): *(description pending...)*
7. [cjfas-2013-0502suppli.fa](http://citizensalmon.s3.amazonaws.com/larson/raw-data/cjfas-2013-0502suppli.fa) (3MB): *(description pending...)*
8. [genepop_western_alaska_chinook_RAD.txt](http://citizensalmon.s3.amazonaws.com/larson/raw-data/genepop_western_alaska_chinook_RAD.txt) (14MB): *(description pending...)*
