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
    data.dropna(subset=["GEOFIPS_ST", "GEOFIPS_CT"], inplace=True)

    data["GEOFIPS_ST"] = data["GEOFIPS_ST"].astype(int)
    data["GEOFIPS_CT"] = data["GEOFIPS_CT"].astype(int)
    data["GEOFIPS"] = data["GEOFIPS_ST"] * 1000 + data["GEOFIPS_CT"]

    data_cleaned = data[
        ["GEOFIPS", "COUNTY", "NUM_RETURN", "NUM_EXEMPT", "AGI", "WAGES_SALARIES", "DIVIDENDS", "INTEREST"]]

    new_filename = re.findall(r'countyincome/(.*)\.xls', file)[0].replace('\\', '/')
    data_cleaned.to_csv(CLEANEDDATA_DIR + new_filename + ".csv", index=False)

def clean_singlefile_2008_2009(file):
    data = pd.read_excel(file).iloc[6:, :9]
    data.columns = ["GEOFIPS_ST", "GEOFIPS_CT", "COUNTY", "NUM_RETURN", "NUM_EXEMPT",
                    "AGI", "WAGES_SALARIES", "DIVIDENDS", "INTEREST"]

    data.dropna(subset=["GEOFIPS_ST", "GEOFIPS_CT"], inplace=True)

    data["GEOFIPS_ST"] = data["GEOFIPS_ST"].astype(int)
    data["GEOFIPS_CT"] = data["GEOFIPS_CT"].astype(int)
    data["GEOFIPS"] = data["GEOFIPS_ST"] * 1000 + data["GEOFIPS_CT"]

    data_cleaned = data[
        ["GEOFIPS", "COUNTY", "NUM_RETURN", "NUM_EXEMPT", "AGI", "WAGES_SALARIES", "DIVIDENDS", "INTEREST"]]

    new_filename = re.findall(r'countyincome/(.*)\.xls', file)[0].replace('\\', '/')
    data_cleaned.to_csv(CLEANEDDATA_DIR + new_filename + ".csv", index=False)


def clean_singlefile_post2011(file):
    pass


def clean_year(year):
    if not os.path.exists(CLEANEDDATA_DIR + str(year) + '/'):
        os.mkdir(CLEANEDDATA_DIR + str(year) + '/')
    for datafile in glob.glob(f"{COUNTY_INCOME_DIR}{year}/*.xls"):
        if year < 2008:
            clean_singlefile(datafile)
        elif year < 2010:
            clean_singlefile_2008_2009(datafile)
        else:
            raise Exception("Not supported. ")


def clean_all():
    if not os.path.exists(CLEANEDDATA_DIR):
        os.mkdir(CLEANEDDATA_DIR)
    year_list = range(1991, 2008)
    for year in year_list:
        clean_year(year)


if __name__ == "__main__":
    # clean_all()
    clean_year(2009)