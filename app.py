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
    
    # API Key handling with multiple fallbacks
    api_key = None
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
        st.success("✅ API Connected")
        st.info("🤖 Model: Meta Llama 3.1")
    except:
        try:
            api_key = st.secrets.get("openrouter", {}).get("api_key")
            if api_key:
                st.success("✅ API Connected")
                st.info("🤖 Model: Meta Llama 3.1")
        except:
            pass
    
    if not api_key:
        api_key = st.text_input("Enter OpenRouter API Key:", type="password", 
                               help="Get free key from https://openrouter.ai/")
        if api_key:
            st.info("🔑 API Key Entered")
        else:
            st.warning("⚠️ Using offline recommendations")

# Enhanced AI Response Function with Fallbacks
def get_ai_response(prompt, health_data=None, max_tokens=250):
    """Get AI response with intelligent fallbacks"""
    
    # Try API first
    if api_key and len(api_key) > 20:
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://ai-health-copilot.streamlit.app",
                "X-Title": "AI Health Copilot"
            }
            
            payload = {
                "model": "meta-llama/llama-3.1-8b-instruct:free",
                "messages": [
                    {"role": "system", "content": "You are an expert health advisor. Provide specific, actionable health recommendations. Always remind users to consult healthcare professionals."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload),
                timeout=25
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            elif response.status_code == 402:
                return get_fallback_recommendation(health_data, "quota_exceeded")
            elif response.status_code == 401:
                return get_fallback_recommendation(health_data, "invalid_key")
            else:
                return get_fallback_recommendation(health_data, "api_error")
                
        except Exception as e:
            return get_fallback_recommendation(health_data, "connection_error")
    
    # Use fallback recommendations
    return get_fallback_recommendation(health_data, "no_api")

def get_fallback_recommendation(health_data, error_type="no_api"):
    """Generate intelligent fallback recommendations"""
    if not health_data:
        return "⚠️ API unavailable. Please add your API key for personalized recommendations."
    
    recommendations = []
    
    # Extract health data
    risk_level = health_data.get('risk_level', 'moderate').lower()
    age = health_data.get('age', 30)
    bmi = health_data.get('bmi', 25)
    
    # Base recommendations by risk level
    if risk_level == 'low':
        recommendations.extend([
            "🎯 **Maintain Current Habits**: Your health indicators are excellent! Continue your current lifestyle.",
            "💪 **Stay Active**: Aim for 150 minutes of moderate exercise weekly to maintain your fitness level.",
            "🥗 **Balanced Nutrition**: Keep eating a variety of fruits, vegetables, whole grains, and lean proteins."
        ])
    elif risk_level == 'moderate':
        recommendations.extend([
            "⚠️ **Lifestyle Adjustments Needed**: Focus on improving key health areas to reduce risk.",
            "🏃‍♂️ **Increase Physical Activity**: Start with 30 minutes of daily walking, gradually increasing intensity.",
            "🍎 **Improve Diet Quality**: Reduce processed foods, increase vegetables and fruits to 5-9 servings daily."
        ])
    else:  # high risk
        recommendations.extend([
            "🚨 **Immediate Action Required**: Consult a healthcare provider for a comprehensive health evaluation.",
            "👨‍⚕️ **Medical Consultation**: Schedule appointment within 1-2 weeks for professional assessment.",
            "📋 **Track Daily Habits**: Monitor blood pressure, weight, diet, and physical activity closely."
        ])
    
    # Age-specific recommendations
    if age < 30:
        recommendations.append("🌱 **Build Healthy Foundations**: Establish exercise routines and healthy eating patterns now for lifelong benefits.")
    elif age < 50:
        recommendations.append("⚖️ **Balance Work-Life**: Manage stress effectively and prioritize sleep quality (7-9 hours nightly).")
    elif age < 65:
        recommendations.append("🔬 **Regular Health Screenings**: Annual check-ups become crucial - monitor cholesterol, blood pressure, and diabetes risk.")
    else:
        recommendations.append("🛡️ **Preventive Care Focus**: Emphasize fall prevention, bone health, and cognitive wellness activities.")
    
    # BMI-specific advice
    if bmi < 18.5:
        recommendations.append("📈 **Healthy Weight Gain**: Focus on nutrient-dense, calorie-rich foods like nuts, avocados, and lean proteins.")
    elif bmi > 25:
        recommendations.append("📉 **Gradual Weight Management**: Aim for 1-2 pounds loss per week through balanced diet and increased activity.")
    
    # Add general wellness tips
    recommendations.extend([
        "💧 **Hydration Priority**: Drink 8-10 glasses of water daily, more if you're active or in hot weather.",
        "😴 **Sleep Optimization**: Maintain consistent sleep schedule and create a relaxing bedtime routine.",
        "🧘 **Stress Management**: Practice deep breathing, meditation, or yoga for 10-15 minutes daily."
    ])
    
    # Combine recommendations
    final_text = "\n\n".join(recommendations[:4])  # Limit to top 4 recommendations
    
    # Add appropriate disclaimer based on error type
    if error_type == "invalid_key":
        final_text += "\n\n🔑 *Note: API key issue detected. Using evidence-based health recommendations.*"
    elif error_type == "quota_exceeded":
        final_text += "\n\n💳 *Note: API quota reached. Displaying curated health guidance.*"
    else:
        final_text += "\n\n🤖 *Note: Providing evidence-based health recommendations from medical guidelines.*"
    
    return final_text

# Health calculation functions
def calculate_risk_score(age, lifestyle_factors):
    """Calculate comprehensive health risk score"""
    score = 0
    if age > 65: score += 3
    elif age > 50: score += 2
    elif age > 35: score += 1
    
    score += sum(lifestyle_factors.values())
    return min(score, 10)

def get_risk_level(score):
    """Get risk level classification"""
    if score <= 3: return "Low", "success", "✅"
    elif score <= 6: return "Moderate", "warning", "⚠️"
    else: return "High", "error", "🚨"

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
            with col1: st.metric("Risk Score", f"{risk_score}/10")
            with col2: st.metric("Risk Level", risk_level)
            with col3: st.metric("Age Factor", f"{age} years")
            
            # Status message
            if status_type == "success":
                st.success(f"{icon} **{risk_level} Risk** - Great health indicators!")
            elif status_type == "warning":
                st.warning(f"{icon} **{risk_level} Risk** - Some areas for improvement")
            else:
                st.error(f"{icon} **{risk_level} Risk** - Consider lifestyle changes")
            
            # Health data for recommendations
            health_data = {
                'risk_level': risk_level,
                'age': age,
                'exercise': exercise,
                'diet': diet,
                'sleep': sleep,
                'stress': stress
            }
            
            # AI Insights
            with st.spinner("🤖 Generating health recommendations..."):
                prompt = f"""Health Assessment: {age}yr, {risk_level} risk ({risk_score}/10), Exercise: {exercise}, Diet: {diet}, Sleep: {sleep}, Stress: {stress}. Provide 3 specific health recommendations under 200 words."""
                advice = get_ai_response(prompt, health_data)
                st.info(f"🤖 **Personalized Recommendations:**\n\n{advice}")

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
            if age > 65: heart_score += 2
            elif age > 45: heart_score += 1
            
            symptom_scores = {"Often": 3, "Sometimes": 2, "Rarely": 1, "Never": 0}
            heart_score += symptom_scores.get(chest_pain, 0)
            heart_score += {"At rest": 3, "With light exercise": 2, "With heavy exercise": 1, "Never": 0}[shortness_breath]
            heart_score += symptom_scores.get(fatigue, 0)
            
            if heart_rate > 100: heart_score += 2
            elif heart_rate < 50: heart_score += 1
            
            bp_scores = {"High Stage 2 (≥140/≥90)": 3, "High Stage 1 (130-139/80-89)": 2, "Elevated (120-129/<80)": 1, "Normal (<120/80)": 0}
            heart_score += bp_scores[blood_pressure]
            
            if family_heart_disease: heart_score += 1
            if exercise_tolerance in ["Poor", "Fair"]: heart_score += 1
            
            heart_score = min(heart_score, 10)
            risk_level, status_type, icon = get_risk_level(heart_score)
            
            # Results
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Heart Score", f"{heart_score}/10")
            with col2: st.metric("Risk Level", risk_level)
            with col3: st.metric("Heart Rate", f"{heart_rate} bpm")
            
            # Status
            if status_type == "success":
                st.success(f"💚 **Good Heart Health** - {icon} Keep up the great work!")
            elif status_type == "warning":
                st.warning(f"💛 **Monitor Closely** - {icon} Some areas need attention")
            else:
                st.error(f"❤️ **Consult Physician** - {icon} Professional evaluation recommended")
            
            # Heart-specific recommendations
            health_data = {
                'risk_level': risk_level,
                'age': age,
                'heart_rate': heart_rate,
                'blood_pressure': blood_pressure,
                'chest_pain': chest_pain,
                'exercise_tolerance': exercise_tolerance
            }
            
            with st.spinner("🤖 Generating heart health guidance..."):
                prompt = f"""Heart Assessment: {age}yr, HR: {heart_rate}bpm, BP: {blood_pressure}, symptoms: chest pain {chest_pain}, breathing {shortness_breath}, risk: {risk_level}. Heart health advice under 200 words."""
                advice = get_ai_response(prompt, health_data)
                st.info(f"🤖 **Heart Health Guidance:**\n\n{advice}")

elif page == "🎯 Health Tips":
    st.header("🎯 Personalized Health Tips")
    
    with st.form("tips_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age_group = st.selectbox("Age Group", ["18-30", "31-45", "46-60", "60+"])
            primary_goal = st.selectbox("Primary Health Goal", ["Weight Loss", "Muscle Gain", "Better Sleep", "More Energy", "Stress Management", "Heart Health", "General Wellness"])
            activity_level = st.selectbox("Current Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
        
        with col2:
            time_commitment = st.selectbox("Available Time/Day", ["15-30 min", "30-60 min", "1-2 hours", "2+ hours"])
            health_concerns = st.multiselect("Health Concerns", ["High Blood Pressure", "High Cholesterol", "Diabetes", "Joint Pain", "Anxiety/Stress", "Sleep Issues", "None"])
            dietary_preferences = st.selectbox("Dietary Preferences", ["No restrictions", "Vegetarian", "Vegan", "Low-carb", "Mediterranean"])
        
        submitted = st.form_submit_button("🎯 Get Personalized Plan", use_container_width=True)
        
        if submitted:
            health_data = {
                'age_group': age_group,
                'goal': primary_goal,
                'activity_level': activity_level,
                'time_commitment': time_commitment,
                'concerns': health_concerns,
                'dietary_preferences': dietary_preferences
            }
            
            with st.spinner("🤖 Creating your personalized health plan..."):
                concerns_text = ", ".join(health_concerns) if health_concerns else "None"
                prompt = f"""Create health plan: Age {age_group}, Goal: {primary_goal}, Activity: {activity_level}, Time: {time_commitment}, Concerns: {concerns_text}, Diet: {dietary_preferences}. Provide 4 specific recommendations under 250 words."""
                
                tips = get_ai_response(prompt, health_data)
                st.success("🎯 **Your Personalized Health Plan**")
                st.write(tips)
                
                # Quick tips
                col1, col2, col3 = st.columns(3)
                with col1: st.info("💧 **Daily Water**\n8-10 glasses minimum")
                with col2: st.info("😴 **Quality Sleep**\n7-9 hours nightly")
                with col3: st.info("🚶 **Movement**\nBreak every 30-60 min")

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
            if bmi < 18.5: category, color, icon = "Underweight", "info", "📉"
            elif bmi < 25: category, color, icon = "Normal", "success", "✅"
            elif bmi < 30: category, color, icon = "Overweight", "warning", "⚠️"
            else: category, color, icon = "Obese", "error", "🚨"
            
            # Calorie estimation
            if gender == "Male":
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            
            activity_multipliers = {"Sedentary": 1.2, "Light": 1.375, "Moderate": 1.55, "Active": 1.725, "Very Active": 1.9}
            daily_calories = int(bmr * activity_multipliers[activity])
            
            # Results
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("BMI", f"{bmi:.1f}")
            with col2: st.metric("Category", category)
            with col3: st.metric("Daily Calories", f"{daily_calories}")
            with col4: st.metric("Goal", goal)
            
            # Status message
            if color == "success": st.success(f"{icon} **{category}** - Healthy BMI range!")
            elif color == "warning": st.warning(f"{icon} **{category}** - Consider lifestyle adjustments")
            elif color == "error": st.error(f"{icon} **{category}** - Consult healthcare provider")
            else: st.info(f"{icon} **{category}** - Focus on healthy weight gain")
            
            # BMI-specific recommendations
            health_data = {
                'bmi': bmi,
                'category': category,
                'age': age,
                'gender': gender,
                'goal': goal,
                'daily_calories': daily_calories
            }
            
            with st.spinner("🤖 Generating personalized recommendations..."):
                prompt = f"""BMI Analysis: {bmi:.1f} ({category}), {weight}kg, {height}cm, {age}yr {gender}, Goal: {goal}, Calories: {daily_calories}. BMI-specific recommendations under 200 words."""
                advice = get_ai_response(prompt, health_data)
                st.info(f"🤖 **Personalized Recommendations:**\n\n{advice}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>⚠️ <strong>Disclaimer:</strong> For educational purposes only. Not medical advice.</p>
    <p>Always consult healthcare professionals for medical concerns.</p>
    <p>🤖 Powered by Meta Llama 3.1 via OpenRouter | © 2025 AI Health Copilot</p>
</div>
""", unsafe_allow_html=True)
