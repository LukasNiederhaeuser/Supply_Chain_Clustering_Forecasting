# Import libraries
import pandas as pd
import sys
import os

FILENAME = "data_sales.csv"
DATA_FOLDER = "../data/raw"
filename = os.path.join(DATA_FOLDER, FILENAME)

def load_data() -> pd.DataFrame:

    """ 
    Function to load the transactional data from the working directory and return the dataframe
    """

    # Get the directory where the data is stored and load the data
    df_data = pd.read_csv(filename, sep=",", encoding = "latin-1")
    # Rename the columns
    df_data = df_data[["data", "venda"]]
    df_data.rename(columns={"data": "Date",
                            "venda": "Sales_Qty"},
                            inplace = True)
    # Drop rows with Sales_Qty = 0
    df_data = df_data[df_data.Sales_Qty != 0]
    # Change index
    df_data.set_index("Date", inplace = True)
    df_data.index = pd.to_datetime(df_data.index)    
    # Freqency Argument for pycaret
    df_data = pd.DataFrame(df_data, index=pd.date_range(start=df_data.index.min(), periods=len(df_data), freq='D'))
    df_data = df_data.fillna(method = "ffill")

    return df_data