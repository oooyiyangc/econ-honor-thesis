import os
import glob
import re

import pandas as pd

CLEANEDDATA_DIR = "../../data/cleaned-data/zipcodeincome/"


def merge_all():
    path = CLEANEDDATA_DIR
    merged = pd.DataFrame()
    zipcode_set = set(())
    for datafile in glob.glob(f"{path}/*.csv"):
        print(re.findall(r'zipcode\d*\.csv', datafile)[0])

        data = pd.read_csv(datafile)
        data_columns = ["zipcode", "n1", "n2", "a00100"]
        if "a09200" in data.columns:
            data_columns.append("a09200")
            data["a09200"] = data["a09200"] * 1000
            data["a00100"] = data["a00100"] * 1000
        else:
            data_columns.append("a10300")

        if "agi_stub" in data.columns:
            data_columns.append("agi_stub")
        else:
            data_columns.append("agi_class")
        data = data[data_columns].dropna(subset=["zipcode"])
        data.rename(columns={data_columns[3]: "agi",
                             data_columns[4]: "total_tax",
                             data_columns[5]: "agi_class"},
                    inplace=True)

        data["year"] = [re.findall(r'zipcode(\d*)\.csv', datafile)[0]] * data.shape[0]

        if (len(zipcode_set) == 0):
            zipcode_set = set(data["zipcode"].unique())
        zipcode_set = zipcode_set.intersection(set(data["zipcode"].unique()))
        merged = pd.concat([merged, data])

    print(len(zipcode_set))
    output = merged.reset_index(drop=True)
    output = output[output["zipcode"].isin(list(zipcode_set))]
    output.to_csv(CLEANEDDATA_DIR + "zipcodeincome/zipcode_all.csv", index=False)


if __name__ == "__main__":
    merge_all()