import streamlit as st
import requests
import json

# Page config
st.set_page_config(page_title="AI Health Copilot", page_icon="🧑‍⚕️", layout="wide")

# Title & Header
st.title("🧑‍⚕️ AI Health Copilot")
st.markdown("**Smart Health Assessment with AI-Powered Insights**")

# Sidebar Configuration
with st.sidebar:
    st.title("🔧 Configuration")
    
    # API Key handling
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
        st.success("✅ API Connected")
        st.info("🤖 Model: Meta Llama 4 Maverick")
    except:
        api_key = st.text_input("Enter OpenRouter API Key:", type="password", help="Get from https://openrouter.ai/")
        if not api_key:
            st.error("❌ API Key Required")
            st.code('Get free API key from: https://openrouter.ai/')

# Optimized AI Response Function
def get_ai_response(prompt, max_tokens=300):
    """Get AI response with improved error handling"""
    if not api_key:
        return "⚠️ API key required for AI insights"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ai-health-copilot.streamlit.app",
        "X-Title": "AI Health Copilot"
    }
    
    payload = {
        "model": "meta-llama/llama-4-maverick-17b-128e-instruct:free",
        "messages": [
            {
                "role": "system", 
                "content": "You are a helpful health advisor. Provide brief, practical health advice. Always remind users to consult healthcare professionals for serious concerns."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "top_p": 0.9,
        "stream": False
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        elif response.status_code == 402:
            return "💳 API quota exceeded. Please check your OpenRouter account."
        elif response.status_code == 401:
            return "🔑 Invalid API key. Please check your credentials."
        elif response.status_code == 429:
            return "⏱️ Rate limit exceeded. Please try again in a moment."
        else:
            return f"❌ API Error {response.status_code}: {response.text[:100]}"
            
    except requests.exceptions.Timeout:
        return "⏱️ Request timeout. Please try again."
    except requests.exceptions.ConnectionError:
        return "🌐 Connection error. Check your internet connection."
    except Exception as e:
        return f"❌ Unexpected error: {str(e)[:100]}"

# Health calculation functions
def calculate_risk_score(age, lifestyle_factors):
    """Calculate health risk score"""
    score = 0
    if age > 65: score += 3
    elif age > 50: score += 2
    elif age > 35: score += 1
    
    score += sum(lifestyle_factors.values())
    return min(score, 10)

def get_risk_level(score):
    """Get risk level and color"""
    if score <= 3:
        return "Low", "success", "✅"
    elif score <= 6:
        return "Moderate", "warning", "⚠️"
    else:
        return "High", "error", "🚨"

# Navigation
page = st.sidebar.selectbox(
    "Choose Assessment",
    ["🩺 Health Risk", "❤️ Heart Health", "🎯 Health Tips", "📊 BMI Calculator"]
)

# Main Pages
if page == "🩺 Health Risk":
    st.header("🩺 General Health Risk Assessment")
    
    with st.form("health_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", 18, 100, 35)
            exercise = st.selectbox("Exercise Frequency", ["Daily", "3-4x/week", "1-2x/week", "Rarely", "Never"])
            diet = st.selectbox("Diet Quality", ["Excellent", "Good", "Fair", "Poor"])
            sleep = st.selectbox("Sleep Hours/Night", ["8-9", "7-8", "6-7", "5-6", "<5"])
        
        with col2:
            stress = st.selectbox("Stress Level", ["Low", "Moderate", "High", "Very High"])
            smoking = st.selectbox("Smoking Status", ["Never", "Former (>1yr)", "Former (<1yr)", "Current"])
            alcohol = st.selectbox("Alcohol Consumption", ["None", "Light", "Moderate", "Heavy"])
            family_history = st.checkbox("Family History of Chronic Disease")
        
        submitted = st.form_submit_button("🔍 Calculate Health Risk", use_container_width=True)
        
        if submitted:
            # Calculate lifestyle factors
            lifestyle_factors = {
                'exercise': {"Never": 3, "Rarely": 2, "1-2x/week": 1, "3-4x/week": 0, "Daily": 0}[exercise],
                'diet': {"Poor": 2, "Fair": 1, "Good": 0, "Excellent": 0}[diet],
                'sleep': {"<5": 3, "5-6": 2, "6-7": 1, "7-8": 0, "8-9": 0}[sleep],
                'stress': {"Very High": 2, "High": 1, "Moderate": 0, "Low": 0}[stress],
                'smoking': {"Current": 3, "Former (<1yr)": 2, "Former (>1yr)": 1, "Never": 0}[smoking],
                'alcohol': {"Heavy": 2, "Moderate": 1, "Light": 0, "None": 0}[alcohol],
                'family': 1 if family_history else 0
            }
            
            risk_score = calculate_risk_score(age, lifestyle_factors)
            risk_level, status_type, icon = get_risk_level(risk_score)
            
            # Display results
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Risk Score", f"{risk_score}/10")
            with col2:
                st.metric("Risk Level", risk_level)
            with col3:
                st.metric("Age Factor", f"{age} years")
            
            # Status message
            if status_type == "success":
                st.success(f"{icon} **{risk_level} Risk** - Great health indicators!")
            elif status_type == "warning":
                st.warning(f"{icon} **{risk_level} Risk** - Some areas for improvement")
            else:
                st.error(f"{icon} **{risk_level} Risk** - Consider lifestyle changes")
            
            # AI Insights
            if api_key:
                with st.spinner("🤖 Getting AI health insights..."):
                    prompt = f"""Health Assessment Results:
                    - Age: {age} years
                    - Risk Score: {risk_score}/10 ({risk_level} risk)
                    - Exercise: {exercise}
                    - Diet: {diet}
                    - Sleep: {sleep}
                    - Stress: {stress}
                    - Smoking: {smoking}
                    
                    Provide 3 specific, actionable health recommendations. Keep under 250 words."""
                    
                    advice = get_ai_response(prompt)
                    st.info(f"🤖 **AI Health Recommendations:**\n\n{advice}")

elif page == "❤️ Heart Health":
    st.header("❤️ Heart Health Assessment")
    
    with st.form("heart_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", 20, 100, 45)
            chest_pain = st.selectbox("Chest Pain/Discomfort", ["Never", "Rarely", "Sometimes", "Often"])
            shortness_breath = st.selectbox("Shortness of Breath", ["Never", "With heavy exercise", "With light exercise", "At rest"])
            fatigue = st.selectbox("Unusual Fatigue", ["Never", "Rarely", "Sometimes", "Often"])
        
        with col2:
            heart_rate = st.number_input("Resting Heart Rate (bpm)", 40, 120, 70)
            blood_pressure = st.selectbox("Blood Pressure", ["Normal (<120/80)", "Elevated (120-129/<80)", "High Stage 1 (130-139/80-89)", "High Stage 2 (≥140/≥90)"])
            family_heart_disease = st.checkbox("Family History of Heart Disease")
            exercise_tolerance = st.selectbox("Exercise Tolerance", ["Excellent", "Good", "Fair", "Poor"])
        
        submitted = st.form_submit_button("💓 Assess Heart Health", use_container_width=True)
        
        if submitted:
            # Heart health scoring
            heart_score = 0
            
            # Age factor
            if age > 65: heart_score += 2
            elif age > 45: heart_score += 1
            
            # Symptoms
            symptom_scores = {"Often": 3, "Sometimes": 2, "Rarely": 1, "Never": 0}
            heart_score += symptom_scores.get(chest_pain, 0)
            heart_score += {"At rest": 3, "With light exercise": 2, "With heavy exercise": 1, "Never": 0}[shortness_breath]
            heart_score += symptom_scores.get(fatigue, 0)
            
            # Vitals
            if heart_rate > 100: heart_score += 2
            elif heart_rate < 50: heart_score += 1
            
            bp_scores = {"High Stage 2 (≥140/≥90)": 3, "High Stage 1 (130-139/80-89)": 2, "Elevated (120-129/<80)": 1, "Normal (<120/80)": 0}
            heart_score += bp_scores[blood_pressure]
            
            # Other factors
            if family_heart_disease: heart_score += 1
            if exercise_tolerance == "Poor": heart_score += 2
            elif exercise_tolerance == "Fair": heart_score += 1
            
            heart_score = min(heart_score, 10)
            risk_level, status_type, icon = get_risk_level(heart_score)
            
            # Results
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Heart Score", f"{heart_score}/10")
            with col2:
                st.metric("Risk Level", risk_level)
            with col3:
                st.metric("Heart Rate", f"{heart_rate} bpm")
            
            # Status
            if status_type == "success":
                st.success(f"💚 **Good Heart Health** - {icon} Keep up the great work!")
            elif status_type == "warning":
                st.warning(f"💛 **Monitor Closely** - {icon} Some areas need attention")
            else:
                st.error(f"❤️ **Consult Physician** - {icon} Professional evaluation recommended")
            
            # AI Advice
            if api_key:
                with st.spinner("🤖 Getting heart health insights..."):
                    prompt = f"""Heart Health Assessment:
                    - Age: {age}, Heart Rate: {heart_rate} bpm
                    - Blood Pressure: {blood_pressure}
                    - Symptoms: Chest pain {chest_pain}, Breathing difficulty {shortness_breath}
                    - Exercise tolerance: {exercise_tolerance}
                    - Risk Level: {risk_level} (score: {heart_score}/10)
                    
                    Provide heart-specific health advice and when to see a doctor. Keep under 250 words."""
                    
                    advice = get_ai_response(prompt)
                    st.info(f"🤖 **Heart Health Guidance:**\n\n{advice}")

elif page == "🎯 Health Tips":
    st.header("🎯 Personalized Health Tips")
    
    if not api_key:
        st.warning("🔑 API key needed for personalized recommendations")
        st.stop()
    
    with st.form("tips_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age_group = st.selectbox("Age Group", ["18-30", "31-45", "46-60", "60+"])
            primary_goal = st.selectbox("Primary Health Goal", [
                "Weight Loss", "Muscle Gain", "Better Sleep", "More Energy", 
                "Stress Management", "Heart Health", "General Wellness"
            ])
            activity_level = st.selectbox("Current Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
        
        with col2:
            time_commitment = st.selectbox("Available Time/Day", ["15-30 min", "30-60 min", "1-2 hours", "2+ hours"])
            health_concerns = st.multiselect("Health Concerns", [
                "High Blood Pressure", "High Cholesterol", "Diabetes", "Joint Pain", 
                "Anxiety/Stress", "Sleep Issues", "Digestive Issues", "None"
            ])
            dietary_preferences = st.selectbox("Dietary Preferences", ["No restrictions", "Vegetarian", "Vegan", "Low-carb", "Mediterranean"])
        
        submitted = st.form_submit_button("🎯 Get Personalized Plan", use_container_width=True)
        
        if submitted:
            with st.spinner("🤖 Creating your personalized health plan..."):
                concerns_text = ", ".join(health_concerns) if health_concerns else "None"
                
                prompt = f"""Create a personalized health plan for:
                - Age group: {age_group}
                - Goal: {primary_goal}
                - Activity level: {activity_level}
                - Time available: {time_commitment}
                - Health concerns: {concerns_text}
                - Diet preference: {dietary_preferences}
                
                Provide:
                1. 3 specific daily habits
                2. Weekly exercise plan
                3. Nutrition guidelines
                4. One key tip for their main goal
                
                Keep practical and actionable. Under 300 words."""
                
                tips = get_ai_response(prompt, max_tokens=400)
                
                st.success("🎯 **Your Personalized Health Plan**")
                st.write(tips)
                
                # Quick tips sidebar
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info("💧 **Daily Water**\n8-10 glasses minimum")
                with col2:
                    st.info("😴 **Quality Sleep**\n7-9 hours nightly")
                with col3:
                    st.info("🚶 **Movement**\nBreak every 30-60 min")

elif page == "📊 BMI Calculator":
    st.header("📊 BMI & Body Composition")
    
    with st.form("bmi_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            weight = st.number_input("Weight (kg)", 30.0, 300.0, 70.0, step=0.1)
            height = st.number_input("Height (cm)", 100.0, 250.0, 170.0, step=0.1)
            age = st.number_input("Age", 15, 100, 30)
        
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female"])
            activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
            goal = st.selectbox("Goal", ["Maintain", "Lose Weight", "Gain Weight", "Build Muscle"])
        
        submitted = st.form_submit_button("📊 Calculate BMI & Recommendations", use_container_width=True)
        
        if submitted:
            # BMI Calculation
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            
            # BMI Categories
            if bmi < 18.5:
                category, color, icon = "Underweight", "info", "📉"
            elif bmi < 25:
                category, color, icon = "Normal", "success", "✅"
            elif bmi < 30:
                category, color, icon = "Overweight", "warning", "⚠️"
            else:
                category, color, icon = "Obese", "error", "🚨"
            
            # Calorie estimation
            if gender == "Male":
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            
            activity_multipliers = {"Sedentary": 1.2, "Light": 1.375, "Moderate": 1.55, "Active": 1.725, "Very Active": 1.9}
            daily_calories = int(bmr * activity_multipliers[activity])
            
            # Results
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("BMI", f"{bmi:.1f}")
            with col2:
                st.metric("Category", category)
            with col3:
                st.metric("Daily Calories", f"{daily_calories}")
            with col4:
                st.metric("Goal", goal)
            
            # Status message
            if color == "success":
                st.success(f"{icon} **{category}** - Healthy BMI range!")
            elif color == "warning":
                st.warning(f"{icon} **{category}** - Consider lifestyle adjustments")
            elif color == "error":
                st.error(f"{icon} **{category}** - Consult healthcare provider")
            else:
                st.info(f"{icon} **{category}** - Focus on healthy weight gain")
            
            # AI Recommendations
            if api_key:
                with st.spinner("🤖 Getting personalized recommendations..."):
                    prompt = f"""BMI Analysis Results:
                    - BMI: {bmi:.1f} ({category})
                    - Weight: {weight}kg, Height: {height}cm
                    - Age: {age}, Gender: {gender}
                    - Activity: {activity}
                    - Goal: {goal}
                    - Daily calorie needs: {daily_calories}
                    
                    Provide specific recommendations for their goal and BMI category. Include diet and exercise suggestions. Under 250 words."""
                    
                    advice = get_ai_response(prompt)
                    st.info(f"🤖 **Personalized Recommendations:**\n\n{advice}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>⚠️ <strong>Disclaimer:</strong> For educational purposes only. Not medical advice.</p>
    <p>Always consult healthcare professionals for medical concerns.</p>
    <p>🤖 Powered by Meta Llama 4 Maverick via OpenRouter | © 2025 AI Health Copilot</p>
</div>
""", unsafe_allow_html=True)
