import sys

import numpy as np
import pandas as pd

from progress_bar import *

CLEANEDDATA_DIR = "../../data/cleaned-data/"


def compute_gini(aggregate_measures, data_subset):
    data_subset.sort_values(by=["agi_class"], ascending=True, inplace=True)
    p_num_exempt = []
    p_total_tax = []
    for idx in range(data_subset.shape[0]):
        num_exempt = data_subset.loc[data_subset.index[idx], "n2"] / aggregate_measures[0]
        p_num_exempt.append(num_exempt)
        total_tax = data_subset.loc[data_subset.index[idx], "total_tax"] / aggregate_measures[1]
        p_total_tax.append(total_tax)
    cum_num_exempt = np.cumsum(p_num_exempt)
    cum_total_tax = np.cumsum(p_total_tax)
    return 1.0 - 2.0 * approximate_integral(cum_num_exempt, cum_total_tax)


def approximate_integral(x, y):
    x = np.insert(x, 0, 0)
    x = np.insert(x, -1, 1)
    y = np.insert(y, 0, 0)
    y = np.insert(y, -1, 1)
    assert len(x) == len(y), "Array length mismatch. "

    area = 0
    for idx in range(len(x) - 1):
        area += (y[idx] + y[idx + 1]) * (x[idx + 1] - x[idx]) / 2.0
    return area


def group_sum(data):
    aggregate_data = data.groupby(["year", "zipcode"]).sum().reset_index()
    return aggregate_data


if __name__ == "__main__":
    data = pd.read_csv(CLEANEDDATA_DIR + "zipcode_all.csv")
    aggregate_data = group_sum(data)
    gini = []

    start_progress("Computing")

    for idx in range(aggregate_data.shape[0]):
        row = aggregate_data.iloc[idx].copy()
        zipcode = row["zipcode"]
        year = row["year"]
        if idx % 1000 == 0:
            progress(idx / aggregate_data.shape[0] * 100)
        data_subset = data[(data["zipcode"] == zipcode) & (data["year"] == year)].copy()
        aggregate_measures = \
            aggregate_data[(aggregate_data["zipcode"] == zipcode) & (aggregate_data["year"] == year)].copy().iloc[0]
        gini.append(compute_gini(list(aggregate_measures[["n2", "total_tax"]]), data_subset))

    end_progress()

    aggregate_data["gini"] = gini
    aggregate_data.to_csv(CLEANEDDATA_DIR + "zipcode_all_gini.csv", index=False)
