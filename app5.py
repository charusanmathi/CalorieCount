import matplotlib.pyplot as plt
import streamlit as st
from dotenv import load_dotenv, find_dotenv
import os
import google.generativeai as genai
from PIL import Image
import base64

# Load environment variables from the .env file
load_dotenv(find_dotenv())

# Configure Streamlit page settings
st.set_page_config(page_title="Calorie Compass", page_icon="🍎", layout="wide")

# Configure Google Generative AI library with an API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Apply custom CSS to enhance the Streamlit app's appearance
st.markdown("""
    <style>
        body {
            background-color: #f9fafc;  /* Subtle background color */
        }
        .stApp {
            font-family: 'Arial', sans-serif;  /* Clean font */
        }
        .main-header {
            color: #4CAF50;  /* Green header */
            text-align: center; 
            font-size: 40px; 
            font-weight: bold;
        }
        .sub-header {
            color: #333333;  /* Darker sub-header color */
            text-align: center;
            font-size: 20px;
        }
        .uploaded-image {
            margin: 20px auto; 
            border: 2px solid #ddd;  /* Border for the uploaded image */
            border-radius: 8px;
        }
        .stButton > button {
            background-color: #4CAF50 !important;  /* Green button */
            border: none;
            color: white;
            padding: 12px 24px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
        }
        .stButton > button:hover {
            background-color: #45a049 !important;  /* Darker green on hover */
        }
        .response-box {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

# Define a function to handle the response from Google Gemini API
def get_gemini_response(input, image):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content([input, image[0]])
    if response.candidates and response.candidates[0].content.parts:
        return response.candidates[0].content.parts[0].text
    else:
        return "No response generated."

# Define a function to set up image uploading and handle the image data
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No image uploaded")

# Header Section
st.markdown('<h1 class="main-header">🍎 CALORIE COMPASS </h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload a meal photo and discover its nutritional value!</p>', unsafe_allow_html=True)

# Sidebar for navigation and file upload
st.sidebar.header("📂 Upload Section")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Image display in main content area
if uploaded_file is not None:
    # Read the uploaded file into binary data
    bytes_data = uploaded_file.getvalue()
    
    # Encode the binary data into a Base64 string
    base64_image = base64.b64encode(bytes_data).decode("utf-8")
    
    # Embed the image in a styled HTML block
    st.markdown(
        f"""
        <div style="text-align: center; margin: 20px auto; border: 2px solid #ddd; border-radius: 8px; padding: 10px;">
            <img src="data:{uploaded_file.type};base64,{base64_image}" alt="Uploaded Image" style="max-width: 100%; border-radius: 8px;">
        </div>
        """,
        unsafe_allow_html=True,
    )

# Button for food analysis
submit = st.button("🔍 Analyze this Food")

# AI model input prompt
input_prompt = """
You are an expert nutritionist analyzing the food items in the image.
Start by determining if the image contains food items. 
If the image does not contain any food items, 
clearly state "No food items detected in the image." 
and do not provide any calorie information. 
If food items are detected, 
start by naming the meal based on the image, 
identify and list every ingredient you can find in the image, 
and then estimate the total calories for each ingredient. 

Summarize the total calories based on the identified ingredients. 
Follow the format below:

If food items are detected:
Meal Name: [Name of the meal]

1. Ingredient 1 - estimated calories
2. Ingredient 2 - estimated calories
----
Total estimated calories: X

Finally, mention whether the food is healthy or not, 
and provide the percentage split of protein, carbs, fibre, sugar and fats in the food item. 

Also, mention the total fiber content in the food item and any other important details.

Provide a recommendation on how to modify the recipe if its unhealthy to a healthy one.

Note: Always identify ingredients and provide an estimated calorie count, 
even if some details are uncertain.
"""

# Perform analysis when the button is clicked
if submit:
    with st.spinner("Processing..."):
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)
            st.markdown('<div class="response-box"><h3>🍴 Food Analysis</h3></div>', unsafe_allow_html=True)
            st.write(response)
            
            # Assuming the response contains the nutritional breakdown
            # You can adjust this part based on how the response is structured
            nutrition_data = {
                'Protein': 25,  # Example data
                'Carbohydrates': 50,
                'Fats': 15,
                'Fiber': 8,
                'Sugar': 10
            }

            # Calories for each component (in kcal)
            calories = {
                'Protein': nutrition_data['Protein'] * 4,
                'Carbohydrates': nutrition_data['Carbohydrates'] * 4,
                'Fats': nutrition_data['Fats'] * 9,
                'Fiber': nutrition_data['Fiber'] * 2,  # Approximation
                'Sugar': nutrition_data['Sugar'] * 4
            }

            total_calories = sum(calories.values())

            # Pie chart generation
            labels = calories.keys()
            sizes = calories.values()
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

            # Display the pie chart
            st.pyplot(fig)

            # Display the total calories and nutrition details
            st.write(f"Total Estimated Calories: {total_calories:.2f} kcal")
            st.write("Nutritional Breakdown:")
            for nutrient, value in nutrition_data.items():
                st.write(f"{nutrient}: {value}g")

        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
