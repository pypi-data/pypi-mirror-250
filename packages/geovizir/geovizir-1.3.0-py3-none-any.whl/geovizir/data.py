import wbdata
import datetime
import pandas as pd

# Fix for Python >= 3.10 until wbdata is updated
import collections
collections.Sequence = collections.abc.Sequence

def get_data(indicator: str, year: int) -> pd.DataFrame:
    """Get data from the World Bank API

    Parameters
    ----------
    indicator : str
        Indicator code
    year : int
        Year

    Returns
    -------
    pandas.DataFrame
        Dataframe with the data
    """
    data_date = datetime.datetime(year, 1, 1), datetime.datetime(year, 12, 31)
    data = wbdata.get_data(indicator, data_date=data_date)
    
    # make a dataframe by iterating over the list of dicts
    df = pd.DataFrame([i for i in data])
    df["country"] = df["country"].apply(lambda x: x["value"])
    df["indicator"] = df["indicator"].apply(lambda x: x["value"])
    df.rename(columns={"date": "year", "countryiso3code": "iso3c"}, inplace=True)

    return df