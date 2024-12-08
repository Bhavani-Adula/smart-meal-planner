
import os
import openai
import streamlit as st

# Load OpenAI API key from environment variable
API_KEY = os.getenv("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")
if not API_KEY:
    st.error("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
else:
    openai.api_key = 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

# Function to get meal plan with OpenAI
def get_meal_plan_with_descriptions(calories, restrictions):
    prompt = (
        f"Design a detailed meal plan for one day, tailored to provide approximately {calories} calories. "
        f"The plan should include five meals: breakfast, lunch, dinner, and two snacks. For each meal, specify: "
        f"The meal name, the main ingredient, and a brief description of the meal. "
        f"Ensure the meal plan adheres to the following dietary restrictions: {', '.join(restrictions)}. "
        f"The total calorie count should align with the specified target, and the meals should be diverse and balanced."
    )

    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Use any OpenAI model suitable for text generation
            prompt=prompt,
            max_tokens=700,
            temperature=0.7
        )
        meal_plan = response.choices[0].text.strip()
    except Exception as e:
        meal_plan = f"Error generating meal plan: {str(e)}"

    return meal_plan

# Calorie calculation function
def calculate_calories(age, weight, height, gender):
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    daily_calories = bmr * 1.55  # Moderate activity factor
    return daily_calories

# Streamlit application
st.title("Daily Calorie Intake & Meal Plan with OpenAI")

name = st.text_input("Name")
age = st.number_input("Age", min_value=1, max_value=120, step=1)
weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, step=0.1)
height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, step=0.1)
gender = st.selectbox("Gender", ["Male", "Female"])
restrictions = st.multiselect("Dietary Restrictions", ["Diabetic", "Vegan", "Vegetarian", "Gluten-Free", "Lactose-Free", "Low-Carb"])

if st.button("Calculate & Get Meal Plan"):
    if all([name, age, weight, height, gender]):
        daily_calories = calculate_calories(age, weight, height, gender)
        meal_plan = get_meal_plan_with_descriptions(daily_calories, restrictions)
        st.success(f"Hello {name}! Your daily caloric requirement is approximately {daily_calories:.2f} calories.")
        st.subheader("Suggested Meal Plan with Descriptions:")
        st.write(meal_plan)
    else:
        st.error("Please fill in all fields.")
