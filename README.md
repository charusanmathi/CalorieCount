# 🍎 Calorie Compass

Calorie Compass is an AI-powered application that lets users upload photos of meals to get a detailed nutritional analysis. Using Google's Gemini AI, it identifies ingredients, estimates calories, and offers actionable health insights.

## 🎯 Features

- Identify ingredients and estimate their calorie content.
- Provide a nutrient breakdown (protein, carbs, fiber, sugar, fats).
- Calorie visualization with pie charts for better understanding.
- Health suggestions for making meals healthier.
- Simple and intuitive Streamlit UI with interactive elements.
  
## 🛠️ Technologies

- Python with Streamlit for frontend development
- Google Gemini AI for image analysis and NLP
-Matplotlib for visualizations


## 🚀 Getting Started

1. Clone the repository:
````
git clone https://github.com/YourUsername/calorie-compass.git  
cd calorie-compass
````

2. Install dependencies:
````
pip install -r requirements.txt
````

3. Set your Google API Key in a .env file:
````
GOOGLE_API_KEY=your_api_key
````

4. Run the app:
````
streamlit run app.py
````

## 📸 Usage

1. Upload an image of your meal.
2. View the ingredient list, calorie count, and nutrient breakdown.
3. Check out health tips and modify recipes if needed.
