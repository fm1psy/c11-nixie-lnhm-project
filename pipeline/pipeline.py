"""ETL Pipeline script"""
from extract import extract_data
from transform import transform
from load import loading_main

if __name__ == "__main__":
    extract_data()
    transform()
    loading_main()
