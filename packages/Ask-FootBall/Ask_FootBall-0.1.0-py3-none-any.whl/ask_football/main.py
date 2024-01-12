import re


def extract_information(table_headers, question):
    column_name = []
    filters = {}

    year_pattern = r"\b(19|20)\d{2}\b"
    country_city_pattern = r"in\s([A-Za-z\s]+)"

    year_match = re.search(year_pattern, question)
    if year_match:
        filters['Year'] = year_match.group()

    country_city_match = re.search(country_city_pattern, question)
    if country_city_match:
        filters['Host'] = country_city_match.group(1).strip()

    if ('venue' in question.lower() or 'location' in question.lower()) and 'Venues_Cities' in table_headers:
        column_name.append('Venues_Cities')
    elif 'host' in question.lower():
        column_name.append('Host')
    elif 'attendance' in question.lower() and ('Total_Attendance' or 'Average_Attendance' or 'Highest_Attendance') in table_headers:
        if 'average' in question.lower() and 'Average_Attendance' in table_headers:
            column_name.append('Average Attendance')
        elif 'total' in question.lower() and 'Total_Attendance' in table_headers:
            column_name.append('Total Attendance')
        elif ('highest' in question.lower() or 'most' in question.lower()) and 'Highest_Attendace':
            column_name.append('Highest_Attendance')
        else:
            column_name.append('Total Attendance')
    elif 'matches' in question.lower() and 'Matches' in table_headers:
        column_name.append('Matches')
    elif ('finalists' in question.lower() or 'winning scores' in question.lower()) and ('Highest_Attendance_Games' or 'Highest_Attendance_Venue' in table_headers):
        column_name.append('Highest Attendance Games')

    return column_name, filters
