"""ETL Pipeline script"""
from extract import extract_data
from transform import transform
from load import loading_main


def lambda_handler(event=None, context=None) -> dict:
    """ LAMBDA HANDLER!!! """
    try:
        extract_data()
        print("extract done.")
        transform()
        print("transform done.")
        loading_main()
        return {"status": "SUCCESSS!!!!!"}
    except Exception as e:
        return {"error": e}


if __name__ == "__main__":
    extract_data()
    transform()
    loading_main()
