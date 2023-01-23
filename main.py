import streamlit as st
import variables

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
        st.text_input("Username", on_change=credentials_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=credentials_entered, key="password"
        )
        return False
    elif not st.session_state["credentials_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=credentials_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=credentials_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_credentials():
    def main():
        st.sidebar.title("Select Mode")
        mode = st.sidebar.radio("", ("Student Data", "Reviews", "Analytics", "Visuals", "Report"))
        # STUDENT DATA
        if mode == 'Student Data':
            st.sidebar.title("Mode 1: View student information")
        if st.sidebar.checkbox('Semester1'):
            st.text("First Semester")
            st.dataframe(v.first_semester.style)
        if st.sidebar.checkbox('Semester2'):
            st.text("Second Semester")
            st.dataframe(v.second_semester.style)
            # REVIEWS
        if mode == "Reviews":
            st.sidebar.title("Mode 2: Reviews")
            reviews = st.sidebar.selectbox("", ('Sociology Reviews', 'Psychology Reviews', 'Computer Science Reviews'))
            if reviews == 'Sociology Reviews':
                v.print_statement(v.soc_reviews, v.sorted_review_soc)
            if reviews == 'Psychology Reviews':
                v.print_statement(v.psy_reviews, v.sorted_review_psy)
            if reviews == 'Computer Science Reviews':
                v.print_statement(v.cs_reviews, v.sorted_review_cs)
            # ANALYSIS
        if mode == 'Analytics':
            st.sidebar.title("Mode 3: Analysis")
            col1, col2 = st.columns(2)
            with col1:
                if st.sidebar.checkbox('First Semester Student Grades By Course Category'):
                    st.text("First Semester")
                    st.dataframe(v.first_semester_grades)
                if st.sidebar.checkbox('Second Semester Student Grades By Course Category'):
                    st.text("Second Semester")
                    st.dataframe(v.second_semester_grades)
            with col2:
                if st.sidebar.checkbox('Courses Mean Grades'):
                    st.text("Mean Grades")
                    st.dataframe(v.courses_mean_df)
                if st.sidebar.checkbox('Course Grades Standard Deviation'):
                    st.text("Standard Deviation")
                    st.dataframe(v.courses_std_df)
            # VISUALS
        if mode == 'Visuals':
            st.sidebar.title("Mode 4: Visuals")
            # REPORT
        if mode == 'Report':
            st.sidebar.title("Mode 5: Report")
            text_contents = 'Students are struggling with CS. Btw, We can report here !!! I like Sushi since it has a lot ' \
                            'of nutrition... '
            st.write(text_contents)

            if st.download_button('Download overall report (.txt file)', text_contents):
                st.write('Thanks for downloading!')


    if __name__ == "__main__":
        main()

