# Equasis Data Fetcher

The Equasis Data Fetcher is a Streamlit-based web application designed to retrieve and analyze maritime vessel information from the Equasis database. It offers functionalities for fetching detailed information about vessels and entire fleets, and it provides an interface for querying this data using natural language questions powered by OpenAI.

At the moment it's only querying data from: equasis.org

## Features

- **Vessel Info**: Fetch detailed information about a specific vessel using its IMO number.
- **Fleet Info**: Retrieve and display fleet information for a specified company identifier.
- **Data Query**: Leverage OpenAI's GPT-3.5 to ask questions directly about the fetched fleet data.

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mihnearad/Vessel-Search-Tool
   cd Vessel-Search-Tool
   ```

2. **Create and Activate a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
   ```

3. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
- You need to set the `OPENAI_API_KEY` in your environment to interact with OpenAI's API (required for data querying). You can do this by setting the environment variable directly or by using a `.env` file:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```

5. **Run the Streamlit Application**
   ```bash
   streamlit run app.py
   ```

## Usage

- Navigate to the URL provided by Streamlit after running the application.
- Use the sidebar to select the type of query you wish to perform.
- For **Fleet Info** and **Vessel Info**, input the required identifiers and click the corresponding fetch button.
- For **Data Query**, after fetching the fleet info, type your query into the input field and press "Execute Query" to see the results.

## Contributing

Contributions to this project are welcome. Please ensure that you update tests as appropriate and adhere to the existing coding style.

## License

This project is licensed under the MIT License.
