### **Partial Genome Alignment**

#### Useful Links

  1. [How to perform a RAD-seq de novo assembly](http://catchenlab.life.illinois.edu/stacks/)
      - Great article walking through the steps to perform a de novo alignment on RAD-seq data
  2. [Stacks software](http://catchenlab.life.illinois.edu/stacks/)
      - The software used in the article above for performing the de novo alignment
      - Developed at the University of Oregon
  3. [NCBI Raw Data](http://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP034950)
      - The raw illumina data
      - [FASTQ format](https://en.wikipedia.org/wiki/FASTQ_format)
      - Downloaded and now stored in a more accessible location on S3
  4. S3 bucket
      - Our S3 bucket is named `citizensalmon`
      - Should be publicly accessible (i.e., only requires [aws cli](https://aws.amazon.com/cli/))
      - The most relevant data for the alignment is located within `s3://citizensalmon/larson/illumina`
      - Also potentially relevant is the Atlantic Salmon genome, located at `s3://citizensalmon/atlantic-salmon/genome/`
