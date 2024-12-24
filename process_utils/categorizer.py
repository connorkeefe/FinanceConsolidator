import openai
from openai import OpenAI
import os
import glob
import pandas as pd
import glob
import yaml



with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

client = OpenAI()

def categorize_transaction(description, context=None):

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"{context}",
            },
            {
                "role": "user",
                "content": f"{description}"
            }
        ],
        model="gpt-3.5-turbo",
    )
    
    return chat_completion.choices[0].message.content

def categorizer(df, grandparent, parent, fname):
    context = config['accounts'][grandparent][parent]['context']
    fname = "categorized_" + fname
    output_file_name = f"data/CategorizedCsvs/{grandparent}/{parent}/{fname}"
    if not(os.path.exists(output_file_name)):    
        df['Category'] = df['Description'].apply(categorize_transaction, context=context)
        df.to_csv(output_file_name, index=False)
        print(f"Categorized file saved as {output_file_name}")
    else:
        print(f"Categorized file: {output_file_name} already exists")

