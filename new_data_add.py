import yaml
from process_utils import scraper
from process_utils import cleanerCategorizer
from process_utils import create_sheet

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

if __name__ == "__main__":
    main_dir = config['base_path']
    statements = f"{main_dir}data/Statements"
    scraper(statements)
    csvs = f"{main_dir}data/csvs"
    cleanerCategorizer(csvs)
    create_sheet()
