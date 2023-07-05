from __future__ import annotations
import csv
from autogpt.agent.agent import Agent
from autogpt.command_decorator import command

@command(
    "read_csv_by_row",
    "Extract a row from a CSV file",
    {
        "file_path": {"type": "string", "description": "The path to csv file", "required": True},
        "row_number": {"type": "integer", "description": "The row number starting with 1, including header if present", "required": True},
    },
)
def read_csv_row_by_number(file_path, row_number):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for curr_row_number, row in enumerate(reader):
            if curr_row_number == row_number:
                return row

    # Return None if the specified row number is out of range
    return None

# Example usage
# file_path = 'autogpt/commands/data.csv'  # Replace with the path to your CSV file
# row_number = 2  # Replace with the desired row number (zero-based indexing)

# row = read_csv_row_by_number(file_path, row_number)
# if row is not None:
#     print(f"Row {row_number + 1}: {row}")
# else:
#     print("Invalid row number.")