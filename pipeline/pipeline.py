"""ETL Pipeline script"""
from extract import extract_data
from transform import transform
from load import loading_main


def lambda_handler(event=None, context=None) -> dict:
    """ LAMBDA HANDLER!!! """
    try:
        data = extract_data()
        print("extract done.")
        trans_data = transform(data)
        print("transform done.")
        loading_main(trans_data)
        return {"status": "SUCCESSS!!!!!"}
    except Exception as e:
        return {"error": e}


if __name__ == "__main__":
    data = extract_data()
    print("extract done.")
    trans_data = transform(data)
    print("transform done.")
    loading_main(trans_data)
