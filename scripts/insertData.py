import pandas as pd
from utilities.sqlalchemy_setup import SessionLocal

csv_file_path = '../netflix_titles.csv'  # Adjust the path as necessary

session = SessionLocal()

