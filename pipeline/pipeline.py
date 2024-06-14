"""ETL Pipeline script"""
import traceback
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
        return {'status': 'SUCCESSS!!!!!'}
    except Exception as e:
        return {"status": "Failed lambda function",
                "cause": str(e),
                "stack_trace": traceback.format_exc()
                }


if __name__ == "__main__":
    print(lambda_handler())
