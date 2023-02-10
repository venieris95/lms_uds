from stop_words import stopwords
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import plotly.express as px
import variables as v
import seaborn as sns
import numpy as np

st.set_page_config("LMS Dashboard", page_icon=":bar_chart:", layout="wide")

def main():
    if v.check_credentials():
        st.sidebar.title("Select Mode")
        mode = st.sidebar.radio("", ("Student Data 🗃️", "Reviews 🗂️", "Analytics 🤖", "Visuals 📈", "Report 🖋️"))
        # STUDENT DATA
        if mode == 'Student Data 🗃️':
            tab1, tab2 = st.tabs(["First Semester", "Second Semester"])
            with tab1:
                st.dataframe(v.first_semester.style)
            with tab2:
                df2 = v.second_semester.drop(columns=['cs reviews', 'psy reviews', 'sociology reviews'])
                st.dataframe(df2)
            # REVIEWS
        if mode == "Reviews 🗂️":
            reviews = st.sidebar.selectbox("", ('Sociology Reviews', 'Psychology Reviews', 'Computer Science Reviews'))
            if reviews == 'Sociology Reviews':
                v.print_statement(v.soc_reviews, v.sorted_review_soc)
            if reviews == 'Psychology Reviews':
                v.print_statement(v.psy_reviews, v.sorted_review_psy)
            if reviews == 'Computer Science Reviews':
                v.print_statement(v.cs_reviews, v.sorted_review_cs)                
                
            # ANALYSIS
        if mode == 'Analytics 🤖':
            tab1, tab2, tab3, tab4 = st.tabs(["First Semester", "Second Semester", "Courses Mean",
                                             "Courses Standard Deviation"])
            with tab1:
                st.subheader('First Semester Student Grades By Course Category')
                st.download_button('Download First Semester Student Grades (.txt)', v.fsg)
                st.dataframe(v.first_semester_grades)
            with tab2:
                st.subheader('Second Semester Student Grades By Course Category')
                st.download_button('Download Second Semester Student Grades (.txt)', v.ssg)
                st.dataframe(v.second_semester_grades)
            with tab3:
                st.subheader('Courses Mean Grades')
                st.download_button('Download Mean Grades (.txt)', v.mg)
                st.dataframe(v.courses_mean_df)
            with tab4:
                st.subheader('Course Grades Standard Deviation')
                st.download_button('Download Grades Standard Deviation(.txt)', v.stg)
                st.dataframe(v.courses_std_df)
            # VISUALS
        if mode == 'Visuals 📈':
            graphs = st.sidebar.selectbox("", ('Bar Graph', 'Correlation Heatmap', 'Scatter Plot', 'Scatter Matrix'))
            if graphs == 'Bar Graph':
                tab1, tab2 = st.tabs(['First Semester', 'Second Semester'])
                with tab1:
                    st.subheader("Bar graph: comparison of means for first semester courses")
                    x = ["Psychology", "Computer Science", "Sociology"]  # x axis, y axis
                    y = [v.mean(v.psy_grades_1), v.mean(v.cs_grades_1), v.mean(v.soc_grades_1)]
                    fig, ax = plt.subplots()
                    ax.bar(x, y)
                    ax.set_ylim([0, 100])
                    ax.set_title("First Semester")
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
                    st.subheader("Correlation Heatmap: comparison of correlations between first semester courses")
                    df1 = v.first_semester
                    df1.drop(df1.columns[[0]], axis=1, inplace=True)
                    fig, ax = plt.subplots()
                    sns.heatmap(df1.corr(), ax=ax)
                    st.write(fig)
                with tab2:
                    st.subheader("Correlation Heatmap: comparison of correlations between second semester courses")
                    df2 = v.second_semester
                    df2.drop(df2.columns[[0]], axis=1, inplace=True)
                    fig, ax = plt.subplots()
                    sns.heatmap(df2.corr(), ax=ax)
                    st.write(fig)
            if graphs == 'Scatter Plot':
                fig1, ax1 = plt.subplots()
                y1 = v.absence_1
                x1 = v.overall_1
                y2 = v.absence_2
                x2 = v.overall_2
                ax1.scatter(x1, y1, c='b', label='first semester')
                ax1.scatter(x2, y2, c='r', label='second semester')
                plt.legend(loc=1)
                plt.title("Scatter plot of absences and Overall grade")
                plt.ylabel('Absences')
                plt.xlabel('Overall Grade')
                ax1.plot([60, 85], [0,10])
                st.write(fig1)
            if graphs == 'Scatter Matrix':
                df1 = v.first_semester
                df2 = v.second_semester
                fig1 = px.scatter_matrix(df1,
                                 dimensions=["intro to cs I", "machine learning I", "web design I", "absence"],
                                 # select comparing items/variables
                                 title="absence and cs classes (1 semester)",  # title
                                 labels={col: col.replace('_', ' ') for col in df1.columns})  # remove underscore step1
                fig1.update_traces(diagonal_visible=False)  # remove underscore step2

                fig2 = px.scatter_matrix(df2,
                                 dimensions=["intro to computer science", "machine learning", "web design", "absence"],
                                 # select comparing items/variables
                                 title="absence and cs classes (2 semester)",  # title
                                 labels={col: col.replace('_', ' ') for col in df1.columns})  # remove underscore step1
                fig2.update_traces(diagonal_visible=False)  # remove underscore step2
                st.write(fig1)
                st.write(fig2)
            # REPORT
        if mode == 'Report 🖋️':
            text = open("Report.txt", "r")
            if st.download_button('Press the button to download overall report (.txt file)', text):
                st.write('Thanks for downloading!')

if __name__ == "__main__":
    main()
