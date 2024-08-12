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

# Custom function to format suggestions
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

# Set page configuration to utilize the whole page
st.set_page_config(layout="wide")

# Streamlit app layout
def main():
    st.title("AIRA 360: Content Generation Bot")

    # API URL and Headers
    url = "https://eucrm.cc.capillarytech.com/arya/api/v1/ask-aira-service/content_gen/log?page=1&limit=10"
    payload = {}
    headers = {
        'Cookie': 'CC=KnSx4ZZPRNDeKQ1DmCnJ8HaUgw8jQil08jcKrMNmnOmhassXAWXpk5icmelZcCSe; CT=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6WyI2MDU4NTI0NSJdLCJvcmdJRCI6MCwiZXhwIjoxNzIzNTI0MTUwLCJpYXQiOjE3MjM0Mzc3NTAsImlzcyI6ImNhcGlsbGFyeXRlY2guY29tIiwiYXVkIjoiY2FwaWxsYXJ5LGludG91Y2gsYXJ5YSxyZW9uLGFwcHMiLCJzb3VyY2UiOiJXRUJBUFAifQ.wRi-883c33JGJ-vTH0tE24N5xEY1kr_jZJVwFIolr0c; OID=0'
    }

    if st.button("Fetch Data"):
        data = fetch_data(url, headers, payload)
        if data and data['success']:
            logs = data.get('logs', [])

            if logs:
                # Create a DataFrame with the specific columns
                df = pd.DataFrame(logs)
                
                # Format suggestions uniquely
                df['suggestions'] = df['suggestions'].apply(format_suggestions)
                
                # Select only the required columns
                df = df[['query', 'suggestions', 'userRefId', 'orgId', 'updated_at']]

                # Rename columns for better readability
                df.columns = ['Query', 'Suggestions', 'User Reference ID', 'Organization ID', 'Last Updated']

                # Format the 'Last Updated' column
                df['Last Updated'] = pd.to_datetime(df['Last Updated']).dt.strftime('%Y-%m-%d %H:%M:%S')
                
                # Display the DataFrame as a table with rich text in the 'Suggestions' column
                st.write("Logs Data:")

                # Creating a new DataFrame to display properly formatted suggestions
                formatted_data = {
                    'Query': df['Query'],
                    'Suggestions': df['Suggestions'].apply(lambda x: "\n\n".join(x)),
                    'User Reference ID': df['User Reference ID'],
                    'Organization ID': df['Organization ID'],
                    'Last Updated': df['Last Updated'],
                }

                formatted_df = pd.DataFrame(formatted_data)

                # Displaying the table
                st.dataframe(formatted_df)

            else:
                st.warning("No logs found in the API response.")

if __name__ == "__main__":
    main()
