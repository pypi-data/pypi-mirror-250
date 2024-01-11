#!/usr/bin/env python3

from cbioportal.create_cbioportal_database import *


def test_create_cbioportal_database():
    # create example List[Dict] of studies
    studies = [
        {
            "studyId": "cervix_msk_2023"
        },
        {
            "studyId": "all_stjude_2013"
        },
        {
            "studyId": "breast_msk_2018"
        }
    ]

    # create cbioportal database
    create_cbioportal_database(studies)

    # check if cbioportal.db exists
    assert os.path.exists(f"{utils.PACKAGE_PATH}/.cache/cbioportal.db")

    # check if cbioportal.db has example tables
    engine = utils.create_sqlite_engine("cbioportal.db", print_logger=False)
    test_list = ['cervix_msk_2023', 'all_stjude_2013', 'breast_msk_2018']
    assert all(ele in engine.table_names() for ele in test_list)

    # check if cbioportal.db has data
    for table in engine.table_names():
        df = pd.read_sql_table(table, engine)
        assert not df.empty


if __name__ == '__main__':
    test_create_cbioportal_database()
