from sqlalchemy import create_engine
from uuid import uuid4
from Bio import Restriction, SeqIO
from Bio.Restriction import AllEnzymes
import pandas as pd

import logging
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create sqlite db
guid = str(uuid4()).split('-')[0]
db = 'snps_%s.db' % guid
logger.debug('Creating db engine: %s' % db)
eng = create_engine('sqlite:///%s' % db)



def print_cuts(seq, enz = AllEnzymes):
    d = enz.search(seq)
    for enzyme, cuts in d.iteritems():
        if len(cuts) == 0:
            continue
        logger.debug('%s: %s' % (enzyme, cuts))
    return None

def cuts_to_df(seq, snp, allele, enz = AllEnzymes):
    s = enz.search(seq)
    d = {'enzyme':[],
         'snp':[],
         'allele':[],
         'cut_site':[]}
    
    logger.debug('Searching for cuts for `%s` <%s>' % (snp, allele))
    for enzyme, cuts in s.iteritems():
        if len(cuts) == 0:
            continue
        for i in cuts:
            d['enzyme'].append(str(enzyme))
            d['snp'].append(snp)
            d['allele'].append(allele)
            d['cut_site'].append(i)
    
    df = pd.DataFrame(d)
    logger.debug('%d cut sites found' % len(df))
    return df



# iterate over sequence data
fn = 'data/larson/cjfas-2013-0502suppli.fa'
with open(fn, 'rU') as f:
    for record in SeqIO.parse(f, "fasta"):
        id_list = record.id.split(';')
        snp_id = id_list[0]
        allele = id_list[1]
        
        logger.debug('SNP:       %s' % snp_id)
        logger.debug('Allele:    %s' % allele)
        logger.debug('Seq:       %s' % record.seq)
        
        # parse cuts
        df = cuts_to_df(record.seq, snp_id, allele, AllEnzymes)
        
        # write df to db
        logger.debug('Writing to db...')
        df.to_sql('cut_sites', eng, if_exists='append', index=False)



# SQL stuff
qry = '''
create table informative_cuts (
    enzyme text,
    snp text,
    cut_site bigint,
    allele_found text
);

insert into informative_cuts (
    enzyme,
    snp,
    cut_site,
    allele_found
)
select
    a1.enzyme,
    a1.snp,
    a1.cut_site,
    a1.allele
from (
    select *
    from cut_sites
    where allele='allele_1'
) as a1
left join (
    select *
    from cut_sites
    where allele='allele_2'
) as a2
on a2.enzyme=a1.enzyme
and a2.snp=a1.snp
and a2.cut_site=a1.cut_site
where a2.cut_site is null
;

insert into informative_cuts (
    enzyme,
    snp,
    cut_site,
    allele_found
)
select
    a2.enzyme,
    a2.snp,
    a2.cut_site,
    a2.allele
from (
    select *
    from cut_sites
    where allele='allele_2'
) as a2
left join (
    select *
    from cut_sites
    where allele='allele_1'
) as a1
on a1.enzyme=a2.enzyme
and a1.snp=a2.snp
and a1.cut_site=a2.cut_site
where a1.cut_site is null
;

-- look for highest-cutting enzymes
select
    enzyme,
    count(*),
    sum(n)
from (
    select
        enzyme,
        snp,
        count(*) as n
    from informative_cuts
    group by
        enzyme,
        snp
) as t
group by
    enzyme
order by
    count(*) desc
;
'''
print 'Up next!\n%s' % qry
