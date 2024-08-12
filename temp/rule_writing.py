import streamlit as st
import requests
import pandas as pd

# Function to fetch data from API with authentication
def fetch_data(api_url, headers, payload):
    try:
        response = requests.get(api_url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()  # Return JSON data
        else:
            st.error(f"Failed to fetch data from API. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Set page configuration to utilize the whole page
st.set_page_config(layout="wide")

# Streamlit app layout
def main():
    st.markdown(
        """
        <style>
        .stDataFrame { 
            margin: 0;
            padding: 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("AIRA 360: Rule Writing Bot")

    url = "https://eucrm.cc.capillarytech.com/arya/api/v1/ask-aira-service/rule_expr/log?page=1&limit=10"

    payload = {}
    headers = {
    'Cookie': 'CC=KnSx4ZZPRNDeKQ1DmCnJ8HaUgw8jQil08jcKrMNmnOmhassXAWXpk5icmelZcCSe; CT=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyI2MDU4NTI0NSJdLCJvcmdJRCI6MCwiZXhwIjoxNzIzNTI0MTUwLCJpYXQiOjE3MjM0Mzc3NTAsImlzcyI6ImNhcGlsbGFyeXRlY2guY29tIiwiYXVkIjoiY2FwaWxsYXJ5LGludG91Y2gsYXJ5YSxyZW9uLGFwcHMiLCJzb3VyY2UiOiJXRUJBUFAifQ.wRi-883c33JGJ-vTH0tE24N5xEY1kr_jZJVwFIolr0c; OID=0; CC=KnSx4ZZPRNDeKQ1DmCnJ8HaUgw8jQil08jcKrMNmnOmhassXAWXpk5icmelZcCSe; CT=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyI2MDU4NTI0NSJdLCJvcmdJRCI6MCwiZXhwIjoxNzIzNTI0MTUwLCJpYXQiOjE3MjM0Mzc3NTAsImlzcyI6ImNhcGlsbGFyeXRlY2guY29tIiwiYXVkIjoiY2FwaWxsYXJ5LGludG91Y2gsYXJ5YSxyZW9uLGFwcHMiLCJzb3VyY2UiOiJXRUJBUFAifQ.wRi-883c33JGJ-vTH0tE24N5xEY1kr_jZJVwFIolr0c; OID=0'
    }

    if st.button("Fetch Data"):
        data = fetch_data(url, headers, payload)
        if data and data['success']:
            logs = data.get('logs', [])

            if logs:
                df = pd.DataFrame(logs)
                
                df = df[['query', 'rule', 'userRefId', 'orgId', 'updated_at']]

                # Rename columns for better readability
                df.columns = ['Query', 'Rule', 'User_ID', 'Org_ID', 'Last_Updated']

                # Format the 'Updated At' column (optional)
                df['Last_Updated'] = pd.to_datetime(df['Last_Updated']).dt.strftime('%Y-%m-%d %H:%M:%S')
                
                # Display the DataFrame as an adjustable table
                st.write("Logs Data:")
                st.dataframe(df, use_container_width=True)  # Adjust to use the full container width
            else:
                st.warning("No logs found in the API response.")
    
    
if __name__ == "__main__":
    main()
