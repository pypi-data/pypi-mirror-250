#!/usr/bin/env python3

import argparse
import os
import requests
import pandas as pd
from utils import utils
from typing import List
from typing import Dict
from tqdm import tqdm


__version__ = '0.0.3'


def create_cbioportal_database(all_studies: List[Dict]):
    engine = utils.create_sqlite_engine("cbioportal.db")
    for study in tqdm(all_studies):
        studyId = {
            "studyIds": [
                study["studyId"]
            ]
        }
        mutated_genes = requests.post(f"{utils.CBIOPORTAL_API}/mutated-genes/fetch", json = studyId).json()
        df = pd.DataFrame.from_records(mutated_genes)
        if not df.empty:
            df = utils.change_columns_to_str(df)
            df = utils.select_columns(df)
            utils.append_to_database(df, study["studyId"], engine)
        else:
            utils.warn_about_no_data(study["studyId"])


def main():
    parser = argparse.ArgumentParser(description='Create database from cBioPortal data')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(__version__))
    args = parser.parse_args()

    if not os.path.exists(f"{utils.PACKAGE_PATH}/.cache"):
        os.mkdir(f"{utils.PACKAGE_PATH}/.cache")

    # Get all studies from cBioPortal
    all_studies = utils.get_all_studies()

    # Create cBioPortal database
    create_cbioportal_database(all_studies)


if __name__ == '__main__':
    main()
