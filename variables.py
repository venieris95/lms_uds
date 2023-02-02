import re
from stop_words import stopwords
import pandas as pd
import numpy as np
import streamlit as st

def check_credentials():
    """Returns `True` if the user had a correct password."""
    def credentials_entered():
        """Checks whether a password entered by the user is correct."""
        if (st.session_state["username"] == st.secrets["username"] and st.session_state["password"] == st.secrets["password"]):
            st.session_state["credentials_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["credentials_correct"] = False

    if "credentials_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.warning("Credentials: username: edutechatpython.com | password: WeLo3593!!")
        st.text_input("Username", on_change=credentials_entered, key="username")
        st.text_input("Password", type="password", on_change=credentials_entered, key="password")
        return False
    elif not st.session_state["credentials_correct"]:
        # Password not correct, show input + error.
        st.warning("Credentials: username: edutechatpython.com | password: WeLo3593!!")
        st.text_input("Username", on_change=credentials_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=credentials_entered, key="password")
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True
    
    
# REVIEWS
# DELETE NON-WORD VALUES
def strip_non_alpha_num(text):
    text = re.compile(r'\W+', re.UNICODE).split(text)
    return text


# REMOVE STOP WORDS
def remove_stopwords(word_list, stop_words):
    final_word_list = list()
    for word in word_list:
        if word not in stop_words:
            if not word.isdigit():
                final_word_list.append(word)
    return final_word_list


# TURN THE SEQUENCE OF WORDS INTO A DICTIONARY OF WORD-NR OR INSTANCES PAIR
def word_list_to_freq_dict(word_list):
    word_freq = [word_list.count(pair) for pair in word_list]
    return dict(list(zip(word_list, word_freq)))


# SORT THE DICTIONARY BY NR OF INSTANCES
def sort_dict(dictionary):
    sorted_dict = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    converted_sorted_dict = dict(sorted_dict)
    return converted_sorted_dict


def format_dict(dictionary):
    final_dict = '\n'.join(f'{key}: {value}' for key, value in dictionary.items())
    return final_dict


# SELECT THE TOP 3 WORDS
def top(dictionary):
    li = list(dictionary.split('\n'))
    return li[0:3]


def sort_words(txt):
    text = txt.lower()  # LOWER SO WORDS ARE CASE INSENSITIVE
    full_word_list = strip_non_alpha_num(text)
    wordlist = remove_stopwords(full_word_list, stopwords)
    dictionary = word_list_to_freq_dict(wordlist)
    sorted_dict = sort_dict(dictionary)
    final_dict = format_dict(sorted_dict)
    return top(final_dict)


def print_statement(review, top_words):
   len_words = len(top_words)
   st.subheader("Top %i Most used words in this review:" % len_words)
   top_words_lst = []
   for i in range(len_words):
       st.text(top_words[i])
       top_words_lst.append(top_words[i])
   my_str = 'Top words in Review: \n'
   for word in top_words_lst:
       my_str += word + '\n'    
   st.download_button('Download Top words(.txt file)', data = my_str)
   st.table(review)


# ANALYSIS
# CALCULATE MEAN
def mean(df):
    df_mean = df.mean()
    return df_mean


# CALCULATE STANDARD DEVIATION
def std(df):
    df_std = np.std(df, ddof=0)
    return df_std


# CLASS THAT ISOLATES THE NAME IN A LIST
class named_object:
    def __init__(self, name, obj):
        self.name = name
        self.obj = obj

    def __getattr__(self, attr):
        if attr == 'name':
            return self.name
        else:
            return getattr(self.obj, attr)


# READ FILE
first_semester = pd.read_csv("https://raw.githubusercontent.com/venieris95/lms_uds/main/data/group_4_semester_1.csv")
second_semester = pd.read_csv("https://raw.githubusercontent.com/venieris95/lms_uds/main/data/group_4_semester_2.csv")

# REVIEWS
# SELECT SPECIFIC COLUMNS
# READ FILE
# SELECT SPECIFIC COLUMNS
soc_reviews = second_semester['sociology reviews']
cs_reviews = second_semester["cs reviews"]
psy_reviews = second_semester["psy reviews"]
# TURN DATAFRAMES INTO LISTS
soc_reviews_list = soc_reviews.values.tolist()
cs_reviews_list = cs_reviews.values.tolist()
psy_reviews_list = psy_reviews.values.tolist()
# TURN LISTS INTO STRINGS
soc_reviews_str = ' '.join([str(item) for item in soc_reviews_list])
cs_reviews_str = ' '.join([str(item) for item in cs_reviews_list])
psy_reviews_str = ' '.join([str(item) for item in psy_reviews_list])
# RUN SORTING FUNCTION ON THE REVIEWS
sorted_review_soc = sort_words(soc_reviews_str)
sorted_review_psy = sort_words(psy_reviews_str)
sorted_review_cs = sort_words(cs_reviews_str)

# ANALYSIS
cog_psy_1 = first_semester['cognitive psy I']
soc_psy_1 = first_semester['social psy I']
ind_psy_1 = first_semester['industrial psy I']
intro_soc_1 = first_semester['intro to sociology I']
crim_1 = first_semester['criminology I']
urb_soc_1 = first_semester['urban sociology I']
intro_cs_1 = first_semester['intro to cs I']
ml_1 = first_semester['machine learning I']
webd_1 = first_semester['web design I']
cog_psy_2 = second_semester['cognitive psy']
soc_psy_2 = second_semester['social psy']
ind_psy_2 = second_semester['industrial psy']
intro_soc_2 = second_semester['intro to sociology']
crim_2 = second_semester['criminology']
urb_soc_2 = second_semester['urban sociology']
intro_cs_2 = second_semester['intro to computer science']
ml_2 = second_semester['machine learning']
webd_2 = second_semester['web design']
absence_1 = first_semester['absence']
absence_2 = second_semester['absence']
absences = (absence_1, absence_2)
# ALL COURSES TOGETHER
courses = (cog_psy_1, soc_psy_1, ind_psy_1, intro_soc_1, crim_1, urb_soc_1, intro_cs_1, ml_1, webd_1,
           cog_psy_2, soc_psy_2, ind_psy_2, intro_soc_2, crim_2, urb_soc_2, intro_cs_2, ml_2, webd_2)
# LIST OF COURSE CATEGORIES
psy_grades_1 = (cog_psy_1 + soc_psy_1 + ind_psy_1) / 3
soc_grades_1 = (intro_soc_1 + crim_1 + urb_soc_1) / 3
cs_grades_1 = (intro_cs_1 + ml_1 + webd_1) / 3
psy_grades_2 = (cog_psy_2 + soc_psy_2 + ind_psy_2) / 3
soc_grades_2 = (intro_soc_2 + crim_2 + urb_soc_2) / 3
cs_grades_2 = (intro_cs_2 + ml_2 + webd_2) / 3
# OVERALL GRADES BY SEMESTER
overall_1 = (psy_grades_1 + soc_grades_1 + cs_grades_1) / 3
overall_2 = (psy_grades_2 + soc_grades_2 + cs_grades_2) / 3
# SELECT STUDENT NAMES
name_1 = first_semester["name"]
name_2 = second_semester["name"]
first_semester_grades = {'Name': name_1, 'Overall Grade': overall_1,
                         'Psychology Grade': psy_grades_1,
                         'Computer Science Grade': cs_grades_1, 'Sociology Grade': soc_grades_1}
second_semester_grades = {'Name': name_2, 'Overall Grade': overall_2,
                          'Psychology Grade': psy_grades_2,
                          'Computer Science Grade': cs_grades_2, 'Sociology Grade': soc_grades_2}

# LIST OF COURSES, MEAN GRADES AND STANDARD DEVIATIONS
courses_name_list = list()
courses_mean_list = list()
courses_std_list = list()
for i in range(len(courses)):
    courses_name_list.append(courses[i].name)
    courses_mean_list.append(mean(courses[i]))
    courses_std_list.append(std(courses[i]))
courses_name_list.extend(['Psychology S1', 'Computer Science S1', 'Sociology S1',
                          'Psychology S2', 'Computer Science S2', 'Sociology S2'])
courses_mean_list.extend([mean(psy_grades_1), mean(cs_grades_1), mean(soc_grades_1),
                          mean(psy_grades_2), mean(cs_grades_2), mean(soc_grades_2)])
courses_std_list.extend([std(psy_grades_1), std(cs_grades_1), std(soc_grades_1),
                         std(psy_grades_2), std(cs_grades_2), std(soc_grades_2)])
# DATA FRAME OF LISTS
courses_mean_df = {'Course Name': courses_name_list, 'Mean Grade': courses_mean_list}
courses_std_df = {'Course Name': courses_name_list, 'Grade Standard Deviation': courses_std_list}

# CONVERT TO TEXT
first_semester_txt = []
for i in range(len(first_semester)):
    first_semester_txt.append("Student Name: " + name_1[i])
    first_semester_txt.append("Overall grade: " + str(overall_1[i]))
    first_semester_txt.append("Psychology grade: " + str(psy_grades_1[i]))
    first_semester_txt.append("CS grade: " + str(cs_grades_1[i]))
    first_semester_txt.append("Sociology grade: " + str(soc_grades_1[i]))
fsg  = "\n".join(str(item) for item in first_semester_txt)

second_semester_txt = []
for i in range(len(second_semester)):
    second_semester_txt.append("Student Name: " + name_2[i])
    second_semester_txt.append("Overall grade: " + str(overall_2[i]))
    second_semester_txt.append("Psychology grade: " + str(psy_grades_2[i]))
    second_semester_txt.append("CS grade: " + str(cs_grades_2[i]))
    second_semester_txt.append("Sociology grade: " + str(soc_grades_2[i]))
ssg = "\n".join(str(item) for item in second_semester_txt)

courses_mean_txt = []
for i in range(len(courses_name_list)):
    courses_mean_txt.append("Course Name: " + courses_name_list[i])
    courses_mean_txt.append("Mean Grade: " + str(courses_mean_list[i]))
mg = "\n".join(str(item) for item in courses_mean_txt)

courses_std_txt = []
for i in range(len(courses_name_list)):
    courses_std_txt.append("Course Name: " + courses_name_list[i])
    courses_std_txt.append("Course Standard Deviation: " + str(courses_std_list[i]))
stg = "\n".join(str(item) for item in courses_std_txt)
