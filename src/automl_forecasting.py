# Import libraries
import pandas as pd
import sys
import os

FILENAME = "data_sales_processed.csv"
DATA_FOLDER = "../data/processed"
filename = os.path.join(DATA_FOLDER, FILENAME)

def load_data() -> pd.DataFrame:

    """
    Load the processed sales data and return it
    """

    df_sales = pd.read_csv(filename, sep=",")
    df_sales.set_index("Date", inplace=True)
    df_sales.index = pd.to_datetime(df_sales.index)

    return df_sales    

def give_dataframe_information():

    """
    Provide information about the dataframe to decide on the test-train split
    """

    df_sales = load_data()

    # Print min and max of data as well as how many observations are present
    min_date = df_sales.index.min()
    max_date = df_sales.index.max()
    dataframe_length = len(df_sales)

    print(f"Minimum date: {min_date}")
    print(f"Maximum date: {max_date}")
    print(f"Length of the DataFrame: {dataframe_length}")

def train_and_test_split(data, split_date) -> pd.DataFrame:

    """
    Performs the train and test split and return two dataframes (in this order): train, test 
    """

    train = data[data.index <= split_date].copy()
    test = data[data.index > split_date].copy()

    return train, test

