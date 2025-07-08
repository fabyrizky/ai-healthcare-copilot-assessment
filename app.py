import streamlit as st
import requests

# Page config
st.set_page_config(page_title="AI Health Copilot", page_icon="🧑‍⚕️", layout="wide")

# Title
st.title("🧑‍⚕️ AI Health Copilot")
st.markdown("**Smart Health Assessment with AI-Powered Insights**")

# Sidebar
st.sidebar.title("🔧 Configuration")

# Get API key
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    st.sidebar.success("✅ API Connected")
    st.sidebar.info("🤖 Model: Qwen QwQ 32B")
except:
    api_key = None
    st.sidebar.error("❌ API Key Missing")
    st.sidebar.code('OPENROUTER_API_KEY = "sk-or-v1-your-key"')

# AI function
def get_ai_response(prompt):
    if not api_key:
        return "⚠️ API key not configured"
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "qwen/qwq-32b-preview",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 400
            },
            timeout=20
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"❌ API Error: {response.status_code}"
    except:
        return "❌ Connection failed"

# Simple health functions
def health_risk_calculator(age, lifestyle_score):
    risk = 0
    if age > 50: risk += 2
    if age > 65: risk += 1
    risk += lifestyle_score
    return min(risk, 10)

# Navigation
page = st.sidebar.selectbox(
    "Choose Assessment",
    ["🩺 Health Risk", "❤️ Heart Check", "🎯 Health Tips"]
)

# Main content
if page == "🩺 Health Risk":
    st.header("🩺 General Health Risk Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", 18, 100, 35)
        exercise = st.selectbox("Exercise", ["Daily", "Weekly", "Rarely", "Never"])
        diet = st.selectbox("Diet Quality", ["Excellent", "Good", "Fair", "Poor"])
        sleep = st.selectbox("Sleep Quality", ["Excellent", "Good", "Fair", "Poor"])
    
    with col2:
        stress = st.selectbox("Stress Level", ["Low", "Moderate", "High", "Very High"])
        smoking = st.selectbox("Smoking", ["Never", "Former", "Current"])
        weight_status = st.selectbox("Weight", ["Underweight", "Normal", "Overweight", "Obese"])
        family_history = st.selectbox("Family History", ["No diseases", "Some diseases", "Multiple diseases"])
    
    if st.button("🔍 Calculate Health Risk"):
        # Simple scoring
        lifestyle_score = 0
        if exercise in ["Rarely", "Never"]: lifestyle_score += 2
        if diet in ["Fair", "Poor"]: lifestyle_score += 1
        if sleep in ["Fair", "Poor"]: lifestyle_score += 1
        if stress in ["High", "Very High"]: lifestyle_score += 1
        if smoking == "Current": lifestyle_score += 3
        if weight_status in ["Overweight", "Obese"]: lifestyle_score += 2
        if family_history != "No diseases": lifestyle_score += 1
        
        risk_score = health_risk_calculator(age, lifestyle_score)
        
        # Display result
        if risk_score <= 3:
            st.success("✅ **Low Risk** - Great health indicators!")
            risk_level = "Low"
        elif risk_score <= 6:
            st.warning("⚠️ **Moderate Risk** - Some areas for improvement")
            risk_level = "Moderate"
        else:
            st.error("🚨 **High Risk** - Consider lifestyle changes")
            risk_level = "High"
        
        # Show score
        st.metric("Risk Score", f"{risk_score}/10")
        
        # AI explanation
        if api_key:
            with st.spinner("Getting AI insights..."):
                prompt = f"Health assessment: {age} years old, {risk_level} risk (score {risk_score}/10). Exercise: {exercise}, Diet: {diet}, Stress: {stress}. Give brief health advice (under 200 words)."
                advice = get_ai_response(prompt)
                st.info(f"🤖 **AI Health Advice:**\n\n{advice}")

elif page == "❤️ Heart Check":
    st.header("❤️ Heart Health Quick Check")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", 20, 100, 40)
        bp = st.selectbox("Blood Pressure", ["Normal", "Elevated", "High", "Very High"])
        cholesterol = st.selectbox("Cholesterol", ["Normal", "Borderline", "High", "Very High"])
    
    with col2:
        chest_pain = st.selectbox("Chest Pain", ["Never", "Rarely", "Sometimes", "Often"])
        shortness_breath = st.selectbox("Shortness of Breath", ["Never", "Rarely", "Sometimes", "Often"])
        family_heart = st.selectbox("Family Heart Disease", ["No", "Yes"])
    
    if st.button("💓 Check Heart Health"):
        heart_score = 0
        if age > 65: heart_score += 2
        elif age > 50: heart_score += 1
        if bp in ["High", "Very High"]: heart_score += 2
        if cholesterol in ["High", "Very High"]: heart_score += 2
        if chest_pain in ["Sometimes", "Often"]: heart_score += 2
        if shortness_breath in ["Sometimes", "Often"]: heart_score += 2
        if family_heart == "Yes": heart_score += 1
        
        if heart_score <= 2:
            st.success("💚 **Good Heart Health** - Keep it up!")
            status = "Good"
        elif heart_score <= 5:
            st.warning("💛 **Moderate Concern** - Monitor closely")
            status = "Moderate"
        else:
            st.error("❤️ **Needs Attention** - Consult doctor")
            status = "High Risk"
        
        st.metric("Heart Risk Score", f"{heart_score}/10")
        
        if api_key:
            with st.spinner("Getting heart health advice..."):
                prompt = f"Heart health assessment: {age} years old, {status} status. BP: {bp}, Cholesterol: {cholesterol}, Symptoms: chest pain {chest_pain}, breathing {shortness_breath}. Give heart health advice (under 200 words)."
                advice = get_ai_response(prompt)
                st.info(f"🤖 **Heart Health Advice:**\n\n{advice}")

elif page == "🎯 Health Tips":
    st.header("🎯 Personalized Health Tips")
    
    if not api_key:
        st.error("🔑 API key needed for personalized tips")
        st.stop()
    
    col1, col2 = st.columns(2)
    
    with col1:
        age_group = st.selectbox("Age Group", ["18-30", "31-50", "51-65", "65+"])
        goal = st.selectbox("Health Goal", [
            "Lose Weight", "Gain Muscle", "Better Sleep", 
            "More Energy", "Stress Relief", "General Health"
        ])
    
    with col2:
        lifestyle = st.selectbox("Lifestyle", ["Very Active", "Active", "Moderate", "Sedentary"])
        time_available = st.selectbox("Time Available", ["< 30 min", "30-60 min", "1-2 hours", "> 2 hours"])
    
    if st.button("🎯 Get Personalized Tips"):
        with st.spinner("Creating your personalized health plan..."):
            prompt = f"""Create personalized health tips for:
            - Age: {age_group}
            - Goal: {goal}
            - Lifestyle: {lifestyle}
            - Time available: {time_available}
            
            Provide:
            1. 3 specific daily tips
            2. 1 weekly goal
            3. Simple meal suggestions
            4. Quick exercise ideas
            
            Keep practical and under 300 words."""
            
            tips = get_ai_response(prompt)
            
            st.success("🎯 **Your Personalized Health Plan:**")
            st.write(tips)
            
            # Additional quick tips
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("💧 **Hydration**\nDrink 8-10 glasses of water daily")
            with col2:
                st.info("😴 **Sleep**\nAim for 7-9 hours nightly")
            with col3:
                st.info("🚶 **Movement**\nTake breaks every hour")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>⚠️ <strong>Disclaimer:</strong> For educational purposes only. Not medical advice.</p>
    <p>🤖 Powered by Qwen QwQ 32B via OpenRouter | © 2025 AI Health Copilot</p>
</div>
""", unsafe_allow_html=True)
