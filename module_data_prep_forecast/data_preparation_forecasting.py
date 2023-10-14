# Import libraries
import pandas as pd
import sys
import os

def load_data() -> pd.DataFrame:

    """ Function to load the transactional data from the working directory
        and returning the dataframe."""

    # Get the directory where the data is stored
    data_raw_directory = (os.getcwd()+"\data_raw")
    # List all files in the directory
    file_list = os.listdir(data_raw_directory)
    # Read the csv-file --> Use latin-1 encoding instead of utf-8 encoding
    df_data = pd.read_csv(filepath_or_buffer = os.path.join(data_raw_directory, file_list[0]),
                        sep=",",
                        encoding = "latin-1")

    # Return the loaded data
    return df_data

def subset_data(df_data) -> list:

    # Subset for complete orders
    df_data = df_data[df_data["Order Status"] == "COMPLETE"]

    # Create three dataframes for each department
    df_apparel = df_data[df_data["Department Name"] == "Apparel"]
    df_fanshop = df_data[df_data["Department Name"] == "Fan Shop"]
    df_golf = df_data[df_data["Department Name"] == "Golf"]

    return df_apparel, df_fanshop, df_golf

def data_cleaning_forecasting() -> list:

    """ Function to clean the  """

    # Call functions to load and subset the data
    df_data = load_data()
    df_apparel, df_fanshop, df_golf = subset_data(df_data)
    df_list = [df_apparel, df_fanshop, df_golf]

    # Empty list to store the cleand dataframes into
    df_list_cleaned = []
    
    for df in df_list:
        # Columns to keep 
        df = df[["order date (DateOrders)",
                 "Sales per customer",
                 "Order Item Quantity"]]
    
        # Adjust datatype for date-column --> order date (DateOrders)
        df["order date (DateOrders)"] = pd.to_datetime(df["order date (DateOrders)"], format='%m/%d/%Y %H:%M')
        df["order date (DateOrders)"] = df["order date (DateOrders)"].dt.date.astype('datetime64[ns]')

        # Rename the columns
        df.rename(columns={"order date (DateOrders)": "Date",
                           "Sales per customer": "Sales_Value",
                           "Order Item Quantity": "Sales_Qty"}, inplace = True)
        
        # Aggregate the dataframe by date and sum qty and value
        df = df.groupby(['Date']).sum()

        # Slice the dataframe on the time-index
        start_date = pd.to_datetime('2015-01-01')
        end_date = pd.to_datetime('2017-10-01')
        df = df.loc[start_date:end_date]

        # Append cleaned dataframe to list
        df_list_cleaned.append(df)

    return df_list_cleaned

def main():

    df_list_cleaned = data_cleaning_forecasting()
    
    # List of filenames
    filenames = ["data_fanshop", "data_apparel", "data_golf"]

    # Construct the filename and save as csv
    for i, name in enumerate(filenames):
        filename = os.path.join(os.getcwd(), "data_forecasting", name + ".csv")
        df_list_cleaned[i].to_csv(filename, index=True)

    return df_list_cleaned

if __name__ == "__main__":
    main()


