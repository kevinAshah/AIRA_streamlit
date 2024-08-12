import streamlit as st
from bots.content_generation import content_generation_bot
from bots.rule_writing import rule_writing_bot

st.set_page_config(layout="wide")

def main():
    
    st.title("AIRA AI Dashboard")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        cookie = st.text_input("Enter your Password", type="password")
        if st.button("Authenticate"):
            if cookie:
                st.session_state.authenticated = True
            else:
                st.error("Cookie cannot be empty!")
    else:
        st.sidebar.title("Navigation")
        selection = st.sidebar.radio("Select a Bot: ", ["Content Generation Bot", "Rule Writing Bot"])

        if selection == "Content Generation Bot":
            content_generation_bot()
        elif selection == "Rule Writing Bot":
            rule_writing_bot()

if __name__ == "__main__":
    main()
