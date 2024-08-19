import streamlit as st
import pandas as pd
from utils import fetch_data, format_suggestions

def content_generation_bot(headers, payload):
    st.subheader("Content Generation Bot")

    # Cookie input specific to this bot
    # cookie = st.text_input("Enter Cookie Header for Content Generation Bot", type="password")
    # payload = {}
    url = "https://eucrm.cc.capillarytech.com/arya/api/v1/ask-aira-service/content_gen/log?page=1&limit=30"

    if st.button("Fetch Data"):
        data = fetch_data(url, headers, payload)
        if data and data['success']:
            logs = data.get('logs', [])

            if logs:
                    df = pd.DataFrame(logs)
                    df['suggestions'] = df['suggestions'].apply(format_suggestions)
                    df = df[['query', 'suggestions', 'userRefId', 'orgId', 'updated_at']]
                    df.columns = ['Query', 'Suggestions', 'User_ID', 'Org_ID', 'Last_Updated']

                    df['Last_Updated'] = pd.to_datetime(df['Last_Updated']).dt.strftime('%Y-%m-%d %H:%M:%S')
                    
                    formatted_data = {
                        'Query': df['Query'],
                        'Suggestions': df['Suggestions'].apply(lambda x: "\n\n".join(x)),
                        'User_ID': df['User_ID'],
                        'Org_ID': df['Org_ID'],
                        'Last_Updated': df['Last_Updated'],
                    }
                    formatted_df = pd.DataFrame(formatted_data)

                    st.dataframe(formatted_df, use_container_width=True)

            else:
                    st.warning("No logs found in the API response.")
