# Import libraries
import pandas as pd
import sys
import os
# Import the costum module
module_path = os.path.join(os.getcwd(), "module_data_prep_forecast")
sys.path.append(module_path)
import data_preparation_forecasting


def get_data():

    # Call the main function to obtain the dataframes
    df_list = data_preparation_forecasting.main()
    
    return df_list

df_list = get_data()
print(df_list[0].head(5))
