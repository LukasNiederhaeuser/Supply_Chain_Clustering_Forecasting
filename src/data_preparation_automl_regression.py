# Import libraries
import pandas as pd
import sys
import os


# Raw data
DATA_FOLDER_RAW = "../data/raw"
FILENAME_RAW = "data_sales.csv"
filename_raw = os.path.join(DATA_FOLDER_RAW, FILENAME_RAW)

# Processed data
DATA_FOLDER_PROCESSED = "../data/processed"
FILENAME_PROCESSED = "data_sales_processed.csv"
filename_processed = os.path.join(DATA_FOLDER_PROCESSED, FILENAME_PROCESSED)


def load_raw_data() -> pd.DataFrame:

    """ 
    Function to load the transactional data from the working directory and return the dataframe
    """

    # Get the directory where the data is stored and load the data
    df_data = pd.read_csv(filename_raw, sep=",", encoding = "latin-1")

    return df_data


def data_cleaning_forecasting() -> pd.DataFrame:

    """
    Function loads the data, adjusts the column names and filters unnecessary data. It then returns the dataframe
    """

    # Call functions to load and subset the data
    df_data = load_raw_data()

    # Rename the columns
    df_data.rename(columns={"data": "Date",
                            "venda": "Sales_Qty",
                            "estoque": "Stock_Qty",
                            "preco": "Price_per_Unit"}, inplace = True)
    
    # Adjust datatype for date-column 
    df_data["Date"] = pd.to_datetime(df_data["Date"])
    
    # Exclude Stock Qty 
    df_data = df_data[["Date", "Sales_Qty"]]

    # Drop rows with Sales_Qty = 0
    df_data = df_data[df_data.Sales_Qty != 0]
    
    # Change index
    df_data.set_index("Date", inplace = True)
    
    return df_data


def create_features():

    """
    Function creates date-based features in the dataframe and saves the dataframe in the data/processed folder
    """

    df = data_cleaning_forecasting()

    # Create features for year, quarter etc.
    df["Year"] = df.index.year
    df["Quarter"] = df.index.quarter
    df["Month"] = df.index.month
    df["Day_of_Week"] = df.index.dayofweek

    # Create lag features for the past 1, 7, and 30 days
    df['lag_1_day'] = df['Sales_Qty'].shift(1)
    df['lag_7_days'] = df['Sales_Qty'].shift(7) 
    df['lag_30_days'] = df['Sales_Qty'].shift(30)

    # Drop the rows where there is a missing value
    df.dropna(inplace = True)

    # Convert evertyhing to integer
    column_data_types = {col: 'int' for col in df.columns}
    df = df.astype(column_data_types)

    try:
        file_path = os.path.join(DATA_FOLDER_PROCESSED, "data_sales_processed.csv")
        df.to_csv(file_path)
        print("Processed version of data_sales.csv successfully saved in folder")
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Saving unsuccessful")


def load_processed_data() -> pd.DataFrame:

    """ 
    Function to load the processed data for forecasting and return the dataframe
    """

    # Get the directory where the data is stored and load the data
    df_data = pd.read_csv(filename_processed, sep=",", encoding = "latin-1")
    df_data.set_index("Date", inplace=True)
    df_data.index = pd.to_datetime(df_data.index)

    return df_data


def give_dataframe_information(df):

    """
    Provide information about the dataframe to decide on the test-train split
    """
    # Print min and max of data as well as how many observations are present
    min_date = df.index.min()
    max_date = df.index.max()
    dataframe_length = len(df)

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