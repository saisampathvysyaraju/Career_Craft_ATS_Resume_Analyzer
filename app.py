import streamlit as st
from dotenv import load_dotenv
from google import genai
import os
import PyPDF2
from PIL import Image
from streamlit_extras import add_vertical_space as avs

# Load environment variables
load_dotenv()

# Streamlit configuration
st.set_page_config(page_title="ATS Resume Analyzer", layout="wide")

# Custom CSS for background color and other UI elements
custom_css = """
    <style>
    body {
        background-color: #3CD795;
    }
    .stApp {
        background-color: #3CD795;
    }
    textarea {
        background-color: #d9f5ec !important;
        color: #1e5f4b !important;
        font-size: 16px !important;
        border: 2px solid #1e5f4b !important;
    }
    .stFileUploadDragAndDrop {
        background-color: #e5f9f2 !important;
        border: 2px dashed #1e5f4b !important;
    }
    .stFileUploadLabel {
        color: #1e5f4b !important;
        font-weight: bold;
    }
    div.stButton > button {
        background-color: #1e5f4b !important;
        color: white !important;
        font-size: 16px !important;
        border-radius: 10px !important;
        height: 50px;
        width: 100%;
        border: none;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #146145 !important;
    }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

client = genai.Client()

# Function to get the Gemini response
def get_gemini_response(resume_text, jd_text):
    input_prompt = f"""
        As an experienced ATS (Applicant Tracking System), proficient in the technical domain encompassing
        Software Engineering, Data Science, Data Analysis, Big Data Engineering, Web Developer, Mobile App
        Developer, DevOps Engineer, Machine Learning Engineer, Cybersecurity Analyst, Cloud Solutions Architect,
        Database Administrator, Network Engineer, AI Engineer, Systems Analyst, Full Stack Developer, UI/UX
        Designer, IT Project Manager, and additional specialized areas, your objective is to meticulously assess
        resumes against provided job descriptions. In a fiercely competitive job market, your expertise is crucial
        in offering top-notch guidance for resume enhancement. Assign precise matching percentages based on the JD
        (Job Description) and meticulously identify any missing keywords with utmost accuracy.

        Resume: {resume_text}
        Job Description: {jd_text}

        I want the response in the following structure:
        The first line indicates the percentage match with the job description (JD).
        The second line presents a list of missing keywords.
        The third section provides a profile summary.

        Mention the title for all the three sections.
        While generating the response, put some space to separate all three sections.
        """
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[input_prompt]
        )
        if response.candidates and len(response.candidates) > 0:
            return response.candidates[0].content.parts[0].text
        return "Error: Unable to retrieve response."
    except Exception as e:
        return f"An error occurred: {e}"

# Extract text from PDF
def input_pdf_text(upload_file):
    reader = PyPDF2.PdfReader(upload_file)
    text = ''.join([reader.pages[i].extract_text() for i in range(len(reader.pages))])
    return text

# Load and rotate images
img1 = Image.open("images/icon1.png").rotate(-90, expand=True)
img2 = Image.open("images/icon2.png").rotate(-90, expand=True)
img3 = Image.open("images/icon3.png").rotate(-90, expand=True)

# Streamlit UI
avs.add_vertical_space(4)
col1, col2 = st.columns([3, 2])

with col1:
    st.title("CareerCraft")
    st.header("Navigate the Job Market with Confidence!")
    st.markdown(
        """<p style='text-align: justify;'>Introducing CareerCraft, an ATS-Optimized Resume Analyzer...</p>""",
        unsafe_allow_html=True
    )

with col2:
    # Changed use_container_width to use_column_width
    st.image('https://cdn.dribbble.com/userupload/12500996/file/original-b458fe398a6d7f4e9999ce66ec856ff9.gif', use_column_width=True)


# Displaying offerings
avs.add_vertical_space(10)
col1, col2 = st.columns([3, 2])

with col2:
    st.header("Wide Range of Offerings")
    st.write('ATS-Optimized Resume Analysis')
    st.write('Resume Optimization')
    st.write('Skill Enhancement')
    st.write('Career Progression Guidance')
    st.write('Tailored Profile Summaries')
    st.write('Streamlined Application Process')
    st.write('Personalized Recommendations')
    st.write('Efficient Career Navigation')

with col1:
    # Changed use_container_width to use_column_width
    st.image(img1, use_column_width=True)  # Display rotated image

# Job description and resume input
avs.add_vertical_space(10)
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("<h1 style='text-align: center;'>Embark on Your Career Adventure</h1>", unsafe_allow_html=True)
    jd = st.text_area("Paste the Job Description")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", help="Upload the PDF of your resume")

    submit = st.button("Submit")

    if submit:
        if uploaded_file is not None and jd.strip():
            resume_text = input_pdf_text(uploaded_file)
            response = get_gemini_response(resume_text, jd)

            # Replace <br>'s with newline characters for plain text display
            cleaned_response = response.replace('<br>', '\n')

            st.header("ATS Analysis Results")
            st.write(cleaned_response) # Display the cleaned response
        else:
            st.error("Please upload a resume and provide the job description.")

with col2:
    # Changed use_container_width to use_column_width
    st.image(img2, use_column_width=True)  # Display rotated image

# FAQ section
avs.add_vertical_space(10)
col1, col2 = st.columns([2, 3])

with col2:
    st.markdown("<h1 style='text-align: center;'>FAQ</h1>", unsafe_allow_html=True)
    st.write("**Question:** How does CareerCraft analyze resumes and job descriptions?")
    st.write("**Answer:** CareerCraft uses advanced algorithms to analyze resumes and job descriptions, identifying key keywords and assessing compatibility.")

    avs.add_vertical_space(3)

    st.write("**Question:** Can CareerCraft suggest improvements for my resume?")
    st.write("**Answer:** Yes, CareerCraft provides personalized recommendations to optimize your resume, including suggestions for missing keywords.")

    avs.add_vertical_space(3)

    st.write("**Question:** Is CareerCraft suitable for both entry-level and experienced professionals?")
    st.write("**Answer:** Absolutely! CareerCraft caters to job seekers at all career stages, offering tailored insights and guidance to enhance their resumes.")

with col1:
    # Changed use_container_width to use_column_width
    st.image(img3, use_column_width=True)  # Display rotated images