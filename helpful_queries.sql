-- table for the 46 most-informative Larson paper SNPs
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


-- apply stricter logic for informative cuts
create table really_informative_cuts (
    enzyme text,
    snp text,
    cut_site bigint,
    allele text
);

-- cut allele 1 but not allele 2
insert into really_informative_cuts
(   enzyme,
    snp,
    cut_site,
    allele
)
select
    a1.enzyme,
    a1.snp,
    a1.cut_site,
    a1.allele
from (
    select *
    from cut_sites
    where allele = 'allele_1'
) as a1
left join (
    select 
        snp,
        enzyme,
        count(*) as n
    from cut_sites
    where allele = 'allele_2'
    group by
        snp,
        enzyme
) as a2
on a2.snp=a1.snp
and a2.enzyme=a1.enzyme
where a2.snp is null;

-- cut allele 2 but not allele 1
insert into really_informative_cuts
(   enzyme,
    snp,
    cut_site,
    allele
)
select
    a2.enzyme,
    a2.snp,
    a2.cut_site,
    a2.allele
from (
    select *
    from cut_sites
    where allele = 'allele_2'
) as a2
left join (
    select 
        snp,
        enzyme,
        count(*) as n
    from cut_sites
    where allele = 'allele_1'
    group by
        snp,
        enzyme
) as a1
on a1.snp=a2.snp
and a1.enzyme=a2.enzyme
where a1.snp is null;



-- write really informative cuts to csv
-- (this is sqlite specific)
.mode csv
.header on
.output really_informative_cuts.csv

select i.*
from really_informative_cuts as i 
join snp_46 as s 
on s.snp=i.snp;



-- identify the most useful Restriction Enzymes
select
    i.enzyme,
    count(distinct i.snp) as snp_count
from really_informative_cuts as i
join snp_46 as s
on s.snp = i.snp
left join (
    select
        distinct a.snp
    from really_informative_cuts as a
    join snp_46 as b
    on b.snp = a.snp
    where a.enzyme = 'FaiI'
) as e1
on e1.snp = i.snp
where e1.snp is null
group by
    i.enzyme
order by
    count(distinct i.snp) desc
;



-- how many unique snps of the 46 are usable?
select
    i.snp,
    count(*)
from really_informative_cuts as i
join snp_46 as s
on s.snp = i.snp
group by
    i.snp
;
