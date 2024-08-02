import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from io import StringIO

def fetch_fleet_info(company_identifier):
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    s = requests.Session()

    login_url = "https://www.equasis.org/EquasisWeb/authen/HomePage?fs=HomePage"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    login_data = {"j_email": email, "j_password": password, "submit": "Login"}
    s.post(login_url, headers=headers, data=login_data)

    all_fleet_data = pd.DataFrame()
    page_number = 1
    while True:  # Loop until break
        search_url = "https://www.equasis.org/EquasisWeb/restricted/FleetInfo?fs=CompanyInfo"
        headers["Referer"] = search_url
        payload = {"P_COMP": company_identifier, "P_PAGE": page_number, "ongletActifSC": "comp"}
        response = s.post(search_url, headers=headers, data=payload)
        soup = BeautifulSoup(response.text, "html.parser")

        fleet_table = soup.find("table", class_="tableLS table table-striped table-responsive")
        if fleet_table:
            fleet_html = str(fleet_table)
            fleet_df = pd.read_html(StringIO(fleet_html))[0]

            # Split '(IMO) Ship's name' into 'IMO' and 'Ship's name'
            if '(IMO) Ship\'s name' in fleet_df.columns:
                fleet_df['IMO'] = fleet_df['(IMO) Ship\'s name'].str.extract(r'\(\s*(\d+)\s*\)')[0]
                fleet_df['Ship\'s name'] = fleet_df['(IMO) Ship\'s name'].str.extract(r'\)\s*(.+)')[0]
                fleet_df.drop('(IMO) Ship\'s name', axis=1, inplace=True)
                
                # Reorder columns
                new_order = ['IMO', 'Ship\'s name'] + [col for col in fleet_df.columns if col not in ['IMO', 'Ship\'s name']]
                fleet_df = fleet_df[new_order]

            all_fleet_data = pd.concat([all_fleet_data, fleet_df], ignore_index=True)
        else:
            break  # Exit loop if no table is found on the new page

        page_number += 1  # Increment to request next page

    return all_fleet_data

# Example usage
company_identifier = "5808451"
fleet_info = fetch_fleet_info(company_identifier)
print(fleet_info)
