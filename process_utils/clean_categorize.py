import pandas as pd
from dateutil.parser import parse
import os
import glob
from .categorizer import categorizer


def convert_date_field_bmo(col_str, year=[]):
    col_str = col_str.strip()
    date_split = col_str.split()
    if len(year) == 2:
        if 'Dec' in date_split[0]:
            date_str = date_split[0] + ' ' + date_split[1] + ' ' + year[0].strip()
        else:
            date_str = date_split[0] + ' ' + date_split[1] + ' ' + year[1].strip()
    else:
        date_str = date_split[0] + ' ' + date_split[1] + ' ' + year[0].strip()
    
    # Parse the first date and format it into YYYY-MM-DD, assuming the year is 2023
    # Adjust the year as necessary
    first_date = parse(date_str).strftime('%Y-%m-%d')
    
    return first_date

def convert_date_field_rbc(col_str):
    # Parse the first date and format it into YYYY-MM-DD, assuming the year is 2023
    date = parse(col_str).strftime('%Y-%m-%d')
    return date

def convert_date_field_rbc_bank(col_str, year=[]):
    col_str = col_str.strip()
    date_split = col_str.split()
    if len(year) == 2:
        if 'Dec' in date_split[1]:
            date_str = date_split[1] + ' ' + date_split[0] + ' ' + year[0].strip()
        else:
            date_str = date_split[1] + ' ' + date_split[0] + ' ' + year[1].strip()
    else:
        date_str = date_split[1] + ' ' + date_split[0] + ' ' + year[0].strip()
    
    # Parse the first date and format it into YYYY-MM-DD, assuming the year is 2023
    # Adjust the year as necessary
    first_date = parse(date_str).strftime('%Y-%m-%d')
    
    return first_date

    

def convert_amount_bmo(col_val):
    col_val = str(col_val)
    col_val = col_val.strip()
    content = col_val.split()
    if len(content) > 1 and content[1] == 'CR':
        return float(content[0].replace(',', ''))
    else:
        return -1 * float(content[0].replace(',', ''))

def convert_amount_rbc_credit(col_val):
    col_val = col_val.strip()
    col_val = col_val.replace('$','').replace(',', '')
    if '(' in col_val:
        return float(col_val.replace('(', '').replace(')',''))
    else:
        return -1 * float(col_val)

def convert_amount_rbc_bank(col_val):
    col_val = col_val.strip()
    col_val = col_val.replace('$','').replace(',', '')
    if '(' in col_val:
        return -1 * float(col_val.replace('(', '').replace(')',''))
    else:
        return float(col_val)

def get_type(col_val):
    if col_val <= 0:
        return 'Expense'
    else:
        return 'Income'



def bmo_credit_process_csv(input_file_name, parent_path):
    # Load the CSV file
    df = pd.read_csv(input_file_name)
    parent_name = os.path.basename(parent_path)
    grandparent_path = os.path.dirname(parent_path)
    grandparent_name = os.path.basename(grandparent_path)
    fname = os.path.basename(input_file_name)
    if 'Jan' in fname:
        year = fname.split(',')[1].replace('.csv', '')
        year = [str(int(year)-1), year]
    else:
        year = [fname.split(',')[1].replace('.csv', '')]
    # Assuming the date fields are in a column named 'DateField'
    # Update the column with the converted first date
    df['Date'] = df['Date'].apply(convert_date_field_bmo, year=year)
    
    # Update amount
    df['Amount'] = df['Amount'].apply(convert_amount_bmo)

    # Update type
    df['Type'] = df['Amount'].apply(get_type)
    
    # Save the updated DataFrame to a new CSV file
    # output_file_name = f"data/cleanCsvs/{grandparent_name}/{parent_name}/processed_{fname}"
    # df.to_csv(output_file_name, index=False)
    # print(f"Cleaned file saved as {output_file_name}")
    print(f"Cleaned file {fname}")
    return categorizer(df, grandparent_name, parent_name, fname)

def rbc_credit_process_csv(input_file_name, parent_path):
    # Load the CSV file
    df = pd.read_csv(input_file_name)
    df = df.dropna(subset=['Amount'])
    parent_name = os.path.basename(parent_path)
    grandparent_path = os.path.dirname(parent_path)
    grandparent_name = os.path.basename(grandparent_path)
    fname = os.path.basename(input_file_name)
    
    # Assuming the date fields are in a column named 'DateField'
    # Update the column with the converted first date
    df['Date'] = df['Date'].apply(convert_date_field_rbc)
    
    # Update amount
    df['Amount'] = df['Amount'].apply(convert_amount_rbc_credit)
    

    # Update type
    df['Type'] = df['Amount'].apply(get_type)
    
    # Save the updated DataFrame to a new CSV file
    # output_file_name = f"data/cleanCsvs/{grandparent_name}/{parent_name}/processed_{fname}"
    # df.to_csv(output_file_name, index=False)
    # print(f"Cleaned file saved as {output_file_name}")
    print(f"Cleaned file {fname}")
    return categorizer(df, grandparent_name, parent_name, fname)

def rbc_bank_process_csv(input_file_name, parent_path):
    # Load the CSV file
    df = pd.read_csv(input_file_name)
    parent_name = os.path.basename(parent_path)
    grandparent_path = os.path.dirname(parent_path)
    grandparent_name = os.path.basename(grandparent_path)
    fname = os.path.basename(input_file_name)
    if '-01-' in fname:
        year = fname.split()[2].replace('.csv', '')
        year = year.split('-')[0]
        year = [str(int(year)-1), year]
    else:
        year = fname.split()[2].replace('.csv', '')
        year = [year.split('-')[0]]
    # Assuming the date fields are in a column named 'DateField'
    # Update the column with the converted first date
    df['Date'] = df['Date'].apply(convert_date_field_rbc_bank, year=year)
    
    # Update amount
    df['Amount'] = df['Amount'].apply(convert_amount_bmo)

    # Update type
    df['Type'] = df['Amount'].apply(get_type)
    
    # Save the updated DataFrame to a new CSV file
    # output_file_name = f"data/cleanCsvs/{grandparent_name}/{parent_name}/processed_{fname}"
    # df.to_csv(output_file_name, index=False)
    # print(f"Cleaned file saved as {output_file_name}")
    print(f"Cleaned file {fname}")
    return categorizer(df, grandparent_name, parent_name, fname)

function_map = {
    "BMO US": bmo_credit_process_csv,
    "BMO CAD": bmo_credit_process_csv,
    "RBC": rbc_credit_process_csv,
    "BMO Chq": bmo_credit_process_csv,
    "BMO Sav": bmo_credit_process_csv,
    "BMO USD": bmo_credit_process_csv,
    "RBC Chq": rbc_bank_process_csv
}

# # Example usage
# file_name = "October 20, 2023.csv"  # Update this with your actual file name
# process_csv(file_name)

def cleanerCategorizer(csvPath):
    files = glob.glob(f'{csvPath}/*/*/*.csv')
    for f in files:
        parent_path = os.path.dirname(f)
        parent_name = os.path.basename(parent_path)
        function = function_map.get(parent_name)
        function(f, parent_path)