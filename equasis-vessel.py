import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def fetch_vessel_details(imo_number):
    s = requests.Session()

    # Fetch credentials from environment variables
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')

    # Login
    login_url = 'https://www.equasis.org/EquasisWeb/authen/HomePage?fs=HomePage'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    login_data = {
        'j_email': email,
        'j_password': password,
        'submit': 'Login'
    }
    s.post(login_url, headers=headers, data=login_data)

    # Fetch basic vessel info
    search_url = 'https://www.equasis.org/EquasisWeb/restricted/Search?fs=Search'
    headers['Referer'] = search_url
    payload = {
        'P_PAGE': '1',
        'P_PAGE_COMP': '1',
        'P_PAGE_SHIP': '1',
        'ongletActifSC': 'ship',
        'P_ENTREE_HOME_HIDDEN': imo_number,
        'P_ENTREE': imo_number,
        'Submit': 'Search',
        'checkbox-shipSearch': 'Ship'
    }
    response = s.post(search_url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Fetch vessel name and year built
    vessel_name = year_built = "Not Found"
    table = soup.find('table')
    if table:
        rows = table.find_all('tr')
        if len(rows) > 1:
            cells = rows[1].find_all('td')
            if cells:
                vessel_name = cells[0].text.strip()  # Check if index is correctly pointing to vessel name
                year_built = cells[3].text.strip()  # Check if index is correctly pointing to year built

    print(f"Vessel Name: {vessel_name}")
    print(f"Year Built: {year_built}")

    # Fetch management details
    details_url = 'https://www.equasis.org/EquasisWeb/restricted/ShipInfo?fs=Search'
    details_payload = {
        'P_IMO': imo_number
    }
    details_response = s.post(details_url, headers=headers, data=details_payload)
    details_soup = BeautifulSoup(details_response.text, 'html.parser')

    # Check if this selector needs adjustment to target the correct table
    management_table = details_soup.find('table', class_='tableLS table table-striped table-responsive')
    if management_table:
        print("Management Details:")
        for row in management_table.find_all('tr')[1:]:  # Exclude header row if needed
            for cell in row.find_all('td'):
                print(cell.text.strip(), end=' | ')
            print()  # Newline for each row end

# Example usage
imo_input = input("Enter IMO number: ")
fetch_vessel_details(imo_input)
