import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import requests
import json
import base64
import numpy as np
from sklearn import svm
from sklearn.linear_model import LogisticRegression

# Set page configuration
st.set_page_config(
    page_title="AI Health Copilot",
    layout="wide",
    page_icon="🧑‍⚕️"
)

# Add custom CSS for styling and animations
st.markdown(
    """
    <style>
    /* General Styling */
    body {
        background-color: #f9f9f9;
        color: #333;
    }
    /* Purple Hover Effects */
    button:hover, a:hover, [role="button"]:hover, label:hover, div[data-testid="stFileUploadDropzone"] div:hover {
        background-color: #8e44ad !important;
        color: #fff !important;
    }
    /* Sidebar Padding Optimized */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 10px !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
        padding-bottom: 10px !important;
    }
    /* Input Field Animations */
    .input-field input {
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        transition: border-color 0.3s ease;
        width: 100%;
    }
    .input-field input:focus {
        border-color: #8e44ad;
        outline: none;
    }
    /* Footer Styling */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #8e44ad;
        color: white;
        text-align: center;
        padding: 10px 0;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to get API key from secrets
def get_api_key():
    try:
        return st.secrets["OPENROUTER_API_KEY"]
    except KeyError:
        return None

# Function to generate Qwen QwQ response using OpenRouter
def generate_qwen_response(prompt, api_key, model="qwen/qwq-32b-preview"):
    """Generate response using Qwen QwQ 32B via OpenRouter."""
    if not api_key:
        return "❌ Error: OpenRouter API key not found in secrets."
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://streamlit.io",
            "X-Title": "AI Health Copilot"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful medical AI assistant. Provide informative and helpful health-related responses while being clear that you are not a replacement for professional medical advice."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"❌ Error: API request failed with status {response.status_code}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Create dummy models if they don't exist
def create_dummy_models():
    """Create dummy models for demonstration purposes."""
    try:
        os.makedirs('saved_models', exist_ok=True)
        
        # Create dummy diabetes model
        if not os.path.exists('saved_models/diabetes_model.sav'):
            dummy_model = svm.SVC(kernel='linear')
            # Create dummy training data
            X_dummy = np.random.rand(100, 8)
            y_dummy = np.random.randint(0, 2, 100)
            dummy_model.fit(X_dummy, y_dummy)
            pickle.dump(dummy_model, open('saved_models/diabetes_model.sav', 'wb'))
        
        # Create dummy heart disease model
        if not os.path.exists('saved_models/heart_disease_model.sav'):
            dummy_model = LogisticRegression()
            X_dummy = np.random.rand(100, 13)
            y_dummy = np.random.randint(0, 2, 100)
            dummy_model.fit(X_dummy, y_dummy)
            pickle.dump(dummy_model, open('saved_models/heart_disease_model.sav', 'wb'))
        
        # Create dummy parkinsons model
        if not os.path.exists('saved_models/parkinsons_model.sav'):
            dummy_model = svm.SVC(kernel='linear')
            X_dummy = np.random.rand(100, 22)
            y_dummy = np.random.randint(0, 2, 100)
            dummy_model.fit(X_dummy, y_dummy)
            pickle.dump(dummy_model, open('saved_models/parkinsons_model.sav', 'wb'))
            
    except Exception as e:
        st.error(f"Error creating models: {e}")

# Initialize models
create_dummy_models()

# Getting the working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Loading the saved models
try:
    diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
    heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
    parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()

# Display a simple logo placeholder instead of image
def display_logo():
    st.sidebar.markdown(
        """
        <div style="text-align:center; padding: 20px;">
            <div style="background: linear-gradient(45deg, #8e44ad, #3498db); 
                        color: white; padding: 20px; border-radius: 10px; 
                        font-size: 24px; font-weight: bold;">
                🧑‍⚕️ AI Health Copilot
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

display_logo()

# Get API key
api_key = get_api_key()

# Sidebar for navigation
with st.sidebar:
    st.header("🔑 API Configuration")
    
    if api_key:
        st.success("✅ OpenRouter API Key loaded from secrets!")
        st.info("Using Qwen QwQ 32B model")
    else:
        st.error("❌ OpenRouter API key not found in secrets.toml")
        st.markdown("Please add your OpenRouter API key to `.streamlit/secrets.toml`")
        st.code('OPENROUTER_API_KEY = "your_api_key_here"')

    selected = option_menu(
        'AI Health Copilot',
        ['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction', 'Personalized Health Plan'],
        menu_icon='hospital-fill',
        icons=['activity', 'heart', 'person', 'gear'],
        default_index=0
    )

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.title('🩺 Diabetes Prediction using ML')

    def input_field(label, min_val, max_val, key, help_text=""):
        return st.number_input(label, min_value=min_val, max_value=max_val, key=key, help=help_text)

    col1, col2, col3 = st.columns(3)
    with col1:
        Pregnancies = input_field('Number of Pregnancies', 0, 17, key="diabetes_pregnancies", help_text="Number of times pregnant")
    with col2:
        Glucose = input_field('Glucose Level', 0, 199, key="diabetes_glucose", help_text="Plasma glucose concentration")
    with col3:
        BloodPressure = input_field('Blood Pressure value', 0, 122, key="diabetes_bp", help_text="Diastolic blood pressure (mm Hg)")
    with col1:
        SkinThickness = input_field('Skin Thickness value', 0, 99, key="diabetes_skin", help_text="Triceps skin fold thickness (mm)")
    with col2:
        Insulin = input_field('Insulin Level', 0, 846, key="diabetes_insulin", help_text="2-Hour serum insulin (mu U/ml)")
    with col3:
        BMI = input_field('BMI value', 0.0, 67.1, key="diabetes_bmi", help_text="Body mass index (weight in kg/(height in m)^2)")
    with col1:
        DiabetesPedigreeFunction = input_field('Diabetes Pedigree Function value', 0.0, 2.42, key="diabetes_pedigree", help_text="Diabetes pedigree function")
    with col2:
        Age = input_field('Age of the Person', 21, 81, key="diabetes_age", help_text="Age in years")

    diab_diagnosis = ''
    if st.button('🔍 Diabetes Test Result', key="diabetes_test_button"):
        try:
            user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
            diab_prediction = diabetes_model.predict([user_input])
            diab_diagnosis = 'The person is diabetic' if diab_prediction[0] == 1 else 'The person is not diabetic'

            # AI explanation using Qwen QwQ
            if api_key:
                prompt = f"""Based on the following diabetes prediction results:
                - Prediction: {diab_diagnosis}
                - Patient data: Pregnancies={Pregnancies}, Glucose={Glucose}, Blood Pressure={BloodPressure}, 
                  Skin Thickness={SkinThickness}, Insulin={Insulin}, BMI={BMI}, 
                  Diabetes Pedigree Function={DiabetesPedigreeFunction}, Age={Age}
                
                Please provide a brief medical explanation (max 3 paragraphs) about:
                1. What this prediction means
                2. Key risk factors observed
                3. General health recommendations
                
                Remember to note that this is for informational purposes and not a substitute for professional medical advice."""
                
                with st.spinner("Generating AI explanation..."):
                    response = generate_qwen_response(prompt, api_key)
                    st.info("🤖 AI Medical Assistant Explanation:")
                    st.write(response)
            
            if diab_diagnosis:
                if 'diabetic' in diab_diagnosis and 'not' not in diab_diagnosis:
                    st.error(f"⚠️ {diab_diagnosis}")
                else:
                    st.success(f"✅ {diab_diagnosis}")
                    
        except Exception as e:
            st.error(f"Error during prediction: {e}")

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    st.title('❤️ Heart Disease Prediction using ML')

    def input_field(label, min_val, max_val, key, help_text=""):
        return st.number_input(label, min_value=min_val, max_value=max_val, key=key, help=help_text)

    col1, col2, col3 = st.columns(3)
    with col1:
        age = input_field('Age', 29, 77, key="heart_age", help_text="Age in years")
    with col2:
        sex = input_field('Sex (0=Female, 1=Male)', 0, 1, key="heart_sex")
    with col3:
        cp = input_field('Chest Pain types (0-3)', 0, 3, key="heart_cp")
    with col1:
        trestbps = input_field('Resting Blood Pressure', 94, 200, key="heart_trestbps")
    with col2:
        chol = input_field('Serum Cholesterol in mg/dl', 126, 564, key="heart_chol")
    with col3:
        fbs = input_field('Fasting Blood Sugar > 120 mg/dl (0=No, 1=Yes)', 0, 1, key="heart_fbs")
    with col1:
        restecg = input_field('Resting Electrocardiographic results (0-2)', 0, 2, key="heart_restecg")
    with col2:
        thalach = input_field('Maximum Heart Rate achieved', 71, 202, key="heart_thalach")
    with col3:
        exang = input_field('Exercise Induced Angina (0=No, 1=Yes)', 0, 1, key="heart_exang")
    with col1:
        oldpeak = input_field('ST depression induced by exercise', 0.0, 6.2, key="heart_oldpeak")
    with col2:
        slope = input_field('Slope of the peak exercise ST segment (0-2)', 0, 2, key="heart_slope")
    with col3:
        ca = input_field('Major vessels colored by fluoroscopy (0-4)', 0, 4, key="heart_ca")
    with col1:
        thal = input_field('Thal (0=normal, 1=fixed defect, 2=reversible defect)', 0, 3, key="heart_thal")

    heart_diagnosis = ''
    if st.button('💓 Heart Disease Test Result', key="heart_test_button"):
        try:
            user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
            heart_prediction = heart_disease_model.predict([user_input])
            heart_diagnosis = 'The person is having heart disease' if heart_prediction[0] == 1 else 'The person does not have any heart disease'

            # AI explanation using Qwen QwQ
            if api_key:
                prompt = f"""Based on the following heart disease prediction results:
                - Prediction: {heart_diagnosis}
                - Patient data: Age={age}, Sex={'Male' if sex==1 else 'Female'}, Chest Pain Type={cp}, 
                  Resting BP={trestbps}, Cholesterol={chol}, Fasting Blood Sugar={fbs}, 
                  Resting ECG={restecg}, Max Heart Rate={thalach}, Exercise Angina={exang}, 
                  ST Depression={oldpeak}, Slope={slope}, Major Vessels={ca}, Thal={thal}
                
                Please provide a brief medical explanation (max 3 paragraphs) about:
                1. What this prediction means
                2. Key cardiovascular risk factors observed
                3. General heart health recommendations
                
                Remember to note that this is for informational purposes and not a substitute for professional medical advice."""
                
                with st.spinner("Generating AI explanation..."):
                    response = generate_qwen_response(prompt, api_key)
                    st.info("🤖 AI Medical Assistant Explanation:")
                    st.write(response)
            
            if heart_diagnosis:
                if 'having heart disease' in heart_diagnosis:
                    st.error(f"⚠️ {heart_diagnosis}")
                else:
                    st.success(f"✅ {heart_diagnosis}")
                    
        except Exception as e:
            st.error(f"Error during prediction: {e}")

# Parkinson's Prediction Page
if selected == "Parkinsons Prediction":
    st.title("🧠 Parkinson's Disease Prediction using ML")
    
    st.info("This prediction uses voice measurement data. Enter the voice analysis parameters below:")

    def input_field(label, min_val, max_val, key, help_text=""):
        return st.number_input(label, min_value=min_val, max_value=max_val, key=key, help=help_text, format="%.6f")

    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Simplified input for key parameters
    with col1:
        fo = input_field('Average vocal fundamental frequency', 88.33, 260.10, key="parkinsons_fo")
    with col2:
        fhi = input_field('Maximum vocal fundamental frequency', 102.14, 592.03, key="parkinsons_fhi")
    with col3:
        flo = input_field('Minimum vocal fundamental frequency', 65.47, 239.17, key="parkinsons_flo")
    with col4:
        Jitter_percent = input_field('Jitter percentage', 0.00168, 0.03316, key="parkinsons_jitter_percent")
    with col5:
        Jitter_Abs = input_field('Absolute jitter', 0.000007, 0.00261, key="parkinsons_jitter_abs")

    # Default values for other parameters (simplified for demo)
    RAP = 0.003
    PPQ = 0.003
    DDP = 0.009
    Shimmer = 0.029
    Shimmer_dB = 0.282
    APQ3 = 0.017
    APQ5 = 0.020
    APQ = 0.024
    DDA = 0.047
    NHR = 0.025
    HNR = 21.9
    RPDE = 0.499
    DFA = 0.718
    spread1 = -5.68
    spread2 = 0.227
    D2 = 2.38
    PPE = 0.207

    parkinsons_diagnosis = ''
    if st.button("🔬 Parkinson's Test Result", key="parkinsons_test_button"):
        try:
            user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, 
                         APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]
            parkinsons_prediction = parkinsons_model.predict([user_input])
            parkinsons_diagnosis = "The person has Parkinson's disease" if parkinsons_prediction[0] == 1 else "The person does not have Parkinson's disease"

            # AI explanation using Qwen QwQ
            if api_key:
                prompt = f"""Based on the following Parkinson's disease prediction results:
                - Prediction: {parkinsons_diagnosis}
                - Voice analysis data: Fundamental frequency (average={fo}, max={fhi}, min={flo}), 
                  Jitter percentage={Jitter_percent}, Absolute jitter={Jitter_Abs}
                
                Please provide a brief medical explanation (max 3 paragraphs) about:
                1. What this prediction means
                2. How voice analysis relates to Parkinson's disease
                3. General recommendations for neurological health
                
                Remember to note that this is for informational purposes and not a substitute for professional medical advice."""
                
                with st.spinner("Generating AI explanation..."):
                    response = generate_qwen_response(prompt, api_key)
                    st.info("🤖 AI Medical Assistant Explanation:")
                    st.write(response)
            
            if parkinsons_diagnosis:
                if 'has Parkinson' in parkinsons_diagnosis:
                    st.error(f"⚠️ {parkinsons_diagnosis}")
                else:
                    st.success(f"✅ {parkinsons_diagnosis}")
                    
        except Exception as e:
            st.error(f"Error during prediction: {e}")

# Personalized Health Plan Page
if selected == "Personalized Health Plan":
    st.title("🎯 Personalized Health & Fitness Planner")

    if not api_key:
        st.error("⚠️ API key not available. Please configure OpenRouter API key in secrets.toml")
        st.stop()

    st.markdown("""
        <div style='background-color: #f0f8ff; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem;'>
            <p style='color: #333333; font-size: 1.1rem; font-family: Arial, sans-serif;'>
            Get personalized dietary and fitness plans tailored to your goals and preferences.
            Our AI-powered system considers your unique profile to create the perfect plan for you.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.header("👤 Your Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=10, max_value=100, step=1, help="Enter your age", key="profile_age")
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, step=0.1, key="profile_height")
        activity_level = st.selectbox(
            "Activity Level",
            options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
            help="Choose your typical activity level",
            key="profile_activity"
        )
        dietary_preferences = st.selectbox(
            "Dietary Preferences",
            options=["Vegetarian", "Keto", "Gluten Free", "Low Carb", "Dairy Free", "Mediterranean", "Standard"],
            help="Select your dietary preference",
            key="profile_diet"
        )
        
    with col2:
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, step=0.1, key="profile_weight")
        sex = st.selectbox("Sex", options=["Male", "Female", "Other"], key="profile_sex")
        fitness_goals = st.selectbox(
            "Fitness Goals",
            options=["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training", "General Health"],
            help="What do you want to achieve?",
            key="profile_goals"
        )

    if st.button("🎯 Generate My Personalized Plan", use_container_width=True, key="generate_plan_button"):
        with st.spinner("Creating your perfect health and fitness routine..."):
            try:
                user_profile = f"""
                Age: {age}
                Weight: {weight}kg
                Height: {height}cm
                Sex: {sex}
                Activity Level: {activity_level}
                Dietary Preferences: {dietary_preferences}
                Fitness Goals: {fitness_goals}
                """
                
                # Generate dietary plan
                dietary_prompt = f"""As a nutrition expert, create a personalized daily meal plan for someone with this profile:
                {user_profile}
                
                Please provide:
                1. A complete daily meal plan (breakfast, lunch, dinner, 2 snacks)
                2. Explanation of why this plan works for their goals
                3. Important nutritional considerations
                4. Estimated daily calorie range
                
                Keep the response practical and actionable, around 300-400 words."""
                
                dietary_response = generate_qwen_response(dietary_prompt, api_key)
                
                # Generate fitness plan
                fitness_prompt = f"""As a fitness expert, create a personalized weekly exercise routine for someone with this profile:
                {user_profile}
                
                Please provide:
                1. A weekly workout schedule with specific exercises
                2. Duration and intensity recommendations
                3. Progression guidelines
                4. Important safety considerations
                
                Keep the response practical and actionable, around 300-400 words."""
                
                fitness_response = generate_qwen_response(fitness_prompt, api_key)
                
                # Display results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🍽️ Your Personalized Dietary Plan")
                    st.info(dietary_response)
                
                with col2:
                    st.markdown("### 💪 Your Personalized Fitness Plan")
                    st.info(fitness_response)
                
                # Additional health tips
                health_tips_prompt = f"""Based on this health profile:
                {user_profile}
                
                Provide 5 quick, practical health tips specifically tailored to this person's goals and lifestyle. Keep each tip to 1-2 sentences."""
                
                health_tips = generate_qwen_response(health_tips_prompt, api_key)
                
                st.markdown("### 💡 Personalized Health Tips")
                st.success(health_tips)
                
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")

# Add footer
st.markdown(
    """
    <div class="footer">
        <span class="disclaimer-icon" 
              title="Disclaimer: AI may not always provide accurate or complete information. 
                     Agentic AI x Corporate Learning Division">
              ℹ️
        </span>
        <span>All rights reserved. © 2025 Patria & Co. | Powered by Qwen QwQ 32B via OpenRouter</span>
    </div>
    """,
    unsafe_allow_html=True
)
