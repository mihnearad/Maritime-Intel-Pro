import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

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

    search_url = "https://www.equasis.org/EquasisWeb/restricted/FleetInfo?fs=CompanyInfo"
    headers["Referer"] = search_url
    payload = {"P_COMP": company_identifier, "P_PAGE": "1", "ongletActifSC": "comp"}
    response = s.post(search_url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, "html.parser")

    fleet_table = soup.find("table", class_="tableLS table table-striped table-responsive")
    if fleet_table:
        # Create DataFrame from HTML table directly if possible
        fleet_df = pd.read_html(str(fleet_table))[0]  # This uses pandas to parse the HTML table directly

        # Post-processing to separate IMO and ship name
        if "(IMO) Ship's name" in fleet_df.columns:
            fleet_df['IMO'] = fleet_df["(IMO) Ship's name"].str.extract(r'\(\s*(\d+)\s*\)')[0]
            fleet_df["Ship's name"] = fleet_df["(IMO) Ship's name"].str.extract(r'\)\s*(.+)')[0]
            fleet_df.drop("(IMO) Ship's name", axis=1, inplace=True)

            # Reorder columns to move 'IMO' and 'Ship's name' to the front
            columns = ['IMO', "Ship's name"] + [col for col in fleet_df.columns if col not in ['IMO', "Ship's name"]]
            fleet_df = fleet_df[columns]



        return fleet_df
    else:
        print("No fleet table found")
        return pd.DataFrame()

# Example usage
company_identifier = "your_company_id"
fleet_info = fetch_fleet_info(company_identifier)
print(fleet_info)
