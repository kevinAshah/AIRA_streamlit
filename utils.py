import requests
import streamlit as st

def fetch_data(api_url, headers, payload):
    try:
        response = requests.get(api_url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch data from API. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def format_suggestions(suggestions):
    formatted_suggestions = []
    for suggestion in suggestions:
        metadata_start = suggestion.find("## METADATA BEGIN ##")
        metadata_end = suggestion.find("## METADATA END ##")
        
        if metadata_start != -1 and metadata_end != -1:
            suggestion_text = suggestion[:metadata_start].strip()
            metadata = suggestion[metadata_start:metadata_end+len("## METADATA END ##")].strip()
        else:
            suggestion_text = suggestion
            metadata = ""

        formatted_suggestions.append(f"{suggestion_text}\n\n**Metadata**:\n{metadata}")
    return formatted_suggestions
