import streamlit as st
import requests
import pandas as pd

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

def format_suggestions(suggestions):
    formatted_suggestions = []
    for suggestion in suggestions:
        # Extract metadata if needed
        metadata_start = suggestion.find("## METADATA BEGIN ##")
        metadata_end = suggestion.find("## METADATA END ##")
        
        if metadata_start != -1 and metadata_end != -1:
            suggestion_text = suggestion[:metadata_start].strip()
            metadata = suggestion[metadata_start:metadata_end+len("## METADATA END ##")].strip()
        else:
            suggestion_text = suggestion
            metadata = ""

        # Combine suggestion text and metadata with formatting
        formatted_suggestions.append(f"{suggestion_text}\n\n**Metadata**:\n{metadata}")
    return formatted_suggestions

st.set_page_config(layout="wide")


def content_generation_bot(headers, payload):
    st.subheader("Content Generation Bot")

    # API URL and Headers
    url = "https://eucrm.cc.capillarytech.com/arya/api/v1/ask-aira-service/content_gen/log?page=1&limit=10"

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

def rule_writing_bot(headers, payload):
    st.subheader("Rule Writing Bot")

    url = "https://eucrm.cc.capillarytech.com/arya/api/v1/ask-aira-service/rule_expr/log?page=1&limit=10"

    if st.button("Fetch Data"):
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


def main():
    st.title("AIRA AI Dashboard")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        # Authentication process
        cookie = st.text_input("Enter Cookie Header", type="password")
        if st.button("Authenticate"):
            if cookie:
                st.session_state.authenticated = True
                st.session_state.headers = {'Cookie': cookie}
                st.session_state.payload = {}
            else:
                st.error("Cookie cannot be empty!")
    else:
        st.sidebar.title("Navigation")
        selection = st.sidebar.radio("Select: ", ["Content Generation Bot", "Rule Writing Bot"])

        if selection == "Content Generation Bot":
            content_generation_bot(st.session_state.headers, st.session_state.payload)
        if selection == "Rule Writing Bot":
            rule_writing_bot(st.session_state.headers, st.session_state.payload)

if __name__ == "__main__":
    main()
