import numpy as np
import pandas as pd

CLEANEDDATA_DIR = "../../data/cleaned-data/"


def convert_to_thousands(year, data):
    if year <= 2008:
        return round(data / 1000.0)
    else:
        return data


if __name__ == "__main__":
    v_convert_to_thousands = np.vectorize(convert_to_thousands)

    zipcode_all_gini = pd.read_csv(CLEANEDDATA_DIR + "zipcode_all_gini.csv")
    zipcode_all_gini["agi"] = v_convert_to_thousands(zipcode_all_gini["year"], zipcode_all_gini["agi"])
    zipcode_all_gini["total_tax"] = v_convert_to_thousands(zipcode_all_gini["year"], zipcode_all_gini["total_tax"])

    zipcode_all_gini.to_csv(CLEANEDDATA_DIR + "zipcode_all_gini_corrected.csv", index=False)
