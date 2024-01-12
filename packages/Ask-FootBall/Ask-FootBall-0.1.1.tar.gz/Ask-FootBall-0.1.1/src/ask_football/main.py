import re


def find_columns_and_filters(table_headers, question):
    relevant_columns = []
    filters = {}

    column_patterns = {
        "Year": r"\byear\b|\byears\b",
        "Host": r"\bhost\b|\bhosts\b",
        "Venues_Cities": r"\bvenue\b|\bvenues\b|\bcity\b|\bcities\b",
        "Total_Attendance": r"\btotal attendance\b",
        "Matches": r"\bmatch\b|\bmatches\b",
        "Average_Attendance": r"\baverage attendance\b",
        "Highest_Attendance_Number": r"\bhighest attendance\b",
        "Highest_Attendance_Venue": r"\bvenue\b",
        "Highest_Attendance_Games": r"\bgame\b|\bgames\b",
        "Winner": r"\bwinner\b|\bwinners\b"
        # Ref: https://github.com/scrapinghub/dateparser/blob/master/dateparser/data/date_translation_data/en.py
    }

    for header in table_headers:
        pattern = column_patterns.get(header)
        if pattern and re.search(pattern, question, re.IGNORECASE):
            relevant_columns.append(header)

    year_match = re.search(r"\b\d{4}\b", question)
    if year_match:
        filters["Year"] = year_match.group()

    return relevant_columns, filters
