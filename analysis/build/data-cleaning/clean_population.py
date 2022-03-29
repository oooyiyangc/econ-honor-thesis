import os
import re
import glob
import numpy as np
import pandas as pd

RAWDATA_DIR = "../../data/raw-data/"
CLEANEDDATA_DIR = "../../data/cleaned-data/population/"

def import_txt_data():
    headings = ['YEAR', 'GEOFIPS', 'SEX', 'AGE', 'POPULATION']
    colspecs = [(0, 4), (6, 11), (15, 16), (16, 18), (18, None)]
    data = pd.read_fwf(RAWDATA_DIR + "us.1969_2019.19ages.adjusted.txt", names=headings, colspecs=colspecs)
    return data

def import_csv_data():
    data = pd.read_csv(CLEANEDDATA_DIR + "population_data.csv")
    return data


def select_relevant_years(data):
    return data[data["YEAR"] >= 1989]


def select_working_age_population(data):
    return data[(data["AGE"] >= 4) & (data["AGE"] <= 13)].copy()


def process_data(data):
    data = data[data["AGE"] > 0].copy()
    data["POPULATION*AGE"] = (2.5 + 5 * (data["AGE"] - 1)) * data["POPULATION"]
    grouped = data.groupby(["YEAR", "GEOFIPS", "SEX"]).sum()
    grouped["AVERAGE_AGE"] = grouped["POPULATION*AGE"] / grouped["POPULATION"]

    result = grouped.reset_index()[["YEAR", "GEOFIPS", "SEX", "POPULATION", "AVERAGE_AGE"]]
    return result


def generate_features(data):

    data_pivot = pd.pivot_table(data, values=["POPULATION", "AVERAGE_AGE"],
                                index=["YEAR", "GEOFIPS"], columns=["SEX"], aggfunc=np.sum).reset_index()
    data_pivot.columns = data_pivot.columns.droplevel(1)
    data_pivot.columns = ["YEAR", "GEOFIPS", "AVERAGE_AGE_1", "AVERAGE_AGE_2", "POPULATION_1", "POPULATION_2"]
    # data_pivot = data_pivot.sort_values(by=["GEOFIPS", "YEAR"])
    data_pivot["GENDER_RATIO"] = data_pivot["POPULATION_2"] / (data_pivot["POPULATION_1"] + data_pivot["POPULATION_2"])

    data["POPULATION*AVERAGE_AGE"] = data["POPULATION"] * data["AVERAGE_AGE"]
    data_grouped = data.groupby(["YEAR", "GEOFIPS"])[["POPULATION", "POPULATION*AVERAGE_AGE"]].sum().reset_index()

    data_grouped["AVERAGE_AGE"] = data_grouped["POPULATION*AVERAGE_AGE"] / data_grouped["POPULATION"]
    data_grouped = data_grouped.drop("POPULATION*AVERAGE_AGE", axis=1)
    result = data_grouped.merge(data_pivot[["YEAR", "GEOFIPS", "GENDER_RATIO"]],
                                left_on=["YEAR", "GEOFIPS"], right_on=["YEAR", "GEOFIPS"])

    return result


def generate_diff_features(data):

    grouped = data.groupby("GEOFIPS")["YEAR"].count()
    complete_counties = grouped[grouped == 31].index
    data = data[data["GEOFIPS"].isin(complete_counties)]

    data = data.sort_values(by=["GEOFIPS", "YEAR"])

    data_exp = data[["YEAR", "GEOFIPS", "POPULATION"]].copy().set_index(["YEAR", "GEOFIPS"])
    data_exp_chg = data_exp.pct_change().reset_index()
    data_exp_chg = data_exp_chg[data_exp_chg["YEAR"] > 1989]

    data_lin = data[["YEAR", "GEOFIPS", "AVERAGE_AGE", "GENDER_RATIO"]].copy().set_index(["YEAR", "GEOFIPS"])
    data_lin_chg = data_lin.diff().reset_index()
    data_lin_chg = data_lin_chg[data_lin_chg["YEAR"] > 1989]

    result = data_exp_chg.merge(data_lin_chg, left_on=["YEAR", "GEOFIPS"], right_on=["YEAR", "GEOFIPS"])
    return result


def standardize(data):
    data = data[data["GEOFIPS"] < 99999]
    data = data.set_index(["YEAR", "GEOFIPS"])
    for column in data.columns:
        mean = np.mean(data[column])
        stdev = np.std(data[column])
        data[column] = (data[column] - mean) / stdev
    return data.reset_index()


def expand_years(data):
    original_cols = ["POPULATION_x", "AVERAGE_AGE_x", "GENDER_RATIO_x",
                     "POPULATION_y", "AVERAGE_AGE_y", "GENDER_RATIO_y"]
    data_pivot = pd.pivot_table(data, values=original_cols,
                                index=["GEOFIPS"], columns=["YEAR"], aggfunc=np.sum).reset_index()
    # data_pivot = data_pivot.reset_index()
    print(data_pivot.head())
    data_pivot.columns = data_pivot.columns.droplevel(1)

    cols = ["GEOFIPS"]
    for col in original_cols:
        for year in range(1990, 2020):
            cols += [col + "_" + str(year)]
    data_pivot.columns = cols

    return data_pivot


def featurize(data, std=True):
    result = generate_features(data)
    result_chg = generate_diff_features(result)

    if std:
        standardized = standardize(result_chg)
    else:
        standardized = result_chg

    return standardized


if __name__ == "__main__":
    # data = select_relevant_years(import_txt_data())
    # print(data.shape)
    # print(data.head())
    # data.to_csv(CLEANEDDATA_DIR + "population_data.csv", index=False)

    # data = import_csv_data()
    # print(data.shape)
    #
    # res_all = process_data(data)
    # print(res_all.shape)
    # res_all.to_csv(CLEANEDDATA_DIR + "population_clustered_all.csv", index=False)
    #
    # res_working = process_data(select_working_age_population(data))
    # print(res_working.shape)
    # res_working.to_csv(CLEANEDDATA_DIR + "population_clustered_working.csv", index=False)

    data_all = pd.read_csv(CLEANEDDATA_DIR + "population_clustered_all.csv")
    standardized_all = featurize(data_all)
    population_diff_all = featurize(data_all, std=False)
    print(standardized_all.head())

    data_working = pd.read_csv(CLEANEDDATA_DIR + "population_clustered_working.csv")
    standardized_working = featurize(data_working)
    population_diff_working = featurize(data_working, std=False)
    print(standardized_working.head())

    # psm
    standardized = standardized_all.merge(standardized_working,
                                          left_on=["YEAR", "GEOFIPS"], right_on=["YEAR", "GEOFIPS"])



    standardized = expand_years(standardized)
    print(standardized.head())

    standardized.to_csv(CLEANEDDATA_DIR + "population_featurized.csv", index=False)

    # robustness
    population_diff = population_diff_all.merge(population_diff_working,
                                                left_on=["YEAR", "GEOFIPS"], right_on=["YEAR", "GEOFIPS"])
    population_diff.to_csv(CLEANEDDATA_DIR + "population_diff.csv", index=False)

