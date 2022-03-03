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
    pass


if __name__ == "__main__":
    merge_year(2001)
