import os
import re
import glob
import numpy as np
import pandas as pd

RAWDATA_DIR = "../../data/raw-data/"
GINI_DIR = RAWDATA_DIR + "gini/"
CLEANEDDATA_DIR = "../../data/cleaned-data/gini/"


def clean_census_gini(file):
    data = pd.read_excel(file).iloc[2:, :5]
    data.columns = ["STATE", "COUNTY", "GEOFIPS", "HHLDS", "GINI"]

    cleaned = data[["STATE", "COUNTY", "GEOFIPS", "GINI"]]
    return cleaned


def clean_acs_gini(file):
    data = pd.read_csv(file)
    data["GEOFIPS"] = data["id"].str.extract(r'US(\d*)').astype(int)
    data["STATE"] = data["Geographic Area Name"].str.extract(r', (.*)')
    data["COUNTY"] = data["Geographic Area Name"].str.extract(r'(.*),')
    data.rename(columns={"Estimate!!Gini Index": "GINI"}, inplace=True)

    cleaned = data[["STATE", "COUNTY", "GEOFIPS", "GINI"]]
    return cleaned


def interpolate(data, years, series=[], method="const"):
    assert method in ["const", "approx"], "Invalid interpolation method."
    cleaned = pd.DataFrame()
    if method == "const":
        for year in years:
            data_year = data.copy()
            data_year["YEAR"] = np.ones(data_year.shape[0]) * year
            cleaned = pd.concat([cleaned, data_year])

    else:
        assert len(years) == len(series), "Length mismatch: year and series"
        raise Exception("Not implemented. ")

    return cleaned


def clean_all_const():
    cleaned_all = pd.DataFrame()
    files = ["1990census_gini.xls", "2000census_gini.xls",
             "ACSDT5Y2010.csv", "ACSDT5Y2015.csv", "ACSDT5Y2020.csv"]
    for i, file in enumerate(files):
        if i == 0:
            cleaned = clean_census_gini(GINI_DIR + file)
            cleaned_all = pd.concat([cleaned_all, interpolate(cleaned, np.arange(1989, 1996))])
        elif i == 1:
            cleaned = clean_census_gini(GINI_DIR + file)
            cleaned_all = pd.concat([cleaned_all, interpolate(cleaned, np.arange(1996, 2006))])
        elif i == 2:
            cleaned = clean_acs_gini(GINI_DIR + file)
            cleaned_all = pd.concat([cleaned_all, interpolate(cleaned, np.arange(2006, 2011))])
        elif i == 3:
            cleaned = clean_acs_gini(GINI_DIR + file)
            cleaned_all = pd.concat([cleaned_all, interpolate(cleaned, np.arange(2011, 2016))])
        elif i == 4:
            cleaned = clean_acs_gini(GINI_DIR + file)
            cleaned_all = pd.concat([cleaned_all, interpolate(cleaned, np.arange(2016, 2020))])
        else:
            raise Exception("Invalid index.")

    cleaned_all.to_csv(CLEANEDDATA_DIR + "census_gini_all.csv", index=False)


def clean_all_approx():
    # TODO: Implement the approximate interpolate method
    pass


if __name__ == "__main__":
    clean_all_const()

