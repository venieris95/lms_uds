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
            graphs = st.sidebar.selectbox("", ('Bar Graph', 'Correlation Heatmap', 'Slopechart'))
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
            if graphs == 'Slopechart':
                df1 = v.first_semester                    
                df2 = v.second_semester
                left_label = [str(c) + ', '+ str(round(y)) for c, y in zip(df1['name'], v.overall_1)]
                right_label = [str(c) + ', '+ str(round(y)) for c, y in zip(df2['name'], v.overall_2)]
                #klass = ['red' if (v.overall_1-v.overall_2) < 0 else 'green']
                                                                            
                def newline(p1, p2, color='black'):
                    ax = plt.gca()
                    l = mlines.Line2D([p1[0],p2[0]], [p1[1],p2[1]], color='red' if p1[1]-p2[1] > 0 else 'green', marker='o', markersize=6)
                    ax.add_line(l)
                    return l

                fig, ax = plt.subplots()
                ax.vlines(x=1, ymin=60, ymax=85, alpha=0.7)
                ax.vlines(x=2, ymin=60, ymax=85, color='black', alpha=0.7)
                ax.scatter(y=v.overall_1, x=np.repeat(1, s=10, color='black', alpha=0.7)
                ax.scatter(y=v.overall_2, x=np.repeat(2, s=10, color='black', alpha=0.7)                                                            
                for p1, p2, c in zip(v.overall_1, v.overall_2, df1['name']):
                    newline([1,p1], [2,p2])
                    ax.text(1-0.05, p1, c + ', ' + str(round(p1)), horizontalalignment='right', verticalalignment='center')
                    ax.text(3+0.05, p2, c + ', ' + str(round(p2)), horizontalalignment='left', verticalalignment='center')
                                                                            
                ax.set_title("Slopechart: Comparing student grades between first and second semester", fontdict={'size':22})
                ax.set(xlim=(0,4), ylim=(60,85), ylabel='Mean Grade')
                ax.set_xticks([1,3])
                ax.set_xticklabels(["First Semester", "Second Semester"])
                plt.yticks(np.arange(60, 85, 3), fontsize=12)
                st.write(fig)
                                                                            
            # REPORT
        if mode == 'Report 🖋️':
            st.sidebar.title("Mode 5: Report")
            text_contents = 'Students are struggling with CS. Btw, We can report here !!! I like Sushi since it has a lot ' \
                            'of nutrition... '
            st.write(text_contents)

            if st.download_button('Download overall report (.txt file)', text_contents):
                st.write('Thanks for downloading!')

if __name__ == "__main__":
    main()
