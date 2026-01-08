# input course code -> home.uprm -> return list of professors
# format for input to notaso
# input professor to notaso -> return ranking
# sort all professors that appear for inputted course code 

import requests
from bs4 import BeautifulSoup

uprm_base_url = "https://www.uprm.edu/registrar/sections/index.php"
notaso_base_url = "https://notaso.com/api/v2/professors/"

def get_professors():

    course_code = input("Enter course code e.g (MATE3031): ")

    print(f"Fetching sections for ({course_code})...")

    payload = {
        'v1' : course_code,
        'term' : '3-2025',
        'a' : 's',
        'cmd1' : 'Search'
    }

    response = requests.get(uprm_base_url, params=payload)
    raw_html = response.text

    soup = BeautifulSoup(raw_html, 'html.parser')

    rows = soup.find_all('tr')

    profs = []

    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 5:
            profs.append(cols[5].text)

    return ['N/A' if len(prof)==0 else prof for prof in profs]

def get_professor_grade(professor : str):
    formatted_prof = professor.split()

    if len(formatted_prof) > 2:
        if len(formatted_prof[1]) == 2: # Handle initial (Victor A. Ocasio Gonzalez -> Victor Ocasio)
            formatted_prof = formatted_prof[0] + ' ' + formatted_prof[2]
        else:                           # Handle multiple last names (Jhoana Romero Leiton -> Jhoana Romero)
            formatted_prof = formatted_prof[0] + ' ' + formatted_prof[1]
    else:
        formatted_prof = formatted_prof[0] + ' ' + formatted_prof[1]

    payload = { 'search' : formatted_prof}

    response = requests.get(notaso_base_url, params=payload)
    info = response.json()

    if info['results']:
        if "Mayagüez" in info['results'][0]['university']:
            return round(info['results'][0]['score'], 2)
    return -1

if __name__ == '__main__':
    professors = get_professors()
    grades = {}
    empty_sections = 0
    print("Getting grades for professors...")
    for prof in professors:
        if prof == 'N/A':
            empty_sections += 1
            grades['N/A Sections'] = empty_sections
        else:
            grades[prof] = get_professor_grade(prof)
    sorted_grades = dict(sorted(grades.items(), key=lambda x: x[1], reverse=True))
    print(sorted_grades)
