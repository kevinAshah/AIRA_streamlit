import streamlit as st
import pandas as pd
from utils import fetch_data

def rule_writing_bot():
    st.subheader("Rule Writing Bot")

    url = "https://crm-nightly-new.cc.capillarytech.com/arya/api/v1/ask-aira-service/rule_expr/log?page=1&limit=10"
    cookie = st.text_input("Enter Cookie Header for Rule Writing Bot", type="password")
    payload = {}

    if st.button("Fetch Data"):
        if cookie:
            headers = {'Cookie': cookie}    
            data = fetch_data(url, headers, payload)
            if data and data['success']:
                logs = data.get('logs', [])

                if logs:
                    df = pd.DataFrame(logs)
                    df = df[['query', 'rule', 'userRefId', 'orgId', 'updated_at']]
                    df.columns = ['Query', 'Rule', 'User_ID', 'Org_ID', 'Last_Updated']
                    df['Last_Updated'] = pd.to_datetime(df['Last_Updated']).dt.strftime('%Y-%m-%d %H:%M:%S')

                    st.write("Logs Data:")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("No logs found in the API response.")
            else:
                st.error("Failed to fetch data.")
        else:
            st.error("Cookie cannot be empty!")
