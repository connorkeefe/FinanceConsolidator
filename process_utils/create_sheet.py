import csv
import sqlite3
from sqlite3 import Error
import glob
import os
import yaml
import json
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

with open('tracker.json', 'r') as f:
    data = json.load(f)

count = data['count']

from datetime import datetime

def convert_date_format(date_string):

    # Parse the date string to a datetime object
    date_obj = datetime.strptime(date_string, '%Y-%m-%d')
    
    # Format the datetime object to a string in 'YYYY-MM' format
    new_date_string = date_obj.strftime('%Y-%m')
    
    return new_date_string


def uniqueID(df, start):
    df["TransactionID"] = None
    for index, row in df.iterrows():
        start = start + 1
        df.at[index, "TransactionID"] = start
    return start

def upload_sheet(df):
    
    # Use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(config['base_path'], config['cert_path']), scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the exact name of the spreadsheet as you've named it
    sheet = client.open("Finance-Tracker")

    worksheet = sheet.worksheet("Transactions_List")

    dataframe = df

    # # Convert DataFrame to a list of lists, where each sublist represents a row in the CSV
    if count == -1:
        data_to_update = [dataframe.columns.values.tolist()] + dataframe.values.tolist()
    else:
        data_to_update = dataframe.values.tolist()

    # # Update the Google Spreadsheet with the CSV data
    worksheet.append_rows(data_to_update)


def create_sheet():
    # database = r"./db/mydb.sqlite"
    df_list = []
    for dirnm in config['accounts']:
        for typeac in config['accounts'][dirnm]:
            path = os.path.join(config['base_path'],f"data/CategorizedCsvs/{dirnm}/{typeac}/")
            if os.path.exists(path):
                # print(typeac)
                csv_files = glob.glob(path + "*csv") 
                
                name = config['accounts'][dirnm][typeac]['name']
                ctype = config['accounts'][dirnm][typeac]['type']

                for cs in csv_files:
                    if cs in data['filenames']:
                        continue
                    else:
                        data['filenames'].append(cs)
                        # Import transactions from a CSV file, using the new account_id for all transactions
                        df = pd.read_csv(cs)
                        df['Account'] = name
                        df['Currency'] = ctype
                        df['Date-Month'] = df['Date'].apply(convert_date_format)
                        data['count'] = uniqueID(df, data['count'])
                        df_list.append(df)
    master_df = pd.DataFrame
    if len(df_list) > 0:              
        master_df = pd.concat(df_list)
    print("Finished creating master df, uploading to sheet:")
    # print(master_df.head())
    with open('tracker.json', 'w') as f:
        json.dump(data, f, indent=4)
    if not master_df.empty:
        upload_sheet(master_df)
    print("Upload to sheet completed")
