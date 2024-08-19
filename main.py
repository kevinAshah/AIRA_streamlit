import streamlit as st
from bots.content_generation import content_generation_bot
from bots.rule_writing import rule_writing_bot

st.set_page_config(layout="wide")

def main():
    
    st.title("AIRA AI Dashboard")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
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
        elif selection == "Rule Writing Bot":
            rule_writing_bot(st.session_state.headers, st.session_state.payload)


if __name__ == "__main__":
    main()
