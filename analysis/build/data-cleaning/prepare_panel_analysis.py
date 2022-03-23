import os
import re
import glob
import numpy as np
import pandas as pd

def merge_income_and_gini(income, gini):
    merged = income.merge(gini, how="inner", left_on=["YEAR", "GEOFIPS"], right_on=["YEAR", "GEOFIPS"])
    year_count = merged.groupby("GEOFIPS")["YEAR"].count()
    valid_counties = np.array(year_count[year_count == 31].index)
    print(f"There are {len(valid_counties)} out of {len(year_count)} counties with complete data.")
    merged_complete = merged[merged["GEOFIPS"].isin(valid_counties)]
    merged_complete = merged_complete[
        ["YEAR", "GEOFIPS", "GINI", "NUM_RETURN", "NUM_EXEMPT", "AGI", "WAGES_SALARIES", "DIVIDENDS", "INTEREST"]]

    return merged_complete

if __name__ == "__main__":
    DATA_DIR = "../../data/cleaned-data/"
    income = pd.read_csv(DATA_DIR + "countyincome_merged.csv")
    gini = pd.read_csv(DATA_DIR + "census_gini_all_const.csv")
    merged = merge_income_and_gini(income, gini)
    merged.to_csv(DATA_DIR + "countyincome_gini_const.csv", index=False)