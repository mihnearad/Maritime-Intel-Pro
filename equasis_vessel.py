import requests
from bs4 import BeautifulSoup
import os

def fetch_vessel_details(imo_number):
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')

    s = requests.Session()
    login_url = 'https://www.equasis.org/EquasisWeb/authen/HomePage?fs=HomePage'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    login_data = {'j_email': email, 'j_password': password, 'submit': 'Login'}
    s.post(login_url, headers=headers, data=login_data)

    search_url = 'https://www.equasis.org/EquasisWeb/restricted/Search?fs=Search'
    headers['Referer'] = search_url
    payload = {'P_PAGE': '1', 'P_PAGE_COMP': '1', 'P_PAGE_SHIP': '1', 'ongletActifSC': 'ship', 'P_ENTREE_HOME_HIDDEN': imo_number, 'P_ENTREE': imo_number, 'Submit': 'Search'}
    response = s.post(search_url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')

    vessel_name = year_built = "Not Found"
    table = soup.find('table')
    if table:
        rows = table.find_all('tr')
        if len(rows) > 1:
            cells = rows[1].find_all('td')
            if cells:
                vessel_name = cells[0].text.strip()
                year_built = cells[3].text.strip()
    return vessel_name, year_built

