# Import libraries
import pandas as pd
import sys
import os
# Add the path to the module to the system path
module_path = os.path.join(os.getcwd(), "module_data_prep_forecast")
sys.path.append(module_path)
import data_preparation_forecasting


def get_data():

    # Call the main function to obtain the dataframes
    df_list = data_preparation_forecasting.main()


    # Store the dataframes accordingly
    df_fanshop = df_list[0]
    df_apparel = df_list[1]
    df_golf = df_list[2]
