import os
import pickle
import streamlit as st
import numpy as np
import pandas as pd

# Load data
courses_list = pickle.load(open(r'C:\Users\sowmi\OneDrive\Documents\MINI PROJECT\Collabrtive filtering\courses (1).pkl', 'rb'))
similarity = pickle.load(open(r'C:\Users\sowmi\OneDrive\Documents\MINI PROJECT\Collabrtive filtering\similarity (1).pkl', 'rb'))

# Define recommendation function
def recommend(course):
    index = courses_list[courses_list['course_name'] == course].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_courses = []
    for i in distances[1:7]:
        course_name = courses_list.iloc[i[0]].course_name
        similarity_score = i[1]
        recommended_courses.append((course_name, similarity_score))  # Return name and similarity score as a tuple

    return recommended_courses

# Set up Streamlit page
st.set_page_config(page_title="Coursera Course Recommendation System", layout="centered")

# Add custom CSS to style the page
st.markdown(
    """
    <style>
    .main { background-color: #f5f5f5; }
    .title { font-size: 48px; color: blue; text-align: center; font-weight: bold; }
    .subtitle { font-size: 24px; color: black; text-align: center; margin-bottom: 20px; }
    .tagline { font-size: 20px; color: black; text-align: center; margin-top: 0; }
    .container { padding: 20px; background-color: white; border-radius: 10px; 
                 box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1); margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True
)

# Content in a centered container
st.markdown("<div class='container'>", unsafe_allow_html=True)
st.markdown("<h2 class='title'>Coursera Course Recommendation System</h2>", unsafe_allow_html=True)
st.markdown("<h4 class='subtitle'>Find similar courses from a dataset of over 3,000 courses from Coursera!</h4>", unsafe_allow_html=True)
st.markdown("<h4 class='tagline'>Explore Your Interest</h4>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Personal Information Form
st.write("### Personal Information")
name = st.text_input("Enter your Name")
phone = st.text_input("Enter your Phone Number")
email = st.text_input("Enter your Email Address")

# Dropdown for Current Education Level
education_levels = ["8-10 Grade", "11-12 Grade", "Bachelor's Degree", "Master's Degree", "Doctorate", "Others"]
current_education = st.selectbox("Select your Current Education Level:", education_levels)

# If user selects "Others", show a text input to enter their education
if current_education == "Others":
    other_education = st.text_input("Please specify your current education:")
else:
    other_education = None

# Combined course search based on domain and recommendation button
with st.container():
    # Add a text input for domain search
    search_query = st.text_input("Type a domain you are interested in (e.g., 'Data Science', 'Business', etc.):")
    
    # Recommendation button and functionality
    if st.button('Show Recommended Courses'):
        filtered_courses = courses_list[courses_list['course_name'].str.contains(search_query, case=False)]['course_name'].values
        
        if filtered_courses.size > 0:
            st.write("Recommended Courses based on your interests are:")
            # Show the first matched course recommendations based on search_query
            recommended_courses = recommend(filtered_courses[0])  # Recommend based on the first matched course
            for i, (course, similarity_score) in enumerate(recommended_courses):
                st.write(f"{i + 1}. {course} (Similarity: {similarity_score:.2%})")  # Display similarity as a percentage
        else:
            st.write("No courses match your search. Please try a different keyword.")

# Footer note
st.markdown("<h6 style='text-align: center; color: red;'>Copyright reserved by Coursera and Respective Course Owners</h6>", unsafe_allow_html=True)
