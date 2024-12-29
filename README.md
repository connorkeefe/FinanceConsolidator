### Environment setup

#### Python requirements
Navigate to the project folder:

```pip install requirements.txt```

#### Get API key for OpenAI

1. Go to openai developer page https://platform.openai.com/api-keys
2. Login and create a new secret key
3. Set it as an environment variable (MacOS):
```export OPENAI_API_KEY="your-api-key-here"```

#### Get API key for Google Sheets

1. Go to the Google Developers Console. https://console.cloud.google.com/apis/dashboard
2. Login and Create a new project.
3. Enable the Google Sheets API for your project.
4. Create credentials (service account key) for your project.
5. Download the JSON file containing your credentials.
6. Create a google sheet in the main google drive directory
7. In the sheet you wish to update paste in the following column names:
**Date,	Description,	Amount,	Type,	Category,	Account,	Currency,	Date-Month,	TransactionID**
8. Share your Google spreadsheet you wish to update with the **client_email** address from your service account (found in your JSON credentials file).

#### config.yml

update the **base_path** with the path to the project folder

update the **cert_path** with the path to the Google sheet json credential file

update the **file_name** with the name of your google sheet, should be in main google drive directory

update the **sheet_name** with the name of the sheet you want to update inside the file

### Usage

#### Available accounts

Check config to see if the accounts you would need to scrape are present, if not this project would have to be updated to handle these statements

#### Inputting the data

For all accounts accept the RBC credit card you will need to place the monthly pdf statements in the following directories inside the project folder:

##### Bank Account
Up until February 2024 use these two folders for BMO chequing account and savings account statemnts

```mkdir data/Statements/Bank Account/BMO Sav``` 

```mkdir data/Statements/Bank Account/BMO Chq```

After February 2024, BMO Checking and Saving statements are combined so only need to download for one of the accounts and place it in combined folder:

```mkdir data/Statements/Bank Account/BMO Comb```

```mkdir data/Statements/Bank Account/BMO USD```

```mkdir data/Statements/Bank Account/RBC Chq```

##### Credit Cards

```mkdir data/Statements/Credit Cards/BMO CAD```

```mkdir data/Statements/Credit Cards/BMO US```

For the RBC Avion credit card you will need to download the full details csv which will have all your historical transactions and put it in the following directory:

```mkdir data/csvs/Credit Cards/RBC```

#### RUN

```python new_data_add.py```


