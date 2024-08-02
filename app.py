import streamlit as st
from equasis_vessel import fetch_vessel_details  # Ensure this module has a correct function signature
from equasis_company import fetch_fleet_info  # Ensure this is imported correctly

st.set_page_config(layout='wide')
st.title('Equasis Data Fetcher')

st.sidebar.title("Query Options")
query_type = st.sidebar.selectbox("Choose a query type", ["Vessel Info", "Fleet Info"])

if query_type == "Vessel Info":
    imo_number = st.sidebar.text_input("Enter IMO number:", "")
    if st.sidebar.button("Fetch Vessel Info"):
        vessel_name, year_built = fetch_vessel_details(imo_number)
        st.subheader("Vessel Details")
        st.write(f"**Name:** {vessel_name}")
        st.write(f"**Year Built:** {year_built}")

elif query_type == "Fleet Info":
    company_identifier = st.sidebar.text_input("Enter Company IMO number:", "")
    if st.sidebar.button("Fetch Fleet Info"):
        fleet_details = fetch_fleet_info(company_identifier)
        st.subheader("Fleet Details")
        st.dataframe(fleet_details)  # Use st.dataframe to properly display the DataFrame

