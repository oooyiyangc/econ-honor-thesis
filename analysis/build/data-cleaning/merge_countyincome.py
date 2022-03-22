import os
import glob

import pandas as pd

CLEANEDDATA_DIR = "../../data/cleaned-data/countyincome/"


def merge_year(year):
    path = CLEANEDDATA_DIR + str(year)
    merged = pd.DataFrame()
    for datafile in glob.glob(f"{path}/*.csv"):
        data = pd.read_csv(datafile)
        merged = pd.concat([merged, data])
    merged["YEAR"] = [year] * merged.shape[0]
    merged.to_csv(CLEANEDDATA_DIR + "countyincome" + str(year) + ".csv", index=False)


def merge_all():
    year_list = range(1991, 2008)
    for year in year_list:
        merge_year(year)

def merge_all_to_single_file():
    merged = pd.DataFrame()
    for datafile in glob.glob(f"{CLEANEDDATA_DIR}*.csv"):
        current = pd.read_csv(datafile)
        merged = pd.concat([merged, current])
    merged.to_csv(CLEANEDDATA_DIR + "merged/countyincome_merged.csv", index=False)

if __name__ == "__main__":
    # merge_all()
    merge_all_to_single_file()
    # merge_year(2009)