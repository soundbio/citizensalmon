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

### File: `best_enzymes.csv`

Output from this query:
```sql
create table snp_46 (
    snp text
);

insert into snp_46 (snp)
values ('snp:ID:4369'),('snp:ID:6618'),('snp:ID:1072'),('snp:ID:995'),
('snp:ID:1282'),('snp:ID:1507'),('snp:ID:1609'),('snp:ID:8354'),
('snp:ID:7695'),('snp:ID:7165'),('snp:ID:7145'),('snp:ID:10583'),
('snp:ID:10807'),('snp:ID:11441'),('snp:ID:4043'),('snp:ID:3123'),
('snp:ID:26540'),('snp:ID:17873'),('snp:ID:14852'),('snp:ID:14650'),
('snp:ID:12182'),('snp:ID:6688'),('snp:ID:3425'),('snp:ID:3386'),
('snp:ID:2687'),('snp:ID:2683'),('snp:ID:2677'),('snp:ID:2598'),
('snp:ID:2207'),('snp:ID:2150'),('snp:ID:2102'),('snp:ID:2068'),
('snp:ID:3703'),('snp:ID:6097'),('snp:ID:5848'),('snp:ID:5730'),
('snp:ID:1510'),('snp:ID:4999'),('snp:ID:4778'),('snp:ID:3925'),
('snp:ID:3858'),('snp:ID:3769'),('snp:ID:3766'),('snp:ID:5335'),
('snp:ID:1372'),('snp:ID:10412');

select
    i.enzyme,
    count(distinct i.snp) as snp_count
from informative_cuts as i
join snp_46 as s
on s.snp = i.snp
group by
    i.enzyme
order by
    count(*) desc;
```

SNP list in that query was created from mapped SNP data identifying which SNP IDs fell within the final 96 used. Of the total 96, only 46 were sourced from Larson data, thus only those 46 could be mapped and checked against in this query. Of the 46, only one SNP ID was not found in the `informative_cuts` table: `snp:ID:8354`.

### File: `iupac-codes.pkl`

Python dict stored as a pickled file, created via the following script:

```python
# IUPAC codes pulled from:
# http://www.bioinformatics.org/sms/iupac.html
import pickle as pkl
d = {'U':['T'],
     'R':['A', 'G'],
     'Y':['C', 'T'],
     'S':['G', 'C'],
     'W':['A', 'T'],
     'K':['G', 'T'],
     'M':['A', 'C'],
     'B':['C', 'G', 'T'],
     'D':['A', 'G', 'T'],
     'H':['A', 'C', 'T'],
     'V':['A', 'C', 'G'],
     'N':['A', 'C', 'G', 'T']}
with open('iupac-codes.pkl', 'wb') as f:
    pkl.dump(d, f)

# load data back into python via:
#with open('iupac-codes.pkl', 'rb') as f:
#    d = pkl.load(f)
```
