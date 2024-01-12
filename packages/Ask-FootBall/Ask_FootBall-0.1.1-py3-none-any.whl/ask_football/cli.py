from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from ask_football.main import find_columns_and_filters


def main():
    table_headers = inquirer.select(
        message="Select Table Headers: (Use space to select them): ",
        choices=[
                Choice("Year", name="Year"),
                Choice("Hosts", name="Hosts"),
                Choice("Venues and Cities", name="Venues_Cities"),
                Choice("Total Attendance", name="Total_Attendance"),
                Choice("Matches", name="Matches"),
                Choice("Average Attendence", name="Average_Attendance"),
                Choice("Highest Attendance", name="Highest_Attendance"),
                Choice("Highest Attendance Venue",
                       name="Highest_Attendance_Venue"),
                Choice("Highest Attendance Games", name="Highest_Attendance_Games"),],
        multiselect=True,
        transformer=lambda result: f"{len(result)} Table Header{'s' if len(result) > 1 else ''} selected",
    ).execute()
    if table_headers:
        question = inquirer.text(message="Enter your Question:").execute()

    print(find_columns_and_filters(table_headers, question))
