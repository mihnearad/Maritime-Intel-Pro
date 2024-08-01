import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fetch_fleet_info(imo_number):
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
    response = s.post(login_url, headers=headers, data=login_data)
    print("Login Response Status:", response.status_code)

    # Fetch fleet info
    search_url = 'https://www.equasis.org/EquasisWeb/restricted/FleetInfo?fs=CompanyInfo'
    headers['Referer'] = search_url
    payload = {
        'P_COMP': imo_number,  # This should be adjusted to the actual parameter expected
        'P_PAGE': '1',
        'ongletActifSC': 'comp',
    }
    response = s.post(search_url, headers=headers, data=payload)
    print("Fleet Info Response Status:", response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Debugging output
    print("Response snippet:", response.text[:1000])  # Print a snippet of the response

    # Fetch fleet
    fleet_table = soup.find('table', class_='tableLS table table-striped table-responsive')
    if fleet_table:
        print("Fleet:")
        for row in fleet_table.find_all('tr')[1:]:  # Exclude header row if needed
            for cell in row.find_all('td'):
                print(cell.text.strip(), end=' | ')
            print()  # Newline for each row end
    else:
        print("Fleet table not found")

# Example usage
imo_input = input("Enter IMO number or company identifier: ")
fetch_fleet_info(imo_input)
