import re


def find_columns_and_filters(table_headers, question):
    relevant_columns = []
    filters = {}

    column_patterns = {
        "Year": r"\b(years?|date|period)\b",
        "Host": r"\b(hosts?|country|nation|where|location|held)\b",
        "Venues_Cities": r"\b(venue|venues|city|cities|location|locations|place|places|where)\b",
        "Total_Attendance": r"\b(total attendance|attendees|people)\b",
        "Matches": r"\b(match|matches|game|games|finals)\b",
        "Average_Attendance": r"\b(average attendance)\b",
        "Highest_Attendance_Number": r"\b(highest attendance)\b",
        "Highest_Attendance_Venue": r"\b(venue|stadium|stadiums)\b",
        "Highest_Attendance_Games": r"\b(most watched game|finals)\b",
        # Ref: https://github.com/scrapinghub/dateparser/blob/master/dateparser/data/date_translation_data/en.py
        # More Keywords we can add to expand the scope
        # data ref; https://en.wikipedia.org/wiki/FIFA_World_Cup#Attendance
    }

    for header in ["Host", "Venues_Cities"]:
        pattern = column_patterns.get(header)
        if pattern and re.search(pattern, question, re.IGNORECASE):
            relevant_columns.append(header)

    if not relevant_columns:
        for header, pattern in column_patterns.items():
            if re.search(pattern, question, re.IGNORECASE):
                relevant_columns.append(header)

    year_match = re.search(r"\b\d{4}\b", question)
    year_range_match = re.search(r"\b(\d{4})-(\d{4})\b", question)
    if year_range_match:
        start_year, end_year = year_range_match.groups()
        filters["Year_Range"] = (start_year, end_year)
    elif year_match:
        filters["Year"] = year_match.group()

    return relevant_columns, filters
