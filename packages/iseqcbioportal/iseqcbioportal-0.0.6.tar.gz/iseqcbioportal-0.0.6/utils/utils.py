import sqlite3
import requests
import os
import sqlalchemy
import pysam
import pandas as pd
from pathlib import Path
from loguru import logger
from typing import List, Dict


# Path to the package
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PACKAGE_PATH = Path(SCRIPT_DIR).parent.absolute()

# PharmGKB clinical/variant URLs
CBIOPORTAL_API = 'https://www.cbioportal.org/api'


def create_sqlite_engine(name: str, print_logger: bool = True) -> sqlalchemy.engine.base.Engine:
    if print_logger:
        logger.info(f"Creating database {name} in {PACKAGE_PATH}/.cache")
    return sqlalchemy.create_engine(f'sqlite:////{PACKAGE_PATH}/.cache/{name}', echo=False)


def connect_to_database(name: str) -> sqlite3.Connection:
    if not os.path.exists(f"{PACKAGE_PATH}/.cache/{name}"):
        logger.error(f"Database {name} does not exist.")
        logger.info('\033[0m' + "Please use " + '\033[1m' + 'create_database' + '\033[0m' + " to create the database.")
        exit(1)
    return sqlite3.connect(f'{PACKAGE_PATH}/.cache/{name}')


def change_columns_to_str(df: pd.DataFrame) -> pd.DataFrame:
    return df.applymap(str)


def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df[["numberOfAlteredCases", "numberOfProfiledCases", "hugoGeneSymbol"]]


def append_to_database(df: pd.DataFrame, name: str, engine: sqlalchemy.engine.base.Engine):
    df.to_sql(name=name, con=engine, if_exists='replace', index=False)


def get_all_studies() -> List[Dict]:
    return requests.get(f"{CBIOPORTAL_API}/studies").json()


def warn_about_no_data(studyId: str):
    logger.warning(f"There is no data in the database for {studyId} (https://www.cbioportal.org/study/summary?id={studyId})")


def load_vcf(vcf_file_path: str) -> pysam.VariantFile:
    return pysam.VariantFile(vcf_file_path)


def load_df(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t")


def add_info_to_header(vcf: pysam.VariantFile):
    vcf.header.info.add("ISEQ_CBIOPORTAL_CASES", number='1', type='String', 
                        description="number of samples with one or more mutations")
    vcf.header.info.add("ISEQ_CBIOPORTAL_FREQUENCY", number='1', type='String', 
                        description="Percentage of samples with one or more mutations")


def add_header_to_output_vcf(vcf_file_path: str, header: pysam.libcbcf.VariantFile) -> pysam.VariantFile:
    return pysam.VariantFile(vcf_file_path, 'w', header=header)
