from typing import Optional

import pandas as pd
from typeguard import typechecked


@typechecked
def load_dataset(filepath: str, verbose: Optional[bool] = False) -> pd.DataFrame:
    """
    # Load dataset

    Load a dataset from a local file.

    ## Arguments:

    - filepath: `str`. Path to the dataset file
    - verbose: `bool`, `Optional`. Determining level of information returned to the user. Default is False.
    """
    df = pd.read_csv(filepath)
    if verbose:
        print("Dataset loaded:")
        print(df)
    return df
