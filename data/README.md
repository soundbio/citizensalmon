## Data Conversion/Cleanup Steps

### File: `snps_287_cleaned.csv`

  1. Source: `cjfas-2013-0502suppli.fa`
  2. Copy data from table S3 in the Word Doc file, paste into Excel
  2. Rename headers to be SQL-friendly
  3. Replace all `NA` in workbook, with `"Match entire cell contents"` option checked
  4. Save as `.csv` file

Notes:
  * Cleaned file saved as `snps_287_cleaned.csv`
  * Records where `source` is `a` can be directly mapped to Larson 2014 SNPs in file `cjfas-2013-0502suppli.fa`
    * `cjfas-2013-0502suppli.fa` format: `snp:ID:<N>` where `<N>` is the SNP ID number
    * `snps_287_cleaned.csv` format: `Ots_RAD<N>` where `<N>` is the SNP ID number