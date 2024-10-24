'''
from dotenv import load_dotenv  

load_dotenv() ## load all the environment variables

import streamlit as st 
import os
import google.generativeai as genai 
from PIL import Image 

# initilize streamlit app
st.set_page_config(page_title="GeminiDecode: Multilanguage Document Extraction by Gemini Pro")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse (input, image, prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input, image[0], prompt])
    return response.text

# input=st.text_input("Input Prompt:", key="input")
uploaded_file=st.file_uploader("Choose an image of the document: ",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
submit=st.button("Tell me about the document")

input_prompt="""
You are expert in understanding invoices.
We will upload a image as invoice and you will have to answer any questions based on the uploaded invoce image.
"""

st.header("GeminiDecode: Multilanguage Document Extraction by Gemini Pro")
text= "Utilizing Gemini Pro AI, this project effortlessly extracts vital information + \
from diverse multilingual documents, transcending language barriers with \nprecision and +\
efficiency for enhanced productivity and decision-making."
styled_text = f"<span style='font-family:serif;'>{text}</span>"
st.markdown(styled_text, unsafe_allow_html=True)

# If submit button is clicked
if submit:
   image_data=input_image_details(uploaded_file)
   response=get_gemini_response(input_prompt, image_data, image)
   st.subheader("The response is")
   st.write(response)
'''

import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Set Streamlit page configuration as the first command
st.set_page_config(page_title="GeminiDecode: Multilanguage Document Extraction by Gemini Pro")

# Configure the API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("API key not found. Please set GEMINI_API_KEY in your environment.")
    st.stop()

genai.configure(api_key=api_key)

# Initialize the Streamlit app layout
st.header("GeminiDecode: Multilanguage Document Extraction by Gemini Pro")

text = (
    "Utilizing Gemini Pro AI, this project effortlessly extracts vital information from diverse "
    "multilingual documents, transcending language barriers with precision and efficiency for "
    "enhanced productivity and decision-making."
)
styled_text = f"<span style='font-family:serif;'>{text}</span>"
st.markdown(styled_text, unsafe_allow_html=True)

# Image uploader
uploaded_file = st.file_uploader("Choose an image of the document:", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Input prompt
input_prompt = """
You are an expert in understanding invoices. 
Identifi the language of the invoics, convert into english language from any other languages if not in english.
Analyze the uploaded image and extract key details such as the 
Ex: reciepent name, total amount, bill generated date, due date, merchant name, and invoice number. 
(give the parameter only if available in the invoice considering the mentioned parameters as examples)
Give all the parameters available in the invoice and their respective content associated.
Always give the output in a structured tabular format only.
"""


# Submit button
submit = st.button("Tell me about the document")

# Function to get response from Gemini
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    # Directly pass the PIL Image object
    response = model.generate_content([input, image, prompt])
    return response.text

# If the submit button is clicked
if submit and uploaded_file is not None:
    response = get_gemini_response(input_prompt, image, input_prompt)
    st.subheader("The response is")
    st.write(response)


