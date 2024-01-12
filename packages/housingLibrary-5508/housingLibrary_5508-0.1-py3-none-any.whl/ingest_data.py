import tarfile

import numpy as np
import pandas as pd


def get_data():
    """Fetches housing data from a given URL and return it.

    Parameters
    -----------
    None

    Returns
    --------
    housing data

    """
    housing = load_housing_data()

    # train_set, test_set = train_test_split(
    # housing, test_size=0.2,
    # random_state=42
    # )

    housing["income_cat"] = pd.cut(
        housing["median_income"],
        bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
        labels=[1, 2, 3, 4, 5],
    )
    return housing


def fetch_housing_data():
    """Fetches housing data

    Parameters
    -----------
    None

    Returns
    --------
    None

    """

    housing_tgz = tarfile.open("housing.tgz", "r:gz")
    for member in housing_tgz.getmembers():
        f = housing_tgz.extractfile(member)
        if f is not None:
            content = f.read()
    housing_tgz.close()
    return content


def load_housing_data():
    """Loads housing data from CSV file.

    Parameters
    -----------

    housing_path : str
    Path to the housing data CSV file.

    Returns
    --------

    pd.DataFrame:Pandas DataFrame containing the loaded housing data.

    """

    return pd.read_csv("./datasets/housing/housing.csv")
