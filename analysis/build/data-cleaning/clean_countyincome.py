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


def clean_singlefile_post2010(file):
    data = pd.read_csv(file, encoding='latin-1')
    data["GEOFIPS"] = data["STATEFIPS"] * 1000 + data["COUNTYFIPS"]
    data_cleaned = data[["GEOFIPS", "COUNTYNAME", "N1", "N2", "A00100", "A00200", "A00600", "A00300"]].copy()
    data_cleaned.rename(columns={"COUNTYNAME": "COUNTY", "N1": "NUM_RETURN", "N2": "NUM_EXEMPT",
                            "A00100": "AGI", "A00200": "WAGES_SALARIES",
                            "A00600": "DIVIDENDS", "A00300": "INTEREST"},
                        inplace=True)
    new_filename = re.findall(r'countyincome/(.*)\.csv', file)[0].replace('\\', '/')
    data_cleaned.to_csv(CLEANEDDATA_DIR + new_filename + ".csv", index=False)


def clean_year(year):
    if not os.path.exists(CLEANEDDATA_DIR + str(year) + '/'):
        os.mkdir(CLEANEDDATA_DIR + str(year) + '/')
    if year < 2010:
        for datafile in glob.glob(f"{COUNTY_INCOME_DIR}{year}/*.xls"):
            if year < 2008:
                clean_singlefile(datafile)
            else:
                clean_singlefile_2008_2009(datafile)

    else:
        clean_singlefile_post2010(f"{COUNTY_INCOME_DIR}{year}/{year % 100}incyallnoagi.csv")


def clean_all():
    if not os.path.exists(CLEANEDDATA_DIR):
        os.mkdir(CLEANEDDATA_DIR)
    year_list = range(1989, 2020)
    for year in year_list:
        clean_year(year)


if __name__ == "__main__":
    clean_all()
    # clean_year(2019)