from stop_words import stopwords
import re
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import variables as v
import seaborn as sns

st.set_page_config("LSM Dashboard", page_icon=":bar_chart:", layout="wide")

def main():
    if v.check_credentials():
        st.sidebar.title("Select Mode")
        mode = st.sidebar.radio("", ("Student Data", "Reviews", "Analytics", "Visuals", "Report"))
        # STUDENT DATA
        if mode == 'Student Data':
            tab1, tab2 = st.tabs(["First Semester", "Second Semester"])
            with tab1:
                st.dataframe(v.first_semester.style)
            with tab2:
                df2 = v.second_semester
                df2.drop(df2.columns[[13, 14, 15]], axis=1, inplace=True)
                st.dataframe(df2)
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
            tab1, tab2, tab3, tab4 = st.tabs(["First Semester", "Second Semester", "Courses Mean",
                                             "Courses Standard Deviation"])
            with tab1:
                st.subheader('First Semester Student Grades By Course Category')
                st.dataframe(v.first_semester_grades)
            with tab2:
                st.subheader('Second Semester Student Grades By Course Category')
                st.dataframe(v.second_semester_grades)
            with tab3:
                st.subheader('Courses Mean Grades')
                st.dataframe(v.courses_mean_df)
            with tab4:
                st.subheader('Course Grades Standard Deviation')
                st.dataframe(v.courses_std_df)
            # VISUALS
        if mode == 'Visuals':
            graphs = st.sidebar.selectbox("", ('Bar Graph', 'Correlation Heatmap', 'Scatter Matrix'))
            if graphs == 'Bar Graph':
                tab1, tab2 = st.tabs(['First Semester', 'Second Semester'])
                with tab1:
                    st.subheader("Bar graph: comparison of means for first semester courses")
                    x = ["Psychology", "Computer Science", "Sociology"]  # x axis, y axis
                    y = [v.mean(v.psy_grades_1), v.mean(v.cs_grades_1), v.mean(v.soc_grades_1)]
                    fig, ax = plt.subplots()
                    ax.bar(x, y)
                    ax.set_ylim([0, 100])
                    ax.set_title("Second Semester")
                    ax.set_xlabel("Course category")
                    ax.set_ylabel("Mean grade")
                    st.pyplot(fig)
                with tab2:
                    st.subheader("Bar graph: comparison of means for second semester courses")
                    x = ["Psychology", "Computer Science", "Sociology"]  # x axis, y axis
                    y = [v.mean(v.psy_grades_2), v.mean(v.cs_grades_2), v.mean(v.soc_grades_2)]
                    fig, ax = plt.subplots()
                    ax.bar(x, y)
                    ax.set_ylim([0, 100])
                    ax.set_title("Second Semester")
                    ax.set_xlabel("Course category")
                    ax.set_ylabel("Mean grade")
                    st.pyplot(fig)
            if graphs == 'Correlation Heatmap':
                tab1, tab2 = st.tabs(['First Semester', 'Second Semester'])
                with tab1:
                    df1 = v.first_semester
                    df1.drop(df1.columns[[0]], axis=1, inplace=True)
                    fig, ax = plt.subplots()
                    sns.heatmap(df1.corr(), ax=ax)
                    st.write(fig)
                with tab2:
                    df2 = v.second_semester
                    df2.drop(df2.columns[[0]], axis=1, inplace=True)
                    fig, ax = plt.subplots()
                    sns.heatmap(df2.corr(), ax=ax)
                    st.write(fig)
            if graphs == 'Scatter Matrix':
                st.write("TODO")
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
