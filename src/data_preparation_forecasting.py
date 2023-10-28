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

def data_cleaning_forecasting() -> pd.DataFrame:

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
    df_data = df_data[["Date", "Sales_Qty"]]

    # Drop rows with Sales_Qty = 0
    df_data = df_data[df_data.Sales_Qty != 0]
    
    # Change index
    df_data.set_index("Date", inplace = True)
    
    return df_data

def create_features(df) -> pd.DataFrame:

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

    return df

def main():

    df_data = data_cleaning_forecasting()
    
    # List of filenames
    filename = "df_sales"

    # Construct the filename and save as csv
    filepath = os.path.join(os.getcwd(), "data_forecasting", filename + ".csv")
    df_data.to_csv(filepath, index=True)

    return df_data

if __name__ == "__main__":
    main()


