import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="AI Health Copilot", 
    page_icon="🧑‍⚕️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .prediction-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .sidebar .stSelectbox {
        background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 10px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
    }
    .health-tip {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #48bb78;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🧑‍⚕️ AI Health Copilot</h1>
    <p>Advanced Health Prediction & Analysis with Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### 🔧 Configuration")
    
    # Enhanced API Key handling
    api_key = None
    api_status = "❌ No API Key"
    
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
        if api_key and len(api_key) > 20:
            api_status = "✅ API Connected"
            model_name = "Meta Llama 3.1"
        else:
            api_status = "⚠️ Invalid API Key"
    except:
        pass
    
    if not api_key or len(api_key) < 20:
        api_key = st.text_input("🔑 OpenRouter API Key:", type="password", 
                               help="Get free key from https://openrouter.ai/")
        if api_key and len(api_key) > 20:
            api_status = "✅ API Connected"
            model_name = "Meta Llama 3.1"
    
    st.success(api_status) if "✅" in api_status else st.error(api_status) if "❌" in api_status else st.warning(api_status)
    
    if "✅" in api_status:
        st.info(f"🤖 Model: {model_name}")

# ML Models Cache
@st.cache_data
def load_health_datasets():
    """Load and prepare health datasets"""
    try:
        # Diabetes Dataset
        diabetes_data = pd.read_csv('diabetes.csv')
        diabetes_X = diabetes_data.drop('Outcome', axis=1)
        diabetes_y = diabetes_data['Outcome']
        
        # Heart Disease Dataset  
        heart_data = pd.read_csv('heart.csv')
        heart_X = heart_data.drop('target', axis=1)
        heart_y = heart_data['target']
        
        # Parkinson's Dataset
        parkinsons_data = pd.read_csv('parkinsons.csv')
        parkinsons_X = parkinsons_data.drop(['name', 'status'], axis=1)
        parkinsons_y = parkinsons_data['status']
        
        return {
            'diabetes': (diabetes_X, diabetes_y),
            'heart': (heart_X, heart_y),
            'parkinsons': (parkinsons_X, parkinsons_y)
        }
    except:
        return None

@st.cache_resource
def train_ml_models():
    """Train ML models for health predictions"""
    data = load_health_datasets()
    if not data:
        return None
    
    models = {}
    
    # Diabetes Model
    X_diabetes, y_diabetes = data['diabetes']
    diabetes_model = RandomForestClassifier(n_estimators=100, random_state=42)
    diabetes_model.fit(X_diabetes, y_diabetes)
    models['diabetes'] = (diabetes_model, X_diabetes.columns.tolist())
    
    # Heart Disease Model
    X_heart, y_heart = data['heart']
    heart_model = LogisticRegression(random_state=42, max_iter=1000)
    heart_model.fit(X_heart, y_heart)
    models['heart'] = (heart_model, X_heart.columns.tolist())
    
    # Parkinson's Model
    X_parkinsons, y_parkinsons = data['parkinsons']
    scaler = StandardScaler()
    X_parkinsons_scaled = scaler.fit_transform(X_parkinsons)
    parkinsons_model = SVC(probability=True, random_state=42)
    parkinsons_model.fit(X_parkinsons_scaled, y_parkinsons)
    models['parkinsons'] = (parkinsons_model, X_parkinsons.columns.tolist(), scaler)
    
    return models

# Enhanced AI Response Function
def get_ai_response(prompt, health_data=None, max_tokens=300):
    """Enhanced AI response with smart fallbacks"""
    
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
                    {"role": "system", "content": "You are an expert health advisor. Provide specific, actionable health recommendations based on medical data. Always remind users to consult healthcare professionals for serious concerns."},
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
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
                
        except Exception as e:
            pass
    
    # Smart Fallback Recommendations
    return generate_smart_fallback(health_data)

def generate_smart_fallback(health_data):
    """Generate intelligent health recommendations"""
    if not health_data:
        return "🤖 **Health Insights:** Enable API for personalized AI recommendations, or continue with evidence-based guidance below."
    
    recommendations = []
    risk_level = health_data.get('risk_level', 'moderate').lower()
    
    if risk_level == 'low':
        recommendations = [
            "🎯 **Maintain Excellence:** Your health indicators are outstanding! Continue your current healthy lifestyle patterns.",
            "💪 **Optimize Performance:** Add strength training 2-3x weekly and maintain 150+ minutes moderate cardio.",
            "🧠 **Mental Wellness:** Practice mindfulness 10-15 minutes daily to maintain emotional balance.",
            "📊 **Track Progress:** Monitor key metrics monthly to maintain your excellent health trajectory."
        ]
    elif risk_level == 'moderate':
        recommendations = [
            "⚡ **Priority Actions:** Focus on improving diet quality and increasing physical activity immediately.",
            "🥗 **Nutrition Upgrade:** Increase vegetables to 5-7 servings daily, reduce processed foods by 50%.",
            "🏃‍♂️ **Movement Goal:** Start with 30-minute daily walks, progress to varied exercise routine.",
            "😴 **Sleep Optimization:** Establish consistent 7-9 hour sleep schedule with proper sleep hygiene."
        ]
    else:  # high risk
        recommendations = [
            "🚨 **Immediate Action:** Schedule healthcare consultation within 1-2 weeks for comprehensive evaluation.",
            "📋 **Daily Monitoring:** Track blood pressure, weight, and symptoms daily using health apps.",
            "💊 **Medication Adherence:** Follow prescribed treatments exactly and discuss concerns with doctor.",
            "🆘 **Emergency Plan:** Know warning signs and when to seek immediate medical attention."
        ]
    
    return "\n\n".join(recommendations[:3]) + "\n\n🤖 *Evidence-based recommendations from medical guidelines.*"

# Navigation
page = st.sidebar.selectbox(
    "🏥 Choose Health Assessment",
    ["🩺 General Health", "❤️ Heart Disease Risk", "🧬 Diabetes Prediction", "🧠 Parkinson's Screening", "💡 Smart Health Tips"]
)

# Load ML Models
models = train_ml_models()

if page == "🩺 General Health":
    st.markdown("### 🩺 Comprehensive Health Risk Assessment")
    
    with st.form("health_assessment"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🧑‍🤝‍🧑 Personal Information**")
            age = st.number_input("Age", 18, 100, 35)
            gender = st.selectbox("Gender", ["Male", "Female"])
            height = st.number_input("Height (cm)", 140, 220, 170)
            weight = st.number_input("Weight (kg)", 40, 200, 70)
            
        with col2:
            st.markdown("**🏃‍♂️ Lifestyle Factors**")
            exercise = st.selectbox("Exercise Frequency", ["Daily", "4-6x/week", "2-3x/week", "1x/week", "Never"])
            diet = st.selectbox("Diet Quality", ["Excellent", "Good", "Fair", "Poor"])
            sleep = st.selectbox("Sleep Hours/Night", ["8-9", "7-8", "6-7", "5-6", "<5"])
            stress = st.selectbox("Stress Level", ["Low", "Moderate", "High", "Very High"])
        
        col3, col4 = st.columns(2)
        with col3:
            smoking = st.selectbox("Smoking Status", ["Never", "Former (>2yr)", "Former (<2yr)", "Current"])
            alcohol = st.selectbox("Alcohol", ["None", "Light", "Moderate", "Heavy"])
            
        with col4:
            family_history = st.multiselect("Family History", ["Diabetes", "Heart Disease", "Cancer", "Hypertension"])
            symptoms = st.multiselect("Current Symptoms", ["Fatigue", "Chest Pain", "Shortness of Breath", "Headaches", "None"])
        
        submitted = st.form_submit_button("🔍 Analyze Health Status", use_container_width=True)
        
        if submitted:
            # Calculate BMI
            bmi = weight / ((height/100) ** 2)
            
            # Risk Scoring Algorithm
            risk_score = 0
            
            # Age factor
            if age > 65: risk_score += 3
            elif age > 50: risk_score += 2
            elif age > 35: risk_score += 1
            
            # BMI factor
            if bmi < 18.5 or bmi > 30: risk_score += 2
            elif bmi > 25: risk_score += 1
            
            # Lifestyle factors
            exercise_scores = {"Never": 3, "1x/week": 2, "2-3x/week": 1, "4-6x/week": 0, "Daily": 0}
            risk_score += exercise_scores[exercise]
            
            diet_scores = {"Poor": 2, "Fair": 1, "Good": 0, "Excellent": -1}
            risk_score += diet_scores[diet]
            
            sleep_scores = {"<5": 3, "5-6": 2, "6-7": 1, "7-8": 0, "8-9": 0}
            risk_score += sleep_scores[sleep]
            
            stress_scores = {"Very High": 2, "High": 1, "Moderate": 0, "Low": 0}
            risk_score += stress_scores[stress]
            
            smoking_scores = {"Current": 3, "Former (<2yr)": 2, "Former (>2yr)": 1, "Never": 0}
            risk_score += smoking_scores[smoking]
            
            alcohol_scores = {"Heavy": 2, "Moderate": 1, "Light": 0, "None": 0}
            risk_score += alcohol_scores[alcohol]
            
            # Family history and symptoms
            risk_score += len(family_history)
            risk_score += len([s for s in symptoms if s != "None"])
            
            risk_score = max(0, min(risk_score, 10))
            
            # Risk level classification
            if risk_score <= 3:
                risk_level, color, icon = "Low", "success", "✅"
            elif risk_score <= 6:
                risk_level, color, icon = "Moderate", "warning", "⚠️"
            else:
                risk_level, color, icon = "High", "error", "🚨"
            
            # Display Results
            st.markdown("### 📊 Health Assessment Results")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🎯 Risk Score", f"{risk_score}/10")
            with col2:
                st.metric("📊 BMI", f"{bmi:.1f}")
            with col3:
                st.metric("⚖️ Risk Level", risk_level)
            with col4:
                st.metric("👤 Age Group", f"{age} years")
            
            # Visual Risk Indicator
            if color == "success":
                st.success(f"{icon} **{risk_level} Risk** - Excellent health indicators!")
            elif color == "warning":
                st.warning(f"{icon} **{risk_level} Risk** - Room for improvement")
            else:
                st.error(f"{icon} **{risk_level} Risk** - Consider lifestyle changes")
            
            # Create visualization
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = risk_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Health Risk Score"},
                delta = {'reference': 5},
                gauge = {
                    'axis': {'range': [None, 10]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 3], 'color': "lightgreen"},
                        {'range': [3, 6], 'color': "yellow"},
                        {'range': [6, 10], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 8
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # AI Recommendations
            health_data = {
                'risk_level': risk_level,
                'age': age,
                'bmi': bmi,
                'exercise': exercise,
                'diet': diet,
                'sleep': sleep
            }
            
            with st.spinner("🤖 Generating personalized recommendations..."):
                prompt = f"""Health Assessment Results:
                - Age: {age}, Gender: {gender}, BMI: {bmi:.1f}
                - Risk Level: {risk_level} (Score: {risk_score}/10)
                - Exercise: {exercise}, Diet: {diet}, Sleep: {sleep}
                - Family History: {', '.join(family_history) if family_history else 'None'}
                
                Provide 4 specific, actionable health recommendations."""
                
                advice = get_ai_response(prompt, health_data)
                
                st.markdown("### 🤖 Personalized Health Recommendations")
                st.markdown(f"""
                <div class="prediction-card">
                {advice}
                </div>
                """, unsafe_allow_html=True)

elif page == "❤️ Heart Disease Risk" and models:
    st.markdown("### ❤️ Heart Disease Risk Prediction")
    st.markdown("*Using Machine Learning with Clinical Parameters*")
    
    with st.form("heart_prediction"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Vital Signs**")
            age = st.number_input("Age", 20, 100, 50)
            sex = st.selectbox("Sex", ["Male", "Female"])
            trestbps = st.number_input("Resting Blood Pressure (mmHg)", 80, 200, 120)
            chol = st.number_input("Cholesterol (mg/dL)", 100, 400, 200)
            thalach = st.number_input("Max Heart Rate", 60, 220, 150)
            
        with col2:
            st.markdown("**🩺 Clinical Indicators**")
            cp = st.selectbox("Chest Pain Type", ["Typical Angina", "Atypical Angina", "Non-anginal", "Asymptomatic"])
            fbs = st.selectbox("Fasting Blood Sugar > 120", ["No", "Yes"])
            restecg = st.selectbox("Resting ECG", ["Normal", "ST-T Abnormality", "LV Hypertrophy"])
            exang = st.selectbox("Exercise Induced Angina", ["No", "Yes"])
            oldpeak = st.number_input("ST Depression", 0.0, 6.0, 1.0, 0.1)
        
        col3, col4 = st.columns(2)
        with col3:
            slope = st.selectbox("ST Slope", ["Upsloping", "Flat", "Downsloping"])
            ca = st.selectbox("Major Vessels Colored", [0, 1, 2, 3])
        with col4:
            thal = st.selectbox("Thalassemia", ["Normal", "Fixed Defect", "Reversible Defect"])
        
        submitted = st.form_submit_button("🔬 Predict Heart Disease Risk", use_container_width=True)
        
        if submitted:
            # Prepare input data
            input_data = np.array([[
                age,
                1 if sex == "Male" else 0,
                ["Typical Angina", "Atypical Angina", "Non-anginal", "Asymptomatic"].index(cp),
                trestbps,
                chol,
                1 if fbs == "Yes" else 0,
                ["Normal", "ST-T Abnormality", "LV Hypertrophy"].index(restecg),
                thalach,
                1 if exang == "Yes" else 0,
                oldpeak,
                ["Upsloping", "Flat", "Downsloping"].index(slope),
                ca,
                ["Normal", "Fixed Defect", "Reversible Defect"].index(thal) + 1
            ]])
            
            # Make prediction
            model, features = models['heart']
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0]
            
            # Display results
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🫀 Prediction", "High Risk" if prediction == 1 else "Low Risk")
            with col2:
                st.metric("📊 Risk Probability", f"{probability[1]*100:.1f}%")
            with col3:
                st.metric("🎯 Confidence", f"{max(probability)*100:.1f}%")
            
            # Risk visualization
            if prediction == 1:
                st.error("🚨 **High Risk of Heart Disease Detected**")
                risk_color = "red"
            else:
                st.success("✅ **Low Risk of Heart Disease**")
                risk_color = "green"
            
            # Create probability chart
            fig = px.bar(
                x=['Low Risk', 'High Risk'],
                y=[probability[0]*100, probability[1]*100],
                title="Heart Disease Risk Probability",
                color=['Low Risk', 'High Risk'],
                color_discrete_map={'Low Risk': 'green', 'High Risk': 'red'}
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # AI Analysis
            health_data = {'risk_level': 'high' if prediction == 1 else 'low', 'heart_risk': probability[1]}
            prompt = f"""Heart Disease Risk Analysis:
            - Risk Level: {'High' if prediction == 1 else 'Low'} ({probability[1]*100:.1f}% probability)
            - Age: {age}, Sex: {sex}
            - Blood Pressure: {trestbps}, Cholesterol: {chol}
            - Max Heart Rate: {thalach}
            
            Provide specific heart health recommendations."""
            
            advice = get_ai_response(prompt, health_data)
            st.markdown("### 🩺 Heart Health Recommendations")
            st.markdown(f"""
            <div class="prediction-card">
            {advice}
            </div>
            """, unsafe_allow_html=True)

elif page == "🧬 Diabetes Prediction" and models:
    st.markdown("### 🧬 Diabetes Risk Prediction")
    st.markdown("*Advanced ML Analysis of Metabolic Indicators*")
    
    with st.form("diabetes_prediction"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🤰 Medical History**")
            pregnancies = st.number_input("Pregnancies", 0, 15, 0)
            age = st.number_input("Age", 18, 100, 35)
            bmi = st.number_input("BMI", 15.0, 50.0, 25.0, 0.1)
            dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.5, 0.01)
            
        with col2:
            st.markdown("**🩸 Lab Results**")
            glucose = st.number_input("Glucose Level (mg/dL)", 50, 300, 120)
            bp = st.number_input("Blood Pressure (mmHg)", 40, 200, 80)
            skin = st.number_input("Skin Thickness (mm)", 0, 100, 20)
            insulin = st.number_input("Insulin (μU/mL)", 0, 900, 80)
        
        submitted = st.form_submit_button("🔬 Analyze Diabetes Risk", use_container_width=True)
        
        if submitted:
            # Prepare input
            input_data = np.array([[pregnancies, glucose, bp, skin, insulin, bmi, dpf, age]])
            
            # Make prediction
            model, features = models['diabetes']
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0]
            
            # Results
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🧬 Risk Status", "High Risk" if prediction == 1 else "Low Risk")
            with col2:
                st.metric("📊 Probability", f"{probability[1]*100:.1f}%")
            with col3:
                st.metric("🎯 Confidence", f"{max(probability)*100:.1f}%")
            
            if prediction == 1:
                st.error("🚨 **High Diabetes Risk Detected**")
            else:
                st.success("✅ **Low Diabetes Risk**")
            
            # Feature importance visualization
            feature_importance = dict(zip(features, model.feature_importances_))
            sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
            
            fig = px.bar(
                x=[f[1] for f in sorted_features[:5]],
                y=[f[0] for f in sorted_features[:5]],
                orientation='h',
                title="Top 5 Risk Factors",
                labels={'x': 'Importance', 'y': 'Features'}
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # AI Recommendations
            health_data = {'risk_level': 'high' if prediction == 1 else 'low', 'diabetes_risk': probability[1]}
            prompt = f"""Diabetes Risk Analysis:
            - Risk: {'High' if prediction == 1 else 'Low'} ({probability[1]*100:.1f}%)
            - Glucose: {glucose}, BMI: {bmi:.1f}
            - Age: {age}, Blood Pressure: {bp}
            
            Provide diabetes prevention/management advice."""
            
            advice = get_ai_response(prompt, health_data)
            st.markdown("### 💊 Diabetes Management Recommendations")
            st.markdown(f"""
            <div class="prediction-card">
            {advice}
            </div>
            """, unsafe_allow_html=True)

elif page == "🧠 Parkinson's Screening" and models:
    st.markdown("### 🧠 Parkinson's Disease Screening")
    st.markdown("*Voice Analysis & Motor Function Assessment*")
    
    with st.form("parkinsons_screening"):
        st.markdown("**🎙️ Voice Analysis Parameters**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fo = st.number_input("Fundamental Frequency (Hz)", 50.0, 300.0, 150.0)
            fhi = st.number_input("Max Frequency (Hz)", 100.0, 600.0, 200.0)
            flo = st.number_input("Min Frequency (Hz)", 50.0, 200.0, 100.0)
            jitter_pct = st.number_input("Jitter (%)", 0.0, 0.05, 0.005, 0.001)
            
        with col2:
            shimmer = st.number_input("Shimmer", 0.0, 0.15, 0.03, 0.001)
            nhr = st.number_input("Noise-to-Harmonics Ratio", 0.0, 0.5, 0.02, 0.001)
            hnr = st.number_input("Harmonics-to-Noise Ratio", 0.0, 40.0, 20.0)
            rpde = st.number_input("RPDE", 0.0, 1.0, 0.5, 0.01)
            
        with col3:
            dfa = st.number_input("DFA", 0.0, 1.0, 0.7, 0.01)
            spread1 = st.number_input("Spread1", -10.0, 0.0, -5.0, 0.1)
            spread2 = st.number_input("Spread2", 0.0, 1.0, 0.2, 0.01)
            ppe = st.number_input("PPE", 0.0, 1.0, 0.2, 0.01)
        
        # Simplified additional parameters
        st.markdown("**🔬 Additional Voice Metrics**")
        col4, col5 = st.columns(2)
        with col4:
            jitter_abs = jitter_pct * fo / 100000  # Approximate conversion
            rap = jitter_pct * 0.5
            ppq = jitter_pct * 0.7
            ddp = rap * 3
            
        with col5:
            shimmer_db = shimmer * 10
            apq3 = shimmer * 0.8
            apq5 = shimmer * 1.2
            apq = shimmer * 1.5
            dda = apq3 * 3
            d2 = 2.0 + np.random.normal(0, 0.5)
        
        submitted = st.form_submit_button("🔬 Screen for Parkinson's", use_container_width=True)
        
        if submitted:
            # Prepare feature array (22 features excluding name and status)
            features_input = np.array([[
                fo, fhi, flo, jitter_pct, jitter_abs, rap, ppq, ddp,
                shimmer, shimmer_db, apq3, apq5, apq, dda, nhr, hnr,
                rpde, dfa, spread1, spread2, d2, ppe
            ]])
            
            # Scale features and predict
            model, feature_names, scaler = models['parkinsons']
            scaled_input = scaler.transform(features_input)
            prediction = model.predict(scaled_input)[0]
            probability = model.predict_proba(scaled_input)[0]
            
            # Results
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🧠 Assessment", "Positive Indicators" if prediction == 1 else "Negative")
            with col2:
                st.metric("📊 Probability", f"{probability[1]*100:.1f}%")
            with col3:
                st.metric("🎯 Confidence", f"{max(probability)*100:.1f}%")
            
            if prediction == 1:
                st.warning("⚠️ **Parkinson's Indicators Detected** - Consult neurologist")
            else:
                st.success("✅ **No Strong Parkinson's Indicators**")
            
            # Voice analysis chart
            voice_metrics = {
                'Jitter': jitter_pct * 1000,
                'Shimmer': shimmer * 100,
                'HNR': hnr,
                'NHR': nhr * 100
            }
            
            fig = px.bar(
                x=list(voice_metrics.keys()),
                y=list(voice_metrics.values()),
                title="Voice Quality Metrics",
                color=list(voice_metrics.values()),
                color_continuous_scale="RdYlBu_r"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # AI Analysis
            health_data = {'risk_level': 'moderate' if prediction == 1 else 'low'}
            prompt = f"""Parkinson's Screening Results:
            - Assessment: {'Positive indicators' if prediction == 1 else 'Negative'}
            - Probability: {probability[1]*100:.1f}%
            - Voice metrics: Jitter {jitter_pct:.3f}, Shimmer {shimmer:.3f}
            
            Provide neurological health guidance."""
            
            advice = get_ai_response(prompt, health_data)
            st.markdown("### 🧠 Neurological Health Guidance")
            st.markdown(f"""
            <div class="prediction-card">
            {advice}
            </div>
            """, unsafe_allow_html=True)

else:  # Smart Health Tips
    st.markdown("### 💡 Smart Health Tips & Wellness Guide")
    
    with st.form("health_tips"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**👤 Personal Profile**")
            age_group = st.selectbox("Age Group", ["18-30", "31-45", "46-60", "60+"])
            health_goal = st.selectbox("Primary Goal", [
                "Weight Management", "Fitness Improvement", "Heart Health", 
                "Diabetes Prevention", "Stress Reduction", "Better Sleep", "General Wellness"
            ])
            activity_level = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
            
        with col2:
            st.markdown("**🎯 Preferences**")
            time_available = st.selectbox("Daily Time Available", ["15-30 min", "30-60 min", "1-2 hours", "2+ hours"])
            dietary_preference = st.selectbox("Dietary Preference", [
                "No restrictions", "Vegetarian", "Vegan", "Mediterranean", "Low-carb", "Keto"
            ])
            health_conditions = st.multiselect("Health Conditions", [
                "Hypertension", "Diabetes", "High Cholesterol", "Anxiety", "Arthritis", "None"
            ])
        
        submitted = st.form_submit_button("💡 Generate Smart Health Tips", use_container_width=True)
        
        if submitted:
            # Health score calculation
            health_score = 7  # Base score
            
            if activity_level in ["Active", "Very Active"]: health_score += 1
            elif activity_level == "Sedentary": health_score -= 1
            
            if dietary_preference in ["Mediterranean", "Vegetarian"]: health_score += 1
            if len([c for c in health_conditions if c != "None"]) == 0: health_score += 1
            
            health_score = max(5, min(health_score, 10))
            
            # Display personalized dashboard
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🎯 Health Score", f"{health_score}/10")
            with col2:
                st.metric("📊 Age Group", age_group)
            with col3:
                st.metric("🏃‍♂️ Activity", activity_level)
            with col4:
                st.metric("⏱️ Time Budget", time_available)
            
            # Smart recommendations
            health_data = {
                'age_group': age_group,
                'goal': health_goal,
                'activity_level': activity_level,
                'conditions': health_conditions
            }
            
            prompt = f"""Create personalized health plan:
            - Age: {age_group}, Goal: {health_goal}
            - Activity: {activity_level}, Time: {time_available}
            - Diet: {dietary_preference}
            - Conditions: {', '.join([c for c in health_conditions if c != 'None']) or 'None'}
            
            Provide 4 specific, actionable daily recommendations."""
            
            advice = get_ai_response(prompt, health_data)
            
            st.markdown("### 🎯 Your Personalized Health Plan")
            st.markdown(f"""
            <div class="prediction-card">
            {advice}
            </div>
            """, unsafe_allow_html=True)
            
            # Quick health tips
            st.markdown("### ⚡ Quick Daily Tips")
            tips_data = {
                "💧 Hydration": f"Drink {8 + (1 if activity_level in ['Active', 'Very Active'] else 0)} glasses of water daily",
                "😴 Sleep": "Maintain 7-9 hours quality sleep with consistent schedule",
                "🚶 Movement": f"Take a {5 if time_available == '15-30 min' else 10}-minute walk every 2 hours",
                "🧘 Mindfulness": "Practice 5-10 minutes of deep breathing or meditation"
            }
            
            cols = st.columns(len(tips_data))
            for i, (tip, desc) in enumerate(tips_data.items()):
                with cols[i]:
                    st.markdown(f"""
                    <div class="health-tip">
                        <h4>{tip}</h4>
                        <p>{desc}</p>
                    </div>
                    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem; background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%); border-radius: 10px; margin-top: 2rem;'>
    <p><strong>⚠️ Medical Disclaimer:</strong> This application provides educational health insights and should not replace professional medical advice.</p>
    <p><strong>Always consult qualified healthcare providers for medical decisions and serious health concerns.</strong></p>
    <p style='margin-top: 1rem;'>🤖 Powered by Advanced Machine Learning & Meta Llama 3.1 AI | © 2025 AI Health Copilot</p>
</div>
""", unsafe_allow_html=True)
