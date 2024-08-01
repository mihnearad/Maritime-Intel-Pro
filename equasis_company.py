import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

def fetch_fleet_info(company_identifier):
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    s = requests.Session()

    # Login setup
    login_url = "https://www.equasis.org/EquasisWeb/authen/HomePage?fs=HomePage"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    login_data = {"j_email": email, "j_password": password, "submit": "Login"}
    s.post(login_url, headers=headers, data=login_data)

    # Fetch fleet info
    search_url = "https://www.equasis.org/EquasisWeb/restricted/FleetInfo?fs=CompanyInfo"
    headers["Referer"] = search_url
    payload = {"P_COMP": company_identifier, "P_PAGE": "1", "ongletActifSC": "comp"}
    response = s.post(search_url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, "html.parser")

    fleet_table = soup.find("table", class_="tableLS table table-striped table-responsive")
    if fleet_table:
        headers = [th.text.strip() for th in fleet_table.find_all("th")]
        rows = []
        for row in fleet_table.find_all("tr")[1:]:
            cells = [td.get_text(" ", strip=True) for td in row.find_all("td")]
            rows.append(cells)
        fleet_df = pd.DataFrame(rows, columns=headers)

        # Add a new empty column to test DataFrame manipulation
        fleet_df['New Column'] = ''

        # Process '(IMO) Ship's name' if it exists in the DataFrame
        if "(IMO) Ship's name" in fleet_df.columns:
            # Attempt to extract IMO and ship name directly
            fleet_df['IMO'] = fleet_df["(IMO) Ship's name"].str.extract(r'\((\d+)\)')
            fleet_df["Ship's name"] = fleet_df["(IMO) Ship's name"].apply(lambda x: x.split(')')[1].strip() if ')' in x else '')
            fleet_df.drop("(IMO) Ship's name", axis=1, inplace=True)  # Remove the original combined column

        return fleet_df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if the table isn't found

# Example usage
company_identifier = "your_company_id"
print(fetch_fleet_info(company_identifier))
