# ISEQcBioPortal

Scripts that allow you to:
1) Create/Update database from [cBioPortal](https://www.cbioportal.org/) 
2) Annotate VCF with information such as:
- number of samples with one or more mutations
- percentage of samples with one or more mutations

## Install iseqcbioportal library

Optional steps (create virtual environment):
```
python3 -m venv venv
source venv/bin/activate
```

Obligatory steps:
```
python3 -m pip install --upgrade pip
pip3 install iseqcbioportal
```

## Requirements

- python >=3.6
- pandas >= 1.4.2
- requests >= 2.28.1
- SQLAlchemy >= 1.4.0
- loguru >= 0.6.0
- pysam >= 0.21.0

## Create databases

```
create_cbioportal_database
```

## Annotate VCF

```
vcf_annotate_cbioportal --input-vcf "/path/to/input.vcf.gz" \
                        --studies "studyId" \
                        --output-vcf "/path/to/output.vcf.gz"
```