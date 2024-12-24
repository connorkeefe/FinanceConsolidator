import fitz  # PyMuPDF
import pandas as pd
import glob
from io import StringIO
import os
import yaml

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

import re

def detect_date_format_credit(s):
    # Regex pattern explanation:
    # - (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.: Matches abbreviated month names followed by a period.
    # - \s: Matches a whitespace character.
    # - (?:3[01]|[12][0-9]|0?[1-9]): Non-capturing group for dates: 01-31, allowing for a leading zero or not.
    # - The entire month and date pattern is repeated twice, with a space in between.
    pattern = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\. (?:3[01]|[12][0-9]|0?[1-9]) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\. (?:3[01]|[12][0-9]|0?[1-9])"
    
    # Search for the pattern in the string
    match = re.search(pattern, s)
    
    # If a match is found, return True; otherwise, False
    return bool(match)

def detect_date_format_bank(s):
    # Regex pattern explanation:
    # - (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.: Matches abbreviated month names followed by a period.
    # - \s: Matches a whitespace character.
    # - (?:3[01]|[12][0-9]|0?[1-9]): Non-capturing group for dates: 01-31, allowing for a leading zero or not.
    # - The entire month and date pattern is repeated twice, with a space in between.
    pattern = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (?:3[01]|[12][0-9]|0?[1-9])"
    
    # Search for the pattern in the string
    match = re.search(pattern, s)
    
    # If a match is found, return True; otherwise, False
    return bool(match)

def detect_date_format_bank_rbc(s):
    # Regex pattern explanation:
    # - (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.: Matches abbreviated month names followed by a period.
    # - \s: Matches a whitespace character.
    # - (?:3[01]|[12][0-9]|0?[1-9]): Non-capturing group for dates: 01-31, allowing for a leading zero or not.
    # - The entire month and date pattern is repeated twice, with a space in between.
    pattern = r"(?:3[01]|[12][0-9]|0?[1-9]) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
    
    # Search for the pattern in the string
    match = re.search(pattern, s)
    
    # If a match is found, return True; otherwise, False
    return bool(match)
    

def starts_with_digit(s):
    # Create a tuple of string digits
    digits = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    # Use startswith() to check if the string starts with any digit
    return s.startswith(digits)

def starts_with_digit_rbc(s):
    s = s.replace('.', '')
    s = s.replace(',', '')

    # Create a tuple of string digits
    digits = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    # Use startswith() to check if the string starts with any digit
    return s.isdigit()


def parse_transactions_credit(f):
    # Assuming each line contains a transaction: Date, Description, Amount
    # Adjust the parsing logic based on your statement's format
    text = extract_text_from_pdf(f)
    data = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        # print(line)
        # print(detect_date_format(line))
        isdate = detect_date_format_credit(line)
        if isdate and (i < (len(lines) - 3)):
            date = line
            description = lines[i+1]
            if starts_with_digit(lines[i+2]) and (detect_date_format_credit(lines[i+3]) or ('Subtotal' in lines[i+3]) or ('(continued' in lines[i+3])):
                amount = lines[i+2]
            else:
                description = description + ' ' + lines[i+2]
                amount = lines[i+3]

            data.append([date, description, amount])
    
    # Convert to DataFrame for easier handling
    df = pd.DataFrame(data, columns=['Date', 'Description', 'Amount'])
    return df

def parse_transactions_bank(f):
    # Assuming each line contains a transaction: Date, Description, Amount
    # Adjust the parsing logic based on your statement's format
    text = extract_text_from_pdf(f)
    data = []
    lines = text.split('\n')
    previous_balance = None
    current_bal = None
    for i, line in enumerate(lines):
        # print(line)
        # print(detect_date_format_bank(line))
        isdate = detect_date_format_bank(line)
        if isdate and (i < (len(lines) - 3)):
            date = line
            description = lines[i+1]
            amount = None
            if description == 'Opening balance' or description == 'Opening Balance':
                previous_balance = lines[i+2]
                continue
            if description == 'Closing totals' or description == 'Closing Balance':
                break
            if starts_with_digit(lines[i+2]) and starts_with_digit(lines[i+3]):
                amount = lines[i+2]
                current_bal = lines[i+3]
                if float(current_bal.replace(',','')) > float(previous_balance.replace(',','')):
                    amount = amount + ' CR'
                previous_balance = current_bal
            if starts_with_digit(lines[i+3]) and starts_with_digit(lines[i+4]) and previous_balance != None:
                description = description + lines[i+2]
                amount = lines[i+3]
                current_bal = lines[i+4]
                if float(current_bal.replace(',','')) > float(previous_balance.replace(',','')):
                    amount = amount + ' CR'
                previous_balance = current_bal
            if amount != None:
                data.append([date, description, amount])
    
    # Convert to DataFrame for easier handling
    df = pd.DataFrame(data, columns=['Date', 'Description', 'Amount'])
    return df

def parse_transactions_bank_rbc(f):
    # Assuming each line contains a transaction: Date, Description, Amount
    # Adjust the parsing logic based on your statement's format
    text = extract_text_from_pdf(f)
    data = []
    lines = text.split('\n')
    # print(lines)
    previous_balance = None
    current_bal = None
    for i, line in enumerate(lines):
        # print(line)
        # print(detect_date_format_bank(line))
        if line == 'Opening Balance':
            previous_balance = lines[i+1]
            continue
        if line == 'Closing Balance':
            break
        isdate = detect_date_format_bank_rbc(line)
        if isdate and (i < (len(lines) - 3)):
            date = line
            description = lines[i+1]
            amount = None
            if starts_with_digit_rbc(lines[i+2]) and starts_with_digit_rbc(lines[i+3]):
                amount = lines[i+2]
                current_bal = lines[i+3]
                if float(current_bal.replace(',','')) > float(previous_balance.replace(',','')):
                    amount = amount + ' CR'
                previous_balance = current_bal
            elif starts_with_digit_rbc(lines[i+3]) and starts_with_digit_rbc(lines[i+4]) and previous_balance != None:
                description = description + lines[i+2]
                amount = lines[i+3]
                current_bal = lines[i+4]
                if float(current_bal.replace(',','')) > float(previous_balance.replace(',','')):
                    amount = amount + ' CR'
                previous_balance = current_bal
            if amount != None:
                data.append([date, description, amount])
    
    # Convert to DataFrame for easier handling
    df = pd.DataFrame(data, columns=['Date', 'Description', 'Amount'])
    return df

function_map = {
    "Credit Cards": parse_transactions_credit,
    "Bank Account": parse_transactions_bank,
    "RBC": parse_transactions_bank_rbc
}

def scraper(statementPath):
    files = glob.glob(f'{statementPath}/*/*/*.pdf')

    for f in files:
        parent_path = os.path.dirname(f)
        parent_name = os.path.basename(parent_path)
        grandparent_path = os.path.dirname(parent_path)
        grandparent_name = os.path.basename(grandparent_path)
        funname = grandparent_name
        if 'RBC' in parent_name:
            funname = 'RBC'
        fname = os.path.basename(f).replace('.pdf','.csv')
        function = function_map.get(funname)
        output_file_name = f'data/csvs/{grandparent_name}/{parent_name}/{fname}'
        if not(os.path.exists(output_file_name)):
            transactions_df = function(f)
            transactions_df.to_csv(output_file_name, index=False)
            print(f"Scraped file saved as {output_file_name}")
