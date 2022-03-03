import os
import re
import glob
import pandas as pd

RAWDATA_DIR = "../../data/raw-data/"
COUNTY_INCOME_DIR = RAWDATA_DIR + "countyincome/"
CLEANEDDATA_DIR = "../../data/cleaned-data/countyincome/"


def clean_singlefile(file):
    data = pd.read_excel(file).iloc[7:, :10]
    data.columns = ["GEOFIPS", "GEOFIPS_ST", "GEOFIPS_CT", "COUNTY", "NUM_RETURN", "NUM_EXEMPT",
                    "AGI", "WAGES_SALARIES", "DIVIDENDS", "INTEREST"]

    data["GEOFIPS_ST"] = data["GEOFIPS_ST"].astype(int)
    data["GEOFIPS_CT"] = data["GEOFIPS_CT"].astype(int)
    data["GEOFIPS"] = data["GEOFIPS_ST"] * 1000 + data["GEOFIPS_CT"]

    data_cleaned = data[
        ["GEOFIPS", "COUNTY", "NUM_RETURN", "NUM_EXEMPT", "AGI", "WAGES_SALARIES", "DIVIDENDS", "INTEREST"]]

    new_filename = re.findall(r'countyincome/(.*)\.xls', file)[0].replace('\\', '/')
    data_cleaned.to_csv(CLEANEDDATA_DIR + new_filename + ".csv", index=False)


def clean_year(year):
    os.mkdir(CLEANEDDATA_DIR + str(year) + '/')
    for datafile in glob.glob(f"{COUNTY_INCOME_DIR}{year}/*.xls"):
        clean_singlefile(datafile)


def clean_all():
    os.mkdir(CLEANEDDATA_DIR)
    year_list = range(1990, 2010)
    for year in year_list:
        clean_year(year)


if __name__ == "__main__":
    clean_year(2001)
