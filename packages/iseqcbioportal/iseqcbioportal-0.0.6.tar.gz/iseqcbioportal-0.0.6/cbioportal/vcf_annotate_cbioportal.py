#!/usr/bin/env python3

import argparse
import pandas as pd
import sqlite3
import pysam
from utils import utils


__version__ = '0.0.6'


def annotate_vcf_with_studies(record: pysam.libcbcf.VariantRecord, vcf: pysam.VariantFile, studies: list, database: sqlite3.Connection):
    gene_name = record.info.get("ISEQ_GENES_NAMES")[0] if record.info.get("ISEQ_GENES_NAMES") else None
    if gene_name:
        cases_for_gene = 0
        all_cases = 0
        for study_id in studies:
            df = pd.read_sql(f'''SELECT * FROM {study_id} 
                WHERE hugoGeneSymbol LIKE "{gene_name}"''' , database)
            if not df.empty:
                cases_for_gene += int(df["numberOfAlteredCases"].tolist()[0])
                all_cases += int(df["numberOfProfiledCases"].tolist()[0])
        if cases_for_gene > 0:
            frequency = round(int(cases_for_gene)/int(all_cases)*100, 1)
            record.info["ISEQ_CBIOPORTAL_CASES"] = str(cases_for_gene)
            record.info["ISEQ_CBIOPORTAL_FREQUENCY"] = str(frequency)
    vcf.write(record)   


def annotate_vcf_with_table(record: pysam.libcbcf.VariantRecord, vcf: pysam.VariantFile, frequency_table: pd.DataFrame):    
    gnomad = record.info.get("ISEQ_GNOMAD_ID")
    df = frequency_table[frequency_table['GNOMAD_ID'] == gnomad]
    if not df.empty:
        record.info["ISEQ_CBIOPORTAL_CASES"] = str(df["Count"].tolist()[0])
        record.info["ISEQ_CBIOPORTAL_FREQUENCY"] = str(df["frequency"].tolist()[0])
    vcf.write(record)   


def main():
    parser = argparse.ArgumentParser(description='Annotate VCF with number of samples with one or more mutations \
                                     and percentage of samples with one or more mutations')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(__version__))
    parser.add_argument('--input-vcf', type=str, required=True, help='Input VCF to annotate')
    parser.add_argument('--studies', type=str, required=False, help='StudyIds')
    parser.add_argument('--frequency-table', type=str, required=False, help='Table with frequencies')
    parser.add_argument('--output-vcf', type=str, required=True, help='Output annotated VCF')
    args = parser.parse_args()

    # connect to database
    database = utils.connect_to_database("cbioportal.db")

    # load input VCF
    vcf_reader = utils.load_vcf(args.input_vcf)

    # add info to header
    utils.add_info_to_header(vcf_reader)

    # add header to output VCF
    vcf_writer = utils.add_header_to_output_vcf(args.output_vcf, header=vcf_reader.header)

    # remove empty elements from studies
    studies = [x for x in args.studies.split(" ") if x != ''] if args.studies else []

    # annotate vcf
    for record in vcf_reader.fetch():
        if studies:
            annotate_vcf_with_studies(record, vcf_writer, studies, database)
        else:
            annotate_vcf_with_table(record, vcf_writer, utils.load_df(args.frequency_table))


if __name__ == '__main__':
    main()
