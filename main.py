import streamlit as st

def check_credentials():
    """Returns `True` if the user had a correct password."""

    def credentials_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["credentials"]
            and st.session_state["password"]
            == st.secrets["credentials"][st.session_state["username"]]
        ):
            st.session_state["credentials_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["credentials_correct"] = False

    if "credentials_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["credentials_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_credentials():
    st.write("Here goes your normal Streamlit app...")
    st.button("Click me")
