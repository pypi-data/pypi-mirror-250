#!/usr/bin/env python
import pandas as pd   


#####################################################
#           Read csv or excel file as df            #
#####################################################
def read_data_by_path(testPredict_file):
    if testPredict_file is not None:
        file_predix = testPredict_file.name.split('.')[1]
        if file_predix == 'csv':
            df_test = pd.read_csv(testPredict_file)
        if file_predix == 'xlsx':
            df_test = pd.read_excel(testPredict_file)
        else:
            print(f"this function can only handle csv and excel file.")
            df_test = None
        return df_test  
    return None


def greet(name):
    return f"Hello, {name}!"
