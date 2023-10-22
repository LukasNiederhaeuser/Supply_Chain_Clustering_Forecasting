# Import libraries
import pandas as pd
import sys
import os

def load_data() -> pd.DataFrame:

    """ Function to load the transactional data from the working directory
        and returning the dataframe."""

    # Get the directory where the data is stored and load the data
    data_raw_directory = (os.getcwd()+"\data_raw\data_sales.csv")
    df_data = pd.read_csv(filepath_or_buffer = data_raw_directory, sep=",", encoding = "latin-1")

    # Return the loaded data
    return df_data

def data_cleaning_forecasting() -> list:

    """ Function loads the data, adjusts the column names, the datatypes returns the cleaned dataframe. """

    # Call functions to load and subset the data
    df_data = load_data()

    # Rename the columns
    df_data.rename(columns={"data": "Date",
                            "venda": "Sales_Qty",
                            "estoque": "Stock_Qty",
                            "preco": "Price_per_Unit"}, inplace = True)
    
    # Adjust datatype for date-column 
    df_data["Date"] = pd.to_datetime(df_data["Date"], format='%Y/%m/%d')
    
    # Exclude Stock Qty 
    df_data = df_data[["Date", "Sales_Qty", "Price_per_Unit"]]

    # Change index
    df_data.set_index("Date", inplace = True)
    
    return df_data

def main():

    df_data = data_cleaning_forecasting()
    
    # List of filenames
    filename = "df_sales"

    # Construct the filename and save as csv
    filepath = os.path.join(os.getcwd(), "data_forecasting", filename + ".csv")
    df_data.to_csv(filename, index=True)

if __name__ == "__main__":
    main()


