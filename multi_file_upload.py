import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Set Streamlit page configuration
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

# Image uploader - allow multiple files to be uploaded
uploaded_files = st.file_uploader("Choose one or more images of the documents:", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Input prompt for document analysis
input_prompt = """
You are an expert in understanding invoices. Analyze the uploaded image and extract key details such as the total amount, due date, merchant name, and invoice number.
"""

# Submit button
submit = st.button("Tell me about the documents")

# Function to get response from Gemini for each image
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    # Generate content based on input, image, and prompt
    response = model.generate_content([input, image, prompt])
    return response.text

# Process each uploaded image if the submit button is clicked
if submit and uploaded_files:
    for uploaded_file in uploaded_files:
        # Open the uploaded image file
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Uploaded Image: {uploaded_file.name}", use_column_width=True)

        # Get response for the current image
        response = get_gemini_response(input_prompt, image, input_prompt)
        
        # Display the response for the image
        st.subheader(f"Response for {uploaded_file.name}:")
        st.write(response)
