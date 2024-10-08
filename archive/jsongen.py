import json
import schedule
import time
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Constants
SPREADSHEET_ID = "your_spreadsheet_id_here"  # Replace with your actual spreadsheet ID
START_ROW_INDEX = 0
END_ROW_INDEX = 1000
START_COLUMN_INDEX = 0
END_COLUMN_INDEX = 1

def generate_json(names: list[str]) -> str:
    """Generate JSON data based on the list of names"""
    requests = []
    values = load_values_from_file("nametemp.txt")  # Load values from file
    sheet_ids = get_sheet_ids(SPREADSHEET_ID)  # Get sheet IDs from Google Sheets API
    for sheet_id in sheet_ids:
        for name in names:
            request = {
                "updateCells": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": START_ROW_INDEX,
                        "endRowIndex": END_ROW_INDEX,
                        "startColumnIndex": START_COLUMN_INDEX,
                        "endColumnIndex": END_COLUMN_INDEX
                    },
                    "rows": [
                        {
                            "values": [
                                {
                                    "dataValidation": {
                                        "condition": {
                                            "type": "ONE_OF_LIST",
                                            "values": [
                                                {"userEnteredValue": value} for value in values
                                            ]
                                        },
                                        "showCustomUi": True
                                    }
                                }
                            ]
                        }
                    ],
                    "fields": "dataValidation"
                },
                "rangeMatcher": {
                    "rangeMatchCriteria": "VALUE_IN_RANGE",
                    "valueRange": {
                        "values": [
                            [
                                name
                            ]
                        ]
                    }
                }
            }
            requests.append(request)
    data = {"requests": requests}
    return json.dumps(data, indent=4)

def get_sheet_ids(spreadsheet_id: str) -> list[str]:
    """Get sheet IDs from Google Sheets API"""
    service = build('sheets', 'v4')
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheet_ids = [sheet['id'] for sheet in spreadsheet['sheets']]
    return sheet_ids

def load_names_from_file(file_path: str) -> list[str]:
    """Load names from a text file"""
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        print("File not found!")
        return []

def load_values_from_file(file_path: str) -> list[str]:
    """Load values from a text file"""
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        print("File not found!")
        return []

def write_json_to_file(json_data: str, file_path: str) -> None:
    """Write JSON data to a file"""
    try:
        with open(file_path, "w") as f:
            f.write(json_data)
    except Exception as e:
        print(f"Error writing to file: {e}")

def delete_file(file_path: str) -> None:
    """Delete a file"""
    try:
        os.remove(file_path)
        print("File deleted successfully!")
    except FileNotFoundError:
        print("File not found!")

def main() -> None:
    names = load_names_from_file("nametemp.txt")
    json_data = generate_json(names)
    write_json_to_file(json_data, "output.json")

    schedule.every().day.at("06:00").do(delete_file, "nametemp.txt")  # UTC+7

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()