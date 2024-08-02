import streamlit as st
from equasis_vessel import fetch_vessel_details
from equasis_company import fetch_fleet_info
import os
import pandas as pd
from pandasai.llm import OpenAI
from pandasai import SmartDataframe

# Load environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Initialize OpenAI language model
llm = OpenAI(api_token=openai_api_key, model="gpt-3.5-turbo")
st.set_page_config(page_title='Maritime Intel Pro',layout='wide')
st.title('Maritime Intel Pro')

if 'fleet_data' not in st.session_state:
    st.session_state.fleet_data = pd.DataFrame()

st.sidebar.title("Query Options")
query_type = st.sidebar.selectbox("Choose a query type", ["Vessel Info", "Fleet Info"])

if query_type == "Fleet Info":
    company_identifier = st.sidebar.text_input("Enter Company Identifier (found on Equasis):", "")
    if st.sidebar.button("Fetch Fleet Info"):
        st.session_state.fleet_data = fetch_fleet_info(company_identifier)
    if not st.session_state.fleet_data.empty:
        st.subheader("Fleet Details")
        st.dataframe(st.session_state.fleet_data)
        user_query = st.text_input("Enter your query here:")
        if st.button("Execute Query"):
            if user_query:
                st.write("Processing your query...")
                try:
                    pandas_ai = SmartDataframe(st.session_state.fleet_data, config={"llm": llm})
                    response = pandas_ai.chat(user_query)
                    st.write("Query Result:", response)
                except Exception as e:
                    st.error(f"Error processing your query: {str(e)}")
            else:
                st.warning("Please enter a query to execute.")
elif query_type == "Vessel Info":
    imo_number = st.sidebar.text_input("Enter IMO number:", "")
    if st.sidebar.button("Fetch Vessel Info"):
        vessel_name, year_built = fetch_vessel_details(imo_number)
        st.subheader("Vessel Details")
        st.write(f"**Name:** {vessel_name}")
        st.write(f"**Year Built:** {year_built}")
