import streamlit as st
import pandas as pd
import base64
import random
import time
import datetime
import io
import os
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from Courses1 import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
import pafy
import plotly.express as px
import nltk
nltk.download('stopwords')

def fetch_yt_video(link):
    video = pafy.new(link)
    return video.title

def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.subheader("**Courses & Certificates Recommendations 🎓**")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 5)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course

# Establish database connection
def create_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='rafi157287',
        db='cv'
    )

def insert_data(connection, cursor, name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses):
    DB_table_name = 'user_data'
    insert_sql = f"""
    INSERT INTO {DB_table_name}
    (Name, Email_ID, resume_score, Timestamp, Page_no, Predicted_Field, User_level, Actual_skills, Recommended_skills, Recommended_courses)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    rec_values = (name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses)
    cursor.execute(insert_sql, rec_values)
    connection.commit()

st.set_page_config(page_title="AI Resume Analyzer", page_icon='./Logo/Logo1.png')

st.title("Resume AI Generator")

def run():
    img = Image.open('./Logo/Logo2.png')
    st.image(img)
    st.title("AI Resume Analyser")
    st.sidebar.markdown("# Choose User")
    activities = ["User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    link = '[©Developed by TI Unila](https://www.linkedin.com/in/mrbriit/)'
    st.sidebar.markdown(link, unsafe_allow_html=True)

    connection = create_connection()
    cursor = connection.cursor()

    # Create the DB if not exists
    db_sql = "CREATE DATABASE IF NOT EXISTS CV;"
    cursor.execute(db_sql)

    # Create table if not exists
    DB_table_name = 'user_data'
    table_sql = f"""
    CREATE TABLE IF NOT EXISTS {DB_table_name} (
        ID INT NOT NULL AUTO_INCREMENT,
        Name VARCHAR(500) NOT NULL,
        Email_ID VARCHAR(500) NOT NULL,
        resume_score VARCHAR(8) NOT NULL,
        Timestamp VARCHAR(50) NOT NULL,
        Page_no VARCHAR(5) NOT NULL,
        Predicted_Field BLOB NOT NULL,
        User_level BLOB NOT NULL,
        Actual_skills BLOB NOT NULL,
        Recommended_skills BLOB NOT NULL,
        Recommended_courses BLOB NOT NULL,
        PRIMARY KEY (ID)
    );
    """
    cursor.execute(table_sql)

    if choice == 'User':
        st.markdown('<h5 style="text-align: left; color: #021659;"> Upload your resume, and get smart recommendations</h5>', unsafe_allow_html=True)
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            with st.spinner('Uploading your Resume...'):
                time.sleep(4)
            upload_dir = './Uploaded_Resumes/'
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            save_image_path = os.path.join(upload_dir, pdf_file.name)
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            show_pdf(save_image_path)
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            if resume_data:
                resume_text = pdf_reader(save_image_path)
                st.header("**Resume Analysis**")
                st.success("Hello " + resume_data['name'])
                st.subheader("**Your Basic info**")
                try:
                    st.text('Name: ' + resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    # Here's where you insert the code to handle mobile number
                    if resume_data['mobile_number'] is not None:
                        st.text('Contact: ' + str(resume_data['mobile_number']))
                    else:
                        st.text('Contact: Not Available')
                    st.text('Resume pages: ' + str(resume_data['no_of_pages']))
                except KeyError:
                    pass

                cand_level = ''
                if resume_data['no_of_pages'] == 1:
                    cand_level = "Fresher"
                    st.markdown('<h4 style="text-align: left; color: #d73b5c;">You are at Fresher level!</h4>', unsafe_allow_html=True)
                elif resume_data['no_of_pages'] == 2:
                    cand_level = "Intermediate"
                    st.markdown('<h4 style="text-align: left; color: #1ed760;">You are at intermediate level!</h4>', unsafe_allow_html=True)
                elif resume_data['no_of_pages'] >= 3:
                    cand_level = "Experienced"
                    st.markdown('<h4 style="text-align: left; color: #fba171;">You are at experience level!</h4>', unsafe_allow_html=True)

                keywords = st_tags(label='### Your Current Skills', text='See our skills recommendation below', value=resume_data['skills'], key='1')

                ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep learning', 'flask', 'streamlit']
                web_keyword = ['react', 'django', 'node js', 'react js', 'php', 'laravel', 'magento', 'wordpress', 'javascript', 'angular js', 'c#', 'flask']
                android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
                ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
                uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes', 'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator', 'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro', 'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp', 'user research', 'user experience']

                recommended_skills = []
                reco_field = ''
                rec_course = ''
                for i in resume_data['skills']:
                    if i.lower() in ds_keyword:
                        reco_field = 'Data Science'
                        st.success("** Our analysis says you are looking for Data Science Jobs.**")
                        recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling', 'Data Mining', 'Clustering & Classification', 'Data Analytics', 'Quantitative Analysis', 'Web Scraping']
                        rec_course = course_recommender(ds_course)
                        break

                    elif i.lower() in web_keyword:
                        reco_field = 'Web Development'
                        st.success("** Our analysis says you are looking for Web Development Jobs **")
                        recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'PHP', 'Laravel', 'Magento', 'Wordpress', 'Javascript', 'Angular JS', 'C#', 'Flask']
                        rec_course = course_recommender(web_course)
                        break

                    elif i.lower() in android_keyword:
                        reco_field = 'Android Development'
                        st.success("** Our analysis says you are looking for Android Development Jobs **")
                        recommended_skills = ['Android', 'Android Development', 'Flutter', 'Kotlin', 'XML', 'Kivy']
                        rec_course = course_recommender(android_course)
                        break

                    elif i.lower() in ios_keyword:
                        reco_field = 'IOS Development'
                        st.success("** Our analysis says you are looking for IOS Development Jobs **")
                        recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode']
                        rec_course = course_recommender(ios_course)
                        break

                    elif i.lower() in uiux_keyword:
                        reco_field = 'UI-UX Development'
                        st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
                        recommended_skills = ['UX', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq', 'UI', 'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing', 'Adobe Illustrator', 'Adobe After Effects', 'Adobe Premier Pro', 'Adobe Indesign', 'Wireframe', 'Solid', 'Grasp', 'User Research', 'User Experience']
                        rec_course = course_recommender(uiux_course)
                        break

                resume_score = 0
                if 'objective' in resume_text.lower():
                    resume_score += 20
                    st.markdown('<h5 style="text-align: left; color: #d73b5c;">[+] Awesome! You have added your career objective</h5>', unsafe_allow_html=True)
                else:
                    st.markdown('<h5 style="text-align: left; color: #f96b6b;">[-] According to our research, you should add your career objective. It gives you an edge over others.</h5>', unsafe_allow_html=True)

                if 'declaration' in resume_text.lower():
                    resume_score += 20
                    st.markdown('<h5 style="text-align: left; color: #d73b5c;">[+] Awesome! You have added your declaration.</h5>', unsafe_allow_html=True)
                else:
                    st.markdown('<h5 style="text-align: left; color: #f96b6b;">[-] According to our research, you should add your declaration. It gives you an edge over others.</h5>', unsafe_allow_html=True)

                if 'hobbies' in resume_text.lower() or 'interests' in resume_text.lower():
                    resume_score += 20
                    st.markdown('<h5 style="text-align: left; color: #d73b5c;">[+] Awesome! You have added your hobbies.</h5>', unsafe_allow_html=True)
                else:
                    st.markdown('<h5 style="text-align: left; color: #f96b6b;">[-] According to our research, you should add your Hobbies. It gives you an edge over others.</h5>', unsafe_allow_html=True)

                if 'achievements' in resume_text.lower() or 'awards' in resume_text.lower():
                    resume_score += 20
                    st.markdown('<h5 style="text-align: left; color: #d73b5c;">[+] Awesome! You have added your Achievements.</h5>', unsafe_allow_html=True)
                else:
                    st.markdown('<h5 style="text-align: left; color: #f96b6b;">[-] According to our research, you should add your Achievements. It gives you an edge over others.</h5>', unsafe_allow_html=True)

                if 'projects' in resume_text.lower():
                    resume_score += 20
                    st.markdown('<h5 style="text-align: left; color: #d73b5c;">[+] Awesome! You have added your Projects</h5>', unsafe_allow_html=True)
                else:
                    st.markdown('<h5 style="text-align: left; color: #f96b6b;">[-] According to our research, you should add your Projects. It gives you an edge over others.</h5>', unsafe_allow_html=True)

                st.subheader("**Resume Score📝**")
                st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #d73b5c;
                        }
                    </style>""",
                    unsafe_allow_html=True,
                )
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score += 1
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)
                st.success('** Your Resume Writing Score: ' + str(score) + '**')
                st.warning("** Note: This score is calculated based on the content that you have added in your Resume. **")
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date + '_' + cur_time)
                insert_data(connection, cursor, resume_data['name'], resume_data['email'], str(score), timestamp, str(resume_data['no_of_pages']), reco_field, cand_level, str(resume_data['skills']), str(recommended_skills), str(rec_course))

                connection.close()

    else:
        st.success('Welcome to Admin Section')
        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        if st.button('Login'):
            if ad_user == 'rafi' and ad_password == 'rafi157287':
                st.success("Welcome Dr. Briit")
                st.subheader('User Profiles')
                cursor.execute('SELECT * FROM user_data')
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'resume_score', 'Timestamp', 'Page_no', 'Predicted_Field', 'User_level', 'Actual_skills', 'Recommended_skills', 'Recommended_courses'])
                st.dataframe(df)
                st.markdown(get_table_download_link(df, 'User_Data.csv', 'Download Report'), unsafe_allow_html=True)
                query = 'SELECT * FROM user_data;'
                plot_data = pd.read_sql(query, connection)
                connection.close()
                plot_data = pd.DataFrame(data)
                # Ensure correct data types
                data = {
                        'ID': [1, 2, 3],
                        'Name': ['Alice', 'Bob', 'Charlie'],
                        'Email_ID': ['alice@example.com', 'bob@example.com', 'charlie@example.com'],
                        'resume_score': [80, 90, 85],
                        'Timestamp': pd.to_datetime(['2021-01-01', '2021-02-01', '2021-03-01']),
                        'Page_no': [1, 2, 3],
                        'Predicted_Field': ['Data Science', 'Web Development', 'Machine Learning'],
                        'User_level': [3, 4, 5],
                        'Actual_skills': ['Python, SQL', 'HTML, CSS', 'Python, TensorFlow'],
                        'Recommended_skills': ['Machine Learning', 'React', 'Deep Learning'],
                        'Recommended_courses': ['Course A', 'Course B', 'Course C']
                    }
                plot_data = pd.DataFrame(data)

                # Print column names to debug
                print("Column names in plot_data:", plot_data.columns)

                    # Check and rename columns if necessary
                    # Assuming 'resume_score' might be named differently
                if 'resume_score' not in plot_data.columns:
                        # Attempt to find similar columns
                    for col in plot_data.columns:
                        if col.strip().lower() == 'resume_score':
                            plot_data.rename(columns={col: 'resume_score'}, inplace=True)
                            break

                # Ensure correct data types
                plot_data['resume_score'] = plot_data['resume_score'].astype(float)
                plot_data['User_level'] = plot_data['User_level'].astype(int)
                plot_data['Timestamp'] = pd.to_datetime(plot_data['Timestamp'])

                # Create the scatter plot
                fig = px.scatter(plot_data, x='resume_score', y='Timestamp', color='Predicted_Field', size='User_level', hover_data=['Name', 'Email_ID'], title="User Data Scatter Plot")
                    
                # Display the figure in Streamlit
                st.plotly_chart(fig)

                plot_data['resume_score'] = plot_data['resume_score'].astype(float)
                plot_data['User_level'] = plot_data['User_level'].astype(int)
                plot_data['Timestamp'] = pd.to_datetime(plot_data['Timestamp'])
                plot_data['User_level'].replace(['Fresher', 'Intermediate', 'Experienced'], [0, 1, 2], inplace=True)
                plot_data['Predicted_Field'].replace(['Data Science', 'Web Development', 'Android Development', 'IOS Development', 'UI-UX Development'], [0, 1, 2, 3, 4], inplace=True)
                fig = px.scatter(plot_data, x='resume_score', y='Timestamp', color='Predicted_Field', size='User_level', hover_data=['Name', 'Email_ID'], title="User Data Scatter Plot")
                st.plotly_chart(fig)
            else:
                st.error("Wrong ID & Password Provided")

if __name__ == '__main__':
    run()


