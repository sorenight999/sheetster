"""
Look up the value of a single cell in the Google Sheet.

Two ways to use this file:

1. From the command line, for a quick manual check:
       python lookup_cell.py H6
   prints:
       The value of H6 is 17!

2. Imported from another script, to grab a value for use in code:
       from lookup_cell import get_cell_value
       score = get_cell_value("H6")
"""

import os
import sys

from dotenv import load_dotenv
import google.auth
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_sheets_client():
    """Authenticate using the service account and return a Sheets API client."""
    creds, _ = google.auth.default(scopes=SCOPES)
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


def get_first_sheet_name(sheets_client, sheet_id):
    """Look up the name of the first tab, used when SHEET_NAME isn't set in .env."""
    metadata = sheets_client.spreadsheets().get(spreadsheetId=sheet_id).execute()
    return metadata["sheets"][0]["properties"]["title"]


def get_cell_value(cell_ref, sheet_id=None, sheet_name=None):
    """
    Fetch and return the value of a single cell, e.g. get_cell_value("H6").

    sheet_id and sheet_name are optional -- if not given, they're pulled
    from .env the same way the other scripts do. This lets another script
    just call get_cell_value("H6") without repeating setup code.

    Returns None if the cell is empty.
    """
    load_dotenv()

    if sheet_id is None:
        sheet_id = os.environ["SHEET_ID"]

    sheets_client = get_sheets_client()

    if sheet_name is None:
        sheet_name = os.environ.get("SHEET_NAME") or get_first_sheet_name(sheets_client, sheet_id)

    full_range = f"{sheet_name}!{cell_ref}"
    result = sheets_client.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=full_range
    ).execute()

    values = result.get("values", [])
    if not values or not values[0]:
        return None

    return values[0][0]


def main():
    if len(sys.argv) != 2:
        print("Usage: python lookup_cell.py <CELL_REF>")
        print("Example: python lookup_cell.py H6")
        sys.exit(1)

    cell_ref = sys.argv[1]
    value = get_cell_value(cell_ref)

    if value is None:
        print(f"{cell_ref} is empty.")
    else:
        print(f'The value of {cell_ref} is "{value}"!')


if __name__ == "__main__":
    main()