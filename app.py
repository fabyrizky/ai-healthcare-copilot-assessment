import streamlit as st
import json
from datetime import datetime
import math

# Set page configuration
st.set_page_config(
    page_title="AI Health Copilot",
    layout="wide",
    page_icon="🧑‍⚕️",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional appearance
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .prediction-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 6px solid #667eea;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .risk-card-low {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 6px solid #28a745;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .risk-card-moderate {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 6px solid #ffc107;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .risk-card-high {
        background: linear-gradient(135deg, #f8d7da 0%, #f1c2c7 100%);
        border-left: 6px solid #dc3545;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
    }
    
    .sidebar-logo {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .info-box {
        background: #e3f2fd;
        border: 1px solid #bbdefb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff8e1;
        border: 1px solid #ffecb3;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #e8f5e8;
        border: 1px solid #c8e6c9;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: #e9ecef;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Advanced Health Assessment Algorithms
class HealthAssessment:
    
    @staticmethod
    def calculate_diabetes_risk(age, bmi, glucose, bp_systolic, family_history, exercise, diet, waist_hip_ratio=0.85):
        """Advanced diabetes risk calculation using validated risk factors"""
        score = 0
        risk_factors = []
        
        # Age factor (ADA guidelines)
        if age >= 65:
            score += 4
            risk_factors.append("Advanced age (≥65)")
        elif age >= 45:
            score += 3
            risk_factors.append("Middle age (45-64)")
        elif age >= 35:
            score += 1
            risk_factors.append("Age over 35")
        
        # BMI factor (WHO classification)
        if bmi >= 35:
            score += 5
            risk_factors.append("Severe obesity (BMI ≥35)")
        elif bmi >= 30:
            score += 4
            risk_factors.append("Obesity (BMI 30-34.9)")
        elif bmi >= 25:
            score += 2
            risk_factors.append("Overweight (BMI 25-29.9)")
        elif bmi >= 23:  # Asian cutoff
            score += 1
            risk_factors.append("High-normal BMI (≥23)")
        
        # Glucose factor (ADA criteria)
        if glucose >= 126:
            score += 6
            risk_factors.append("Diabetic range glucose (≥126 mg/dL)")
        elif glucose >= 100:
            score += 3
            risk_factors.append("Pre-diabetic glucose (100-125 mg/dL)")
        elif glucose >= 90:
            score += 1
            risk_factors.append("High-normal glucose")
        
        # Blood pressure factor
        if bp_systolic >= 140:
            score += 2
            risk_factors.append("High blood pressure (≥140)")
        elif bp_systolic >= 130:
            score += 1
            risk_factors.append("Elevated blood pressure")
        
        # Family history
        if family_history == "Both parents":
            score += 4
            risk_factors.append("Strong family history (both parents)")
        elif family_history == "One parent":
            score += 2
            risk_factors.append("Family history (one parent)")
        elif family_history == "Siblings":
            score += 2
            risk_factors.append("Family history (siblings)")
        
        # Exercise factor
        if exercise == "Never":
            score += 3
            risk_factors.append("Sedentary lifestyle")
        elif exercise == "Rarely":
            score += 2
            risk_factors.append("Minimal physical activity")
        elif exercise == "Sometimes":
            score += 1
            risk_factors.append("Inconsistent exercise")
        
        # Diet factor
        if diet == "Poor":
            score += 2
            risk_factors.append("Poor dietary habits")
        elif diet == "Fair":
            score += 1
            risk_factors.append("Suboptimal diet")
        
        # Waist-hip ratio (central obesity)
        if waist_hip_ratio > 0.95:  # Male
            score += 2
            risk_factors.append("Central obesity (high waist-hip ratio)")
        elif waist_hip_ratio > 0.85:  # Female
            score += 1
            risk_factors.append("Moderate central obesity")
        
        return score, risk_factors
    
    @staticmethod
    def calculate_heart_risk(age, sex, bp_systolic, bp_diastolic, cholesterol_total, 
                           hdl, ldl, smoking, family_history, exercise, bmi):
        """Framingham-based cardiovascular risk assessment"""
        score = 0
        risk_factors = []
        
        # Age and sex factor
        if sex == "Male":
            if age >= 65:
                score += 5
                risk_factors.append("Male ≥65 years")
            elif age >= 55:
                score += 4
                risk_factors.append("Male 55-64 years")
            elif age >= 45:
                score += 3
                risk_factors.append("Male 45-54 years")
            elif age >= 35:
                score += 2
                risk_factors.append("Male 35-44 years")
        else:  # Female
            if age >= 65:
                score += 4
                risk_factors.append("Female ≥65 years")
            elif age >= 55:
                score += 3
                risk_factors.append("Female 55-64 years")
            elif age >= 45:
                score += 2
                risk_factors.append("Female 45-54 years")
        
        # Blood pressure (updated AHA guidelines)
        if bp_systolic >= 180 or bp_diastolic >= 110:
            score += 6
            risk_factors.append("Stage 2 hypertension (≥180/110)")
        elif bp_systolic >= 140 or bp_diastolic >= 90:
            score += 4
            risk_factors.append("Stage 1 hypertension (140-179/90-109)")
        elif bp_systolic >= 130 or bp_diastolic >= 80:
            score += 2
            risk_factors.append("Elevated blood pressure (130-139/80-89)")
        elif bp_systolic >= 120:
            score += 1
            risk_factors.append("High normal blood pressure")
        
        # Cholesterol profile
        if cholesterol_total >= 280:
            score += 4
            risk_factors.append("Very high total cholesterol (≥280)")
        elif cholesterol_total >= 240:
            score += 3
            risk_factors.append("High total cholesterol (240-279)")
        elif cholesterol_total >= 200:
            score += 1
            risk_factors.append("Borderline high cholesterol (200-239)")
        
        # HDL cholesterol (protective factor)
        if hdl < 35:
            score += 3
            risk_factors.append("Very low HDL cholesterol (<35)")
        elif hdl < 40:
            score += 2
            risk_factors.append("Low HDL cholesterol (<40)")
        elif hdl >= 60:
            score -= 1  # Protective factor
            risk_factors.append("High HDL cholesterol (≥60) - protective")
        
        # LDL cholesterol
        if ldl >= 190:
            score += 4
            risk_factors.append("Very high LDL cholesterol (≥190)")
        elif ldl >= 160:
            score += 3
            risk_factors.append("High LDL cholesterol (160-189)")
        elif ldl >= 130:
            score += 2
            risk_factors.append("Borderline high LDL (130-159)")
        elif ldl >= 100:
            score += 1
            risk_factors.append("Above optimal LDL (100-129)")
        
        # Smoking
        if smoking == "Current heavy (>20/day)":
            score += 5
            risk_factors.append("Heavy smoking (>20 cigarettes/day)")
        elif smoking == "Current moderate":
            score += 3
            risk_factors.append("Moderate smoking")
        elif smoking == "Former (quit <5 years)":
            score += 1
            risk_factors.append("Recent former smoker")
        
        # Family history
        if family_history == "Early onset (<50)":
            score += 4
            risk_factors.append("Family history of early heart disease")
        elif family_history == "Late onset (50-65)":
            score += 2
            risk_factors.append("Family history of heart disease")
        
        # Exercise
        if exercise == "Sedentary":
            score += 2
            risk_factors.append("Sedentary lifestyle")
        elif exercise == "Minimal":
            score += 1
            risk_factors.append("Insufficient physical activity")
        
        # BMI
        if bmi >= 35:
            score += 3
            risk_factors.append("Severe obesity (BMI ≥35)")
        elif bmi >= 30:
            score += 2
            risk_factors.append("Obesity (BMI 30-34.9)")
        elif bmi >= 25:
            score += 1
            risk_factors.append("Overweight (BMI 25-29.9)")
        
        return score, risk_factors
    
    @staticmethod
    def assess_mental_health(stress_level, sleep_hours, social_support, exercise, 
                           work_satisfaction, life_events, coping_skills):
        """Comprehensive mental health assessment"""
        score = 0
        concerns = []
        strengths = []
        
        # Stress level assessment
        stress_mapping = {
            "Overwhelming": (5, "Overwhelming stress levels"),
            "Very High": (4, "Very high stress"),
            "High": (3, "High stress levels"),
            "Moderate": (2, "Moderate stress"),
            "Low": (1, "Low stress"),
            "Very Low": (0, "Minimal stress")
        }
        if stress_level in stress_mapping:
            stress_score, stress_desc = stress_mapping[stress_level]
            score += stress_score
            if stress_score >= 3:
                concerns.append(stress_desc)
            elif stress_score <= 1:
                strengths.append("Good stress management")
        
        # Sleep assessment (CDC guidelines)
        if sleep_hours < 6:
            score += 3
            concerns.append("Insufficient sleep (<6 hours)")
        elif sleep_hours < 7:
            score += 2
            concerns.append("Below recommended sleep (6-7 hours)")
        elif sleep_hours > 9:
            score += 1
            concerns.append("Excessive sleep (>9 hours)")
        elif 7 <= sleep_hours <= 9:
            strengths.append("Healthy sleep duration")
        
        # Social support
        social_mapping = {
            "Excellent": (0, "Strong social support network"),
            "Good": (1, "Good social connections"),
            "Fair": (2, "Limited social support"),
            "Poor": (3, "Inadequate social support"),
            "None": (4, "Social isolation")
        }
        if social_support in social_mapping:
            social_score, social_desc = social_mapping[social_support]
            score += social_score
            if social_score >= 2:
                concerns.append(social_desc)
            else:
                strengths.append(social_desc)
        
        # Exercise impact on mental health
        exercise_mapping = {
            "Daily": (0, "Regular physical activity"),
            "Most days": (0, "Frequent exercise"),
            "Weekly": (1, "Some physical activity"),
            "Occasionally": (2, "Minimal exercise"),
            "Rarely": (3, "Insufficient physical activity"),
            "Never": (4, "Sedentary lifestyle")
        }
        if exercise in exercise_mapping:
            ex_score, ex_desc = exercise_mapping[exercise]
            score += ex_score
            if ex_score >= 2:
                concerns.append(f"Mental health impact: {ex_desc}")
            else:
                strengths.append(f"Mental health benefit: {ex_desc}")
        
        # Work/life satisfaction
        satisfaction_mapping = {
            "Very satisfied": (0, "High life satisfaction"),
            "Satisfied": (1, "Good life satisfaction"),
            "Neutral": (2, "Moderate satisfaction"),
            "Dissatisfied": (3, "Low life satisfaction"),
            "Very dissatisfied": (4, "Poor life satisfaction")
        }
        if work_satisfaction in satisfaction_mapping:
            sat_score, sat_desc = satisfaction_mapping[work_satisfaction]
            score += sat_score
            if sat_score >= 3:
                concerns.append(sat_desc)
            elif sat_score <= 1:
                strengths.append(sat_desc)
        
        # Recent life events
        if life_events == "Major stressful events":
            score += 3
            concerns.append("Recent major life stressors")
        elif life_events == "Some changes":
            score += 1
            concerns.append("Recent life changes")
        elif life_events == "Stable":
            strengths.append("Life stability")
        
        # Coping skills
        coping_mapping = {
            "Excellent": (0, "Strong coping strategies"),
            "Good": (1, "Adequate coping skills"),
            "Fair": (2, "Limited coping strategies"),
            "Poor": (3, "Inadequate coping skills")
        }
        if coping_skills in coping_mapping:
            cop_score, cop_desc = coping_mapping[coping_skills]
            score += cop_score
            if cop_score >= 2:
                concerns.append(cop_desc)
            else:
                strengths.append(cop_desc)
        
        return score, concerns, strengths

# Sidebar
st.sidebar.markdown("""
<div class="sidebar-logo">
    <h2>🧑‍⚕️ AI Health Copilot</h2>
    <p><strong>Advanced Health Analytics</strong></p>
    <p style="font-size: 0.9em;">Evidence-based assessments</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🎯 Assessment Tools")
page = st.sidebar.selectbox(
    "Choose Assessment",
    [
        "🩺 Diabetes Risk Calculator", 
        "❤️ Cardiovascular Assessment", 
        "🧠 Mental Health Evaluation",
        "📊 Health Dashboard",
        "🎯 Personalized Recommendations"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About This Tool")
st.sidebar.info("""
**Professional Health Assessment**

This tool uses evidence-based algorithms and clinical guidelines to provide comprehensive health risk assessments.

**Features:**
- Advanced risk scoring
- Detailed analysis
- Personalized recommendations
- Professional insights
""")

# Main header
st.markdown("""
<div class="main-header">
    <h1>🧑‍⚕️ Advanced Health Copilot</h1>
    <p style="font-size: 1.2em; margin-bottom: 0;">
        <strong>Professional-Grade Health Risk Assessment Platform</strong>
    </p>
    <p style="font-size: 1em; opacity: 0.9; margin-top: 0.5rem;">
        Evidence-based algorithms • Clinical guidelines • Personalized insights
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize health assessment
health_assess = HealthAssessment()

# Diabetes Risk Assessment
if page == "🩺 Diabetes Risk Calculator":
    st.header("🩺 Advanced Diabetes Risk Assessment")
    
    st.markdown("""
    <div class="info-box">
        <h4>📋 Clinical Assessment Protocol</h4>
        <p>This assessment uses validated risk factors from the American Diabetes Association (ADA) 
        and incorporates international guidelines for diabetes risk stratification.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Patient Information
    st.subheader("👤 Patient Demographics")
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age (years)", min_value=18, max_value=100, value=35, 
                             help="Age is a significant risk factor for type 2 diabetes")
        sex = st.selectbox("Sex", ["Male", "Female"], help="Biological sex affects risk calculations")
        height = st.number_input("Height (cm)", min_value=140, max_value=220, value=170)
        weight = st.number_input("Weight (kg)", min_value=40, max_value=200, value=70)
    
    with col2:
        waist = st.number_input("Waist circumference (cm)", min_value=60, max_value=150, value=85,
                               help="Central obesity is a key risk factor")
        hip = st.number_input("Hip circumference (cm)", min_value=70, max_value=160, value=95,
                             help="Used to calculate waist-hip ratio")
        glucose = st.number_input("Fasting glucose (mg/dL)", min_value=70, max_value=300, value=95,
                                 help="Recent fasting blood glucose level")
        bp_systolic = st.number_input("Systolic blood pressure", min_value=80, max_value=200, value=120)
    
    # Calculate BMI and waist-hip ratio
    bmi = weight / ((height/100) ** 2)
    waist_hip_ratio = waist / hip
    
    # Risk Factors
    st.subheader("🧬 Risk Factor Assessment")
    col1, col2 = st.columns(2)
    
    with col1:
        family_history = st.selectbox("Family history of diabetes", 
                                    ["None", "Grandparents", "One parent", "Both parents", "Siblings"],
                                    help="Genetic predisposition to diabetes")
        exercise = st.selectbox("Physical activity level", 
                              ["Daily vigorous", "Regular moderate", "Sometimes", "Rarely", "Never"],
                              help="Regular exercise reduces diabetes risk")
        diet = st.selectbox("Overall diet quality", 
                          ["Excellent", "Good", "Fair", "Poor"],
                          help="Diet quality affects glucose metabolism")
    
    with col2:
        sleep_hours = st.number_input("Average sleep hours", min_value=3, max_value=12, value=7,
                                     help="Sleep duration affects glucose regulation")
        stress_level = st.selectbox("Chronic stress level", 
                                  ["Low", "Moderate", "High", "Very high"],
                                  help="Chronic stress can affect blood sugar")
        smoking = st.selectbox("Smoking status", 
                             ["Never", "Former", "Current"],
                             help="Smoking increases diabetes risk")
    
    # Assessment Button
    if st.button("🔍 Calculate Diabetes Risk", use_container_width=True):
        # Calculate risk score
        risk_score, risk_factors = health_assess.calculate_diabetes_risk(
            age, bmi, glucose, bp_systolic, family_history, exercise, diet, waist_hip_ratio
        )
        
        # Additional risk factors
        if sleep_hours < 6 or sleep_hours > 9:
            risk_score += 1
            risk_factors.append("Sleep duration outside optimal range")
        
        if stress_level in ["High", "Very high"]:
            risk_score += 1
            risk_factors.append("Chronic high stress")
        
        if smoking == "Current":
            risk_score += 2
            risk_factors.append("Current smoking")
        elif smoking == "Former":
            risk_score += 1
            risk_factors.append("Former smoking history")
        
        # Risk categorization
        if risk_score <= 5:
            risk_level = "Low Risk"
            risk_color = "success"
            risk_percentage = min(5 + risk_score, 15)
            card_class = "risk-card-low"
        elif risk_score <= 12:
            risk_level = "Moderate Risk"
            risk_color = "warning"
            risk_percentage = 15 + (risk_score - 5) * 5
            card_class = "risk-card-moderate"
        else:
            risk_level = "High Risk"
            risk_color = "error"
            risk_percentage = min(50 + (risk_score - 12) * 5, 85)
            card_class = "risk-card-high"
        
        # Display results
        st.markdown(f"""
        <div class="{card_class}">
            <h3>📊 Diabetes Risk Assessment Results</h3>
            <h2>{risk_level}</h2>
            <p><strong>Risk Score:</strong> {risk_score}/25</p>
            <p><strong>Estimated 10-year risk:</strong> ~{risk_percentage}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>BMI</h4>
                <h2>{bmi:.1f}</h2>
                <p>{'Normal' if 18.5 <= bmi < 25 else 'Overweight' if 25 <= bmi < 30 else 'Obese' if bmi >= 30 else 'Underweight'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Waist-Hip Ratio</h4>
                <h2>{waist_hip_ratio:.2f}</h2>
                <p>{'Normal' if waist_hip_ratio < 0.85 else 'Elevated'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            glucose_status = "Normal" if glucose < 100 else "Pre-diabetic" if glucose < 126 else "Diabetic range"
            st.markdown(f"""
            <div class="metric-card">
                <h4>Glucose Status</h4>
                <h2>{glucose} mg/dL</h2>
                <p>{glucose_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            bp_status = "Normal" if bp_systolic < 120 else "Elevated" if bp_systolic < 130 else "High"
            st.markdown(f"""
            <div class="metric-card">
                <h4>Blood Pressure</h4>
                <h2>{bp_systolic} mmHg</h2>
                <p>{bp_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Risk factors analysis
        st.markdown("""
        <div class="prediction-card">
            <h3>🎯 Risk Factor Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if risk_factors:
            st.markdown("**Identified Risk Factors:**")
            for factor in risk_factors:
                st.markdown(f"• {factor}")
        else:
            st.success("✅ No significant risk factors identified")
        
        # Detailed recommendations
        st.markdown("""
        <div class="prediction-card">
            <h3>💡 Evidence-Based Recommendations</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Personalized recommendations based on risk level and factors
        recommendations = []
        
        if risk_level == "High Risk":
            recommendations.extend([
                "🏥 **Immediate Action**: Consult with healthcare provider for comprehensive diabetes screening",
                "📅 **Testing**: Request HbA1c, oral glucose tolerance test, and lipid panel",
                "⚖️ **Weight Management**: If BMI >25, target 5-10% weight reduction",
                "🥗 **Nutrition**: Follow diabetes prevention diet (low glycemic index, portion control)",
                "🏃‍♂️ **Exercise**: Minimum 150 minutes moderate activity + 2 strength training sessions/week"
            ])
        elif risk_level == "Moderate Risk":
            recommendations.extend([
                "📊 **Annual Screening**: Schedule yearly glucose and HbA1c testing",
                "🎯 **Lifestyle Focus**: Implement preventive lifestyle changes",
                "🥙 **Diet Modification**: Reduce refined carbohydrates, increase fiber intake",
                "🚶‍♀️ **Activity Goal**: Aim for 10,000 steps daily or equivalent exercise"
            ])
        else:
            recommendations.extend([
                "✅ **Maintain Status**: Continue current healthy lifestyle",
                "📅 **Routine Screening**: Follow standard screening guidelines for your age",
                "🏆 **Prevention Focus**: Maintain healthy weight and active lifestyle"
            ])
        
        # Specific recommendations based on risk factors
        if bmi >= 25:
            recommendations.append("⚖️ **Weight Loss**: Target BMI <25 through caloric deficit of 500-750 calories/day")
        
        if "family history" in str(risk_factors).lower():
            recommendations.append("🧬 **Genetic Risk**: Consider genetic counseling and earlier/more frequent screening")
        
        if glucose >= 100:
            recommendations.append("🍯 **Glucose Management**: Monitor carbohydrate intake, consider continuous glucose monitoring")
        
        if exercise in ["Rarely", "Never"]:
            recommendations.append("💪 **Exercise Priority**: Start with 10-minute walks, gradually increase to 30 minutes daily")
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
        
        # Progress tracking suggestions
        st.markdown("""
        <div class="warning-box">
            <h4>📈 Recommended Monitoring</h4>
            <p><strong>Track these metrics:</strong></p>
            <ul>
                <li>Fasting glucose (weekly if high risk)</li>
                <li>Weight and BMI (weekly)</li>
                <li>Blood pressure (if elevated)</li>
                <li>Physical activity minutes (daily)</li>
                <li>HbA1c (every 3-6 months if high risk)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Cardiovascular Assessment
elif page == "❤️ Cardiovascular Assessment":
    st.header("❤️ Comprehensive Cardiovascular Risk Assessment")
    
    st.markdown("""
    <div class="info-box">
        <h4>🫀 Framingham Risk Score Protocol</h4>
        <p>This assessment incorporates the Framingham Heart Study algorithms and American Heart Association 
        guidelines for cardiovascular disease risk prediction.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Demographics
    st.subheader("👤 Patient Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=20, max_value=100, value=45)
        sex = st.selectbox("Sex", ["Male", "Female"])
        height = st.number_input("Height (cm)", min_value=140, max_value=220, value=170)
        weight = st.number_input("Weight (kg)", min_value=40, max_value=200, value=75)
    
    with col2:
        ethnicity = st.selectbox("Ethnicity", ["Caucasian", "African American", "Hispanic", "Asian", "Other"])
        occupation = st.selectbox("Occupation type", ["Sedentary", "Light activity", "Moderate activity", "Heavy labor"])
        education = st.selectbox("Education level", ["High school", "College", "Graduate degree"])
        income = st.selectbox("Income level", ["Low", "Middle", "High"])
    
    bmi = weight / ((height/100) ** 2)
    
    # Cardiovascular measurements
    st.subheader("🩺 Clinical Measurements")
    col1, col2 = st.columns(2)
    
    with col1:
        bp_systolic = st.number_input("Systolic BP (mmHg)", min_value=80, max_value=220, value=120,
                                     help="Upper number in blood pressure reading")
        bp_diastolic = st.number_input("Diastolic BP (mmHg)", min_value=50, max_value=130, value=80,
                                      help="Lower number in blood pressure reading")
        resting_hr = st.number_input("Resting heart rate (bpm)", min_value=40, max_value=120, value=70)
        cholesterol_total = st.number_input("Total cholesterol (mg/dL)", min_value=100, max_value=400, value=180)
    
    with col2:
        hdl = st.number_input("HDL cholesterol (mg/dL)", min_value=20, max_value=100, value=50,
                             help="Good cholesterol - higher is better")
        ldl = st.number_input("LDL cholesterol (mg/dL)", min_value=50, max_value=250, value=100,
                             help="Bad cholesterol - lower is better")
        triglycerides = st.number_input("Triglycerides (mg/dL)", min_value=50, max_value=500, value=120)
        glucose = st.number_input("Fasting glucose (mg/dL)", min_value=70, max_value=200, value=90)
    
    # Risk factors
    st.subheader("⚠️ Cardiovascular Risk Factors")
    col1, col2 = st.columns(2)
    
    with col1:
        smoking = st.selectbox("Smoking status", 
                              ["Never smoked", "Former (quit >5 years)", "Former (quit <5 years)", 
                               "Current moderate", "Current heavy (>20/day)"])
        family_history = st.selectbox("Family history of heart disease", 
                                    ["None", "Late onset (>65)", "Late onset (50-65)", "Early onset (<50)"])
        diabetes = st.selectbox("Diabetes status", 
                               ["No diabetes", "Pre-diabetes", "Type 2 diabetes", "Type 1 diabetes"])
        exercise = st.selectbox("Exercise frequency", 
                              ["Daily vigorous", "Regular moderate", "Weekly", "Minimal", "Sedentary"])
    
    with col2:
        stress_level = st.selectbox("Chronic stress level", 
                                  ["Low", "Moderate", "High", "Very high"])
        alcohol = st.selectbox("Alcohol consumption", 
                             ["None", "Light (1-7 drinks/week)", "Moderate (8-14/week)", "Heavy (>14/week)"])
        sleep_quality = st.selectbox("Sleep quality", 
                                   ["Excellent", "Good", "Fair", "Poor"])
        medications = st.multiselect("Current medications", 
                                   ["None", "Blood pressure meds", "Cholesterol meds", "Diabetes meds", 
                                    "Blood thinners", "Other cardiac meds"])
    
    if st.button("💓 Calculate Cardiovascular Risk", use_container_width=True):
        # Calculate comprehensive cardiovascular risk
        risk_score, risk_factors = health_assess.calculate_heart_risk(
            age, sex, bp_systolic, bp_diastolic, cholesterol_total, hdl, ldl, 
            smoking, family_history, exercise, bmi
        )
        
        # Additional risk factors
        if diabetes in ["Type 2 diabetes", "Type 1 diabetes"]:
            risk_score += 4
            risk_factors.append("Diabetes mellitus")
        elif diabetes == "Pre-diabetes":
            risk_score += 2
            risk_factors.append("Pre-diabetes")
        
        if stress_level in ["High", "Very high"]:
            risk_score += 2
            risk_factors.append("Chronic high stress")
        
        if alcohol == "Heavy (>14/week)":
            risk_score += 1
            risk_factors.append("Heavy alcohol consumption")
        
        if sleep_quality in ["Fair", "Poor"]:
            risk_score += 1
            risk_factors.append("Poor sleep quality")
        
        if triglycerides >= 200:
            risk_score += 1
            risk_factors.append("High triglycerides")
        
        # Risk stratification
        if risk_score <= 8:
            risk_level = "Low Risk"
            risk_percentage = 5 + risk_score
            card_class = "risk-card-low"
            risk_description = "Low 10-year cardiovascular disease risk"
        elif risk_score <= 15:
            risk_level = "Moderate Risk"
            risk_percentage = 15 + (risk_score - 8) * 3
            card_class = "risk-card-moderate"
            risk_description = "Moderate 10-year cardiovascular disease risk"
        else:
            risk_level = "High Risk"
            risk_percentage = min(35 + (risk_score - 15) * 4, 75)
            card_class = "risk-card-high"
            risk_description = "High 10-year cardiovascular disease risk"
        
        # Results display
        st.markdown(f"""
        <div class="{card_class}">
            <h3>💓 Cardiovascular Risk Assessment</h3>
            <h2>{risk_level}</h2>
            <p><strong>Risk Score:</strong> {risk_score}/30</p>
            <p><strong>10-year CVD risk:</strong> ~{risk_percentage}%</p>
            <p>{risk_description}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Clinical metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            bp_category = ("Normal" if bp_systolic < 120 and bp_diastolic < 80 
                          else "Elevated" if bp_systolic < 130 
                          else "Stage 1" if bp_systolic < 140 
                          else "Stage 2")
            st.markdown(f"""
            <div class="metric-card">
                <h4>Blood Pressure</h4>
                <h3>{bp_systolic}/{bp_diastolic}</h3>
                <p>{bp_category}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            chol_ratio = cholesterol_total / hdl if hdl > 0 else 0
            ratio_status = "Optimal" if chol_ratio < 3.5 else "Good" if chol_ratio < 5 else "High risk"
            st.markdown(f"""
            <div class="metric-card">
                <h4>Cholesterol Ratio</h4>
                <h3>{chol_ratio:.1f}</h3>
                <p>{ratio_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            bmi_category = ("Underweight" if bmi < 18.5 else "Normal" if bmi < 25 
                           else "Overweight" if bmi < 30 else "Obese")
            st.markdown(f"""
            <div class="metric-card">
                <h4>BMI</h4>
                <h3>{bmi:.1f}</h3>
                <p>{bmi_category}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            hr_status = "Low" if resting_hr < 60 else "Normal" if resting_hr < 100 else "Elevated"
            st.markdown(f"""
            <div class="metric-card">
                <h4>Resting HR</h4>
                <h3>{resting_hr} bpm</h3>
                <p>{hr_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Risk factors breakdown
        st.markdown("""
        <div class="prediction-card">
            <h3>🎯 Identified Risk Factors</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if risk_factors:
            for factor in risk_factors:
                if "protective" in factor.lower():
                    st.success(f"✅ {factor}")
                else:
                    st.warning(f"⚠️ {factor}")
        else:
            st.success("✅ No major risk factors identified")
        
        # Comprehensive recommendations
        st.markdown("""
        <div class="prediction-card">
            <h3>💡 Cardiovascular Health Recommendations</h3>
        </div>
        """, unsafe_allow_html=True)
        
        recommendations = []
        
        # Risk level specific recommendations
        if risk_level == "High Risk":
            recommendations.extend([
                "🏥 **Immediate Medical Consultation**: Comprehensive cardiovascular evaluation needed",
                "💊 **Medication Review**: Discuss statin therapy, ACE inhibitors, or other cardioprotective medications",
                "📊 **Advanced Testing**: Consider stress testing, coronary calcium scoring, or echocardiogram",
                "🎯 **Aggressive Risk Factor Modification**: Intensive lifestyle intervention required"
            ])
        elif risk_level == "Moderate Risk":
            recommendations.extend([
                "📅 **Regular Monitoring**: Quarterly check-ups with cardiovascular risk assessment",
                "🎯 **Targeted Interventions**: Focus on modifiable risk factors",
                "💊 **Consider Medications**: Discuss preventive medications with healthcare provider"
            ])
        else:
            recommendations.extend([
                "✅ **Maintain Current Status**: Continue heart-healthy lifestyle",
                "📅 **Annual Screening**: Routine cardiovascular risk assessment"
            ])
        
        # Specific recommendations based on findings
        if bp_systolic >= 140 or bp_diastolic >= 90:
            recommendations.append("🩺 **Blood Pressure Control**: Target <130/80 through diet, exercise, and possibly medication")
        
        if ldl >= 130:
            recommendations.append("🥗 **LDL Cholesterol**: Target <100 mg/dL (or <70 if high risk) through diet and statin therapy")
        
        if hdl < 40:
            recommendations.append("🏃‍♂️ **HDL Improvement**: Increase through aerobic exercise, weight loss, and omega-3 fatty acids")
        
        if smoking != "Never smoked":
            recommendations.append("🚭 **Smoking Cessation**: Immediate priority - reduces risk by 50% within 1 year")
        
        if exercise in ["Minimal", "Sedentary"]:
            recommendations.append("💪 **Exercise Prescription**: 150 minutes moderate cardio + 2 strength sessions weekly")
        
        if bmi >= 25:
            recommendations.append("⚖️ **Weight Management**: Target BMI 18.5-24.9 through caloric deficit")
        
        if stress_level in ["High", "Very high"]:
            recommendations.append("🧘‍♀️ **Stress Management**: Meditation, yoga, counseling, or stress reduction techniques")
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
        
        # Lifestyle prescription
        st.markdown("""
        <div class="success-box">
            <h4>🎯 Evidence-Based Lifestyle Prescription</h4>
            <p><strong>DASH Diet Protocol:</strong></p>
            <ul>
                <li>Fruits & vegetables: 8-10 servings daily</li>
                <li>Whole grains: 6-8 servings daily</li>
                <li>Lean proteins: 6 oz or less daily</li>
                <li>Low-fat dairy: 2-3 servings daily</li>
                <li>Sodium: <2,300mg daily (ideally <1,500mg)</li>
            </ul>
            <p><strong>Exercise Guidelines:</strong></p>
            <ul>
                <li>Aerobic: 150 min moderate OR 75 min vigorous weekly</li>
                <li>Resistance training: 2+ sessions weekly</li>
                <li>Flexibility: Daily stretching</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Mental Health Evaluation
elif page == "🧠 Mental Health Evaluation":
    st.header("🧠 Comprehensive Mental Health Assessment")
    
    st.markdown("""
    <div class="info-box">
        <h4>🧠 Psychological Wellness Evaluation</h4>
        <p>This assessment evaluates multiple dimensions of mental health using validated psychological 
        assessment frameworks and evidence-based indicators of psychological well-being.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Core mental health indicators
    st.subheader("😊 Emotional Well-being Indicators")
    col1, col2 = st.columns(2)
    
    with col1:
        mood_rating = st.slider("Overall mood (past 2 weeks)", 1, 10, 7,
                               help="1 = Very poor, 10 = Excellent")
        energy_level = st.slider("Energy levels", 1, 10, 6,
                                help="1 = Exhausted, 10 = Very energetic")
        life_satisfaction = st.slider("Life satisfaction", 1, 10, 7,
                                     help="1 = Very dissatisfied, 10 = Very satisfied")
        self_esteem = st.slider("Self-confidence", 1, 10, 6,
                               help="1 = Very low, 10 = Very high")
    
    with col2:
        anxiety_level = st.selectbox("Anxiety/worry levels", 
                                   ["Minimal", "Mild", "Moderate", "Severe", "Very severe"])
        depression_signs = st.selectbox("Depression symptoms", 
                                      ["None", "Mild", "Moderate", "Severe"])
        concentration = st.selectbox("Concentration ability", 
                                   ["Excellent", "Good", "Fair", "Poor", "Very poor"])
        irritability = st.selectbox("Irritability/anger", 
                                  ["Rarely", "Sometimes", "Often", "Very often"])
    
    # Sleep and physical factors
    st.subheader("😴 Sleep & Physical Factors")
    col1, col2 = st.columns(2)
    
    with col1:
        sleep_hours = st.number_input("Average sleep hours", min_value=3, max_value=12, value=7)
        sleep_quality = st.selectbox("Sleep quality", 
                                   ["Excellent", "Good", "Fair", "Poor", "Very poor"])
        physical_symptoms = st.multiselect("Physical symptoms", 
                                         ["None", "Headaches", "Fatigue", "Muscle tension", 
                                          "Digestive issues", "Chest tightness", "Other"])
    
    with col2:
        appetite_changes = st.selectbox("Appetite changes", 
                                      ["No change", "Decreased", "Increased", "Very decreased", "Very increased"])
        exercise_frequency = st.selectbox("Exercise frequency", 
                                        ["Daily", "Most days", "Weekly", "Occasionally", "Rarely", "Never"])
        substance_use = st.selectbox("Alcohol/substance use", 
                                   ["None", "Occasional", "Regular", "Heavy", "Problematic"])
    
    # Social and environmental factors
    st.subheader("👥 Social & Environmental Factors")
    col1, col2 = st.columns(2)
    
    with col1:
        social_support = st.selectbox("Social support network", 
                                    ["Excellent", "Good", "Fair", "Poor", "None"])
        relationship_satisfaction = st.selectbox("Relationship satisfaction", 
                                                ["Very satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very dissatisfied"])
        work_satisfaction = st.selectbox("Work/school satisfaction", 
                                       ["Very satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very dissatisfied"])
    
    with col2:
        life_events = st.selectbox("Recent major life events", 
                                 ["None significant", "Some changes", "Major stressful events", "Multiple crises"])
        financial_stress = st.selectbox("Financial stress", 
                                      ["None", "Mild", "Moderate", "Severe", "Overwhelming"])
        coping_skills = st.selectbox("Stress coping ability", 
                                   ["Excellent", "Good", "Fair", "Poor"])
    
    # Behavioral patterns
    st.subheader("🔄 Behavioral Patterns")
    col1, col2 = st.columns(2)
    
    with col1:
        stress_level = st.selectbox("Current stress level", 
                                  ["Very low", "Low", "Moderate", "High", "Very high", "Overwhelming"])
        motivation_level = st.selectbox("Motivation for activities", 
                                      ["Very high", "High", "Moderate", "Low", "Very low"])
        social_withdrawal = st.selectbox("Social withdrawal", 
                                       ["Not at all", "Slightly", "Moderately", "Significantly", "Completely"])
    
    with col2:
        decision_making = st.selectbox("Decision-making ability", 
                                     ["Very easy", "Easy", "Moderate", "Difficult", "Very difficult"])
        future_outlook = st.selectbox("Outlook on future", 
                                    ["Very optimistic", "Optimistic", "Neutral", "Pessimistic", "Very pessimistic"])
        help_seeking = st.selectbox("Willingness to seek help", 
                                  ["Very willing", "Willing", "Neutral", "Reluctant", "Very reluctant"])
    
    if st.button("🧠 Evaluate Mental Health Status", use_container_width=True):
        # Calculate comprehensive mental health score
        mental_score, concerns, strengths = health_assess.assess_mental_health(
            stress_level, sleep_hours, social_support, exercise_frequency, 
            work_satisfaction, life_events, coping_skills
        )
        
        # Additional scoring factors
        mood_score = (10 - mood_rating) * 0.5
        energy_score = (10 - energy_level) * 0.3
        anxiety_scores = {"Minimal": 0, "Mild": 1, "Moderate": 2, "Severe": 3, "Very severe": 4}
        depression_scores = {"None": 0, "Mild": 1, "Moderate": 3, "Severe": 4}
        
        mental_score += mood_score + energy_score
        mental_score += anxiety_scores.get(anxiety_level, 0)
        mental_score += depression_scores.get(depression_signs, 0)
        
        # Concentration and functioning
        conc_scores = {"Excellent": 0, "Good": 0.5, "Fair": 1, "Poor": 2, "Very poor": 3}
        mental_score += conc_scores.get(concentration, 0)
        
        # Sleep impact
        if sleep_quality in ["Poor", "Very poor"]:
            mental_score += 2
            concerns.append("Poor sleep quality affecting mental health")
        elif sleep_quality == "Fair":
            mental_score += 1
            concerns.append("Suboptimal sleep quality")
        
        # Physical symptoms
        if "None" not in physical_symptoms and physical_symptoms:
            mental_score += len(physical_symptoms) * 0.5
            concerns.append("Physical symptoms potentially related to stress/anxiety")
        
        # Social factors
        if relationship_satisfaction in ["Dissatisfied", "Very dissatisfied"]:
            mental_score += 2
            concerns.append("Relationship difficulties")
        
        if financial_stress in ["Severe", "Overwhelming"]:
            mental_score += 2
            concerns.append("Significant financial stress")
        
        # Risk categorization
        if mental_score <= 8:
            wellness_level = "Good Mental Health"
            card_class = "risk-card-low"
            wellness_description = "Strong psychological well-being indicators"
            color_code = "#28a745"
        elif mental_score <= 15:
            wellness_level = "Moderate Concerns"
            card_class = "risk-card-moderate"
            wellness_description = "Some areas for mental health improvement"
            color_code = "#ffc107"
        else:
            wellness_level = "Significant Concerns"
            card_class = "risk-card-high"
            wellness_description = "Professional mental health support recommended"
            color_code = "#dc3545"
        
        # Results display
        st.markdown(f"""
        <div class="{card_class}">
            <h3>🧠 Mental Health Assessment Results</h3>
            <h2>{wellness_level}</h2>
            <p><strong>Wellness Score:</strong> {mental_score:.1f}/25</p>
            <p>{wellness_description}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mental health dashboard
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Mood Rating</h4>
                <h2>{mood_rating}/10</h2>
                <p>{'Excellent' if mood_rating >= 8 else 'Good' if mood_rating >= 6 else 'Needs attention'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Energy Level</h4>
                <h2>{energy_level}/10</h2>
                <p>{'High' if energy_level >= 7 else 'Moderate' if energy_level >= 5 else 'Low'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            sleep_status = "Good" if 7 <= sleep_hours <= 9 and sleep_quality in ["Excellent", "Good"] else "Needs work"
            st.markdown(f"""
            <div class="metric-card">
                <h4>Sleep Health</h4>
                <h2>{sleep_hours}h</h2>
                <p>{sleep_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Stress Level</h4>
                <h2>{stress_level}</h2>
                <p>{'Manageable' if stress_level in ['Very low', 'Low', 'Moderate'] else 'High'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed analysis
        if concerns:
            st.markdown("""
            <div class="prediction-card">
                <h3>⚠️ Areas of Concern</h3>
            </div>
            """, unsafe_allow_html=True)
            for concern in concerns:
                st.warning(f"• {concern}")
        
        if strengths:
            st.markdown("""
            <div class="prediction-card">
                <h3>💪 Mental Health Strengths</h3>
            </div>
            """, unsafe_allow_html=True)
            for strength in strengths:
                st.success(f"• {strength}")
        
        # Comprehensive recommendations
        st.markdown("""
        <div class="prediction-card">
            <h3>💡 Mental Health Recommendations</h3>
        </div>
        """, unsafe_allow_html=True)
        
        recommendations = []
        
        # Risk level specific recommendations
        if wellness_level == "Significant Concerns":
            recommendations.extend([
                "🏥 **Professional Support**: Consider consulting with a mental health professional",
                "📞 **Crisis Resources**: Know emergency mental health contacts and support lines",
                "💊 **Medical Evaluation**: Discuss symptoms with primary care physician",
                "👥 **Support System**: Engage family/friends for additional support"
            ])
        elif wellness_level == "Moderate Concerns":
            recommendations.extend([
                "🧘‍♀️ **Stress Management**: Implement daily stress reduction techniques",
                "📱 **Mental Health Apps**: Consider guided meditation or mood tracking apps",
                "🗣️ **Counseling**: Consider preventive counseling or therapy sessions"
            ])
        else:
            recommendations.extend([
                "✅ **Maintain Wellness**: Continue current positive mental health practices",
                "🎯 **Prevention Focus**: Build resilience through continued self-care"
            ])
        
        # Specific recommendations based on findings
        if sleep_quality in ["Poor", "Very poor"] or sleep_hours < 7:
            recommendations.append("😴 **Sleep Hygiene**: Establish consistent bedtime routine, limit screens before bed")
        
        if exercise_frequency in ["Rarely", "Never"]:
            recommendations.append("🏃‍♀️ **Physical Activity**: Start with 10-minute daily walks, build to 30 minutes")
        
        if anxiety_level in ["Moderate", "Severe", "Very severe"]:
            recommendations.append("🧘‍♂️ **Anxiety Management**: Practice deep breathing, mindfulness, or progressive muscle relaxation")
        
        if social_support in ["Poor", "None"]:
            recommendations.append("👥 **Social Connection**: Join groups, volunteer, or reconnect with friends/family")
        
        if mood_rating <= 4:
            recommendations.append("🌈 **Mood Enhancement**: Engage in enjoyable activities, practice gratitude, seek sunlight")
        
        if stress_level in ["High", "Very high", "Overwhelming"]:
            recommendations.append("🎯 **Stress Reduction**: Identify stressors, practice time management, set boundaries")
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
        
        # Mental health action plan
        st.markdown("""
        <div class="success-box">
            <h4>🎯 Daily Mental Health Action Plan</h4>
            <p><strong>Morning Routine:</strong></p>
            <ul>
                <li>10 minutes mindfulness or meditation</li>
                <li>Gratitude journaling (3 things)</li>
                <li>Physical movement or stretching</li>
            </ul>
            <p><strong>Throughout Day:</strong></p>
            <ul>
                <li>Regular breaks from work/stress</li>
                <li>Stay hydrated and eat nutritiously</li>
                <li>Connect with supportive people</li>
            </ul>
            <p><strong>Evening Routine:</strong></p>
            <ul>
                <li>Reflect on positive moments</li>
                <li>Limit screen time before bed</li>
                <li>Prepare for restful sleep</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Crisis resources
        if mental_score > 18:
            st.markdown("""
            <div class="warning-box">
                <h4>🆘 Mental Health Resources</h4>
                <p><strong>If you're experiencing thoughts of self-harm:</strong></p>
                <ul>
                    <li><strong>National Suicide Prevention Lifeline:</strong> 988</li>
                    <li><strong>Crisis Text Line:</strong> Text HOME to 741741</li>
                    <li><strong>Emergency:</strong> Call 911 or go to nearest emergency room</li>
                </ul>
                <p><strong>Professional Support:</strong></p>
                <ul>
                    <li>Contact your primary care physician</li>
                    <li>Seek referral to mental health professional</li>
                    <li>Consider employee assistance programs</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# Health Dashboard
elif page == "📊 Health Dashboard":
    st.header("📊 Comprehensive Health Dashboard")
    
    st.markdown("""
    <div class="info-box">
        <h4>📈 Integrated Health Monitoring</h4>
        <p>Complete health overview combining multiple assessment domains for comprehensive health tracking.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick health input form
    st.subheader("⚡ Quick Health Input")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📊 Basic Metrics**")
        age = st.number_input("Age", 18, 100, 35)
        height = st.number_input("Height (cm)", 140, 220, 170)
        weight = st.number_input("Weight (kg)", 40, 200, 70)
        sex = st.selectbox("Sex", ["Male", "Female"])
    
    with col2:
        st.markdown("**🔬 Lab Values**")
        glucose = st.number_input("Glucose (mg/dL)", 70, 300, 95)
        bp_sys = st.number_input("Systolic BP", 80, 200, 120)
        cholesterol = st.number_input("Total Cholesterol", 100, 400, 180)
        hdl = st.number_input("HDL", 20, 100, 50)
    
    with col3:
        st.markdown("**🎯 Lifestyle**")
        exercise = st.selectbox("Exercise", ["Daily", "Weekly", "Rarely", "Never"])
        smoking = st.selectbox("Smoking", ["Never", "Former", "Current"])
        stress = st.selectbox("Stress", ["Low", "Moderate", "High"])
        sleep_hrs = st.number_input("Sleep hours", 3, 12, 7)
    
    if st.button("📊 Generate Health Dashboard", use_container_width=True):
        # Calculate BMI
        bmi = weight / ((height/100) ** 2)
        
        # Quick health scores
        diabetes_risk, _ = health_assess.calculate_diabetes_risk(
            age, bmi, glucose, bp_sys, "None", exercise, "Good", 0.85
        )
        
        heart_risk, _ = health_assess.calculate_heart_risk(
            age, sex, bp_sys, 80, cholesterol, hdl, 100, smoking, "None", exercise, bmi
        )
        
        mental_score, _, _ = health_assess.assess_mental_health(
            stress, sleep_hrs, "Good", exercise, "Satisfied", "Stable", "Good"
        )
        
        # Overall health score
        overall_score = (diabetes_risk + heart_risk + mental_score) / 3
        
        # Health grade
        if overall_score <= 5:
            health_grade = "A"
            grade_color = "#28a745"
            grade_desc = "Excellent Health"
        elif overall_score <= 10:
            health_grade = "B"
            grade_color = "#17a2b8"
            grade_desc = "Good Health"
        elif overall_score <= 15:
            health_grade = "C"
            grade_color = "#ffc107"
            grade_desc = "Fair Health"
        else:
            health_grade = "D"
            grade_color = "#dc3545"
            grade_desc = "Needs Improvement"
        
        # Dashboard header
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {grade_color} 0%, {grade_color}80 100%); 
                    color: white; padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0;">
            <h1>Health Grade: {health_grade}</h1>
            <h3>{grade_desc}</h3>
            <p>Overall Health Score: {overall_score:.1f}/25</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Health metrics grid
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            bmi_status = "Normal" if 18.5 <= bmi < 25 else "Overweight" if bmi < 30 else "Obese"
            st.markdown(f"""
            <div class="metric-card">
                <h4>BMI</h4>
                <h2>{bmi:.1f}</h2>
                <p>{bmi_status}</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {min(bmi/40*100, 100)}%; 
                         background: {'#28a745' if 18.5 <= bmi < 25 else '#ffc107' if bmi < 30 else '#dc3545'};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            bp_status = "Normal" if bp_sys < 120 else "Elevated" if bp_sys < 140 else "High"
            st.markdown(f"""
            <div class="metric-card">
                <h4>Blood Pressure</h4>
                <h2>{bp_sys} mmHg</h2>
                <p>{bp_status}</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {min(bp_sys/200*100, 100)}%; 
                         background: {'#28a745' if bp_sys < 120 else '#ffc107' if bp_sys < 140 else '#dc3545'};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            glucose_status = "Normal" if glucose < 100 else "Pre-diabetic" if glucose < 126 else "High"
            st.markdown(f"""
            <div class="metric-card">
                <h4>Glucose</h4>
                <h2>{glucose} mg/dL</h2>
                <p>{glucose_status}</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {min(glucose/200*100, 100)}%; 
                         background: {'#28a745' if glucose < 100 else '#ffc107' if glucose < 126 else '#dc3545'};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            hdl_status = "Low" if hdl < 40 else "Good" if hdl < 60 else "Excellent"
            st.markdown(f"""
            <div class="metric-card">
                <h4>HDL Cholesterol</h4>
                <h2>{hdl} mg/dL</h2>
                <p>{hdl_status}</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {min(hdl/100*100, 100)}%; 
                         background: {'#dc3545' if hdl < 40 else '#ffc107' if hdl < 60 else '#28a745'};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Risk assessment summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            diabetes_level = "Low" if diabetes_risk <= 5 else "Moderate" if diabetes_risk <= 12 else "High"
            diabetes_color = "#28a745" if diabetes_risk <= 5 else "#ffc107" if diabetes_risk <= 12 else "#dc3545"
            st.markdown(f"""
            <div class="prediction-card" style="border-left-color: {diabetes_color};">
                <h4>🩺 Diabetes Risk</h4>
                <h3>{diabetes_level} Risk</h3>
                <p>Score: {diabetes_risk}/25</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {diabetes_risk/25*100}%; background: {diabetes_color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            heart_level = "Low" if heart_risk <= 8 else "Moderate" if heart_risk <= 15 else "High"
            heart_color = "#28a745" if heart_risk <= 8 else "#ffc107" if heart_risk <= 15 else "#dc3545"
            st.markdown(f"""
            <div class="prediction-card" style="border-left-color: {heart_color};">
                <h4>❤️ Heart Disease Risk</h4>
                <h3>{heart_level} Risk</h3>
                <p>Score: {heart_risk}/30</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {heart_risk/30*100}%; background: {heart_color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            mental_level = "Good" if mental_score <= 8 else "Moderate" if mental_score <= 15 else "Concerning"
            mental_color = "#28a745" if mental_score <= 8 else "#ffc107" if mental_score <= 15 else "#dc3545"
            st.markdown(f"""
            <div class="prediction-card" style="border-left-color: {mental_color};">
                <h4>🧠 Mental Health</h4>
                <h3>{mental_level}</h3>
                <p>Score: {mental_score:.1f}/25</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {mental_score/25*100}%; background: {mental_color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Lifestyle factors
        st.subheader("🎯 Lifestyle Assessment")
        
        lifestyle_score = 0
        if exercise in ["Daily", "Weekly"]: lifestyle_score += 2
        else: lifestyle_score -= 1
        
        if smoking == "Never": lifestyle_score += 2
        elif smoking == "Former": lifestyle_score += 1
        else: lifestyle_score -= 2
        
        if stress == "Low": lifestyle_score += 2
        elif stress == "Moderate": lifestyle_score += 1
        else: lifestyle_score -= 1
        
        if 7 <= sleep_hrs <= 9: lifestyle_score += 2
        elif 6 <= sleep_hrs <= 10: lifestyle_score += 1
        else: lifestyle_score -= 1
        
        lifestyle_percentage = max(0, min(100, (lifestyle_score + 5) * 10))
        
        col1, col2, col3, col4 = st.columns(4)
        
        lifestyle_factors = [
            ("🏃‍♂️ Exercise", exercise, "#28a745" if exercise in ["Daily", "Weekly"] else "#dc3545"),
            ("🚭 Smoking", smoking, "#28a745" if smoking == "Never" else "#ffc107" if smoking == "Former" else "#dc3545"),
            ("😰 Stress", stress, "#28a745" if stress == "Low" else "#ffc107" if stress == "Moderate" else "#dc3545"),
            ("😴 Sleep", f"{sleep_hrs}h", "#28a745" if 7 <= sleep_hrs <= 9 else "#ffc107" if 6 <= sleep_hrs <= 10 else "#dc3545")
        ]
        
        for i, (factor, value, color) in enumerate(lifestyle_factors):
            with [col1, col2, col3, col4][i]:
                st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid {color};">
                    <h4>{factor}</h4>
                    <h3>{value}</h3>
                </div>
                """, unsafe_allow_html=True)
        
        # Overall recommendations
        st.markdown("""
        <div class="prediction-card">
            <h3>🎯 Priority Health Actions</h3>
        </div>
        """, unsafe_allow_html=True)
        
        priority_actions = []
        
        if diabetes_risk > 12:
            priority_actions.append("🩺 **HIGH PRIORITY**: Diabetes prevention - consult healthcare provider")
        elif diabetes_risk > 5:
            priority_actions.append("🩺 **MODERATE**: Monitor glucose, improve diet and exercise")
        
        if heart_risk > 15:
            priority_actions.append("❤️ **HIGH PRIORITY**: Cardiovascular protection - medical evaluation needed")
        elif heart_risk > 8:
            priority_actions.append("❤️ **MODERATE**: Heart health improvement - lifestyle changes")
        
        if mental_score > 15:
            priority_actions.append("🧠 **HIGH PRIORITY**: Mental health support - consider professional help")
        elif mental_score > 8:
            priority_actions.append("🧠 **MODERATE**: Stress management and self-care focus")
        
        if bmi >= 30:
            priority_actions.append("⚖️ **PRIORITY**: Weight management - target BMI <25")
        
        if bp_sys >= 140:
            priority_actions.append("🩺 **PRIORITY**: Blood pressure control - medical consultation")
        
        if not priority_actions:
            priority_actions.append("✅ **MAINTAIN**: Continue excellent health practices")
        
        for action in priority_actions:
            st.markdown(action)
        
        # Health tracking recommendations
        st.markdown("""
        <div class="success-box">
            <h4>📱 Recommended Health Tracking</h4>
            <p><strong>Daily Monitoring:</strong></p>
            <ul>
                <li>Weight and BMI</li>
                <li>Blood pressure (if elevated)</li>
                <li>Physical activity minutes</li>
                <li>Sleep hours and quality</li>
                <li>Mood and stress levels</li>
            </ul>
            <p><strong>Regular Check-ups:</strong></p>
            <ul>
                <li>Glucose: Every 3 years (or annually if high risk)</li>
                <li>Cholesterol: Every 5 years (or more frequently if elevated)</li>
                <li>Blood pressure: Annual (or more if elevated)</li>
                <li>Mental health: Annual assessment or as needed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Personalized Recommendations
elif page == "🎯 Personalized Recommendations":
    st.header("🎯 Personalized Health & Lifestyle Recommendations")
    
    st.markdown("""
    <div class="info-box">
        <h4>🎯 Evidence-Based Health Optimization</h4>
        <p>Get personalized, actionable recommendations based on your health profile, goals, and preferences.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User goals and preferences
    st.subheader("🎯 Your Health Goals")
    col1, col2 = st.columns(2)
    
    with col1:
        primary_goal = st.selectbox("Primary Health Goal", [
            "Lose Weight", "Gain Weight", "Build Muscle", "Improve Cardiovascular Health",
            "Prevent Diabetes", "Manage Stress", "Better Sleep", "Increase Energy",
            "General Wellness", "Disease Prevention"
        ])
        
        time_commitment = st.selectbox("Available time for health activities", [
            "Less than 30 minutes/day", "30-60 minutes/day", 
            "1-2 hours/day", "More than 2 hours/day"
        ])
        
        fitness_level = st.selectbox("Current fitness level", [
            "Beginner", "Intermediate", "Advanced", "Athletic"
        ])
    
    with col2:
        budget_preference = st.selectbox("Budget preference", [
            "Low cost/free options", "Moderate investment", "Premium options available"
        ])
        
        preferred_activities = st.multiselect("Preferred activities", [
            "Walking/Hiking", "Running", "Cycling", "Swimming", "Weight Training",
            "Yoga", "Dancing", "Sports", "Home Workouts", "Gym Classes"
        ])
        
        lifestyle_constraints = st.multiselect("Lifestyle constraints", [
            "Limited time", "Physical limitations", "Travel frequently", 
            "Work from home", "Irregular schedule", "Family obligations",
            "No equipment access", "Weather dependent"
        ])
    
    # Health preferences
    st.subheader("🥗 Nutrition & Lifestyle Preferences")
    col1, col2 = st.columns(2)
    
    with col1:
        dietary_style = st.selectbox("Dietary preference", [
            "No restrictions", "Vegetarian", "Vegan", "Keto", "Paleo", 
            "Mediterranean", "Low carb", "High protein", "Intermittent fasting"
        ])
        
        cooking_level = st.selectbox("Cooking skill/time", [
            "Minimal cooking", "Basic meals", "Intermediate cooking", "Advanced cooking"
        ])
        
        meal_prep_time = st.selectbox("Meal prep availability", [
            "No meal prep", "Weekend prep only", "Daily prep", "Extensive meal prep"
        ])
    
    with col2:
        food_allergies = st.multiselect("Food allergies/intolerances", [
            "None", "Gluten", "Dairy", "Nuts", "Shellfish", "Eggs", "Soy", "Other"
        ])
        
        supplement_interest = st.selectbox("Supplement interest", [
            "None", "Basic vitamins", "Performance supplements", "Comprehensive program"
        ])
        
        stress_triggers = st.multiselect("Main stress sources", [
            "Work", "Finances", "Relationships", "Health", "Family", 
            "Time management", "Technology", "News/Media", "Social situations"
        ])
    
    # Current health status input
    st.subheader("📊 Current Health Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_weight = st.number_input("Current weight (kg)", 40, 200, 70)
        target_weight = st.number_input("Target weight (kg)", 40, 200, 70)
        height = st.number_input("Height (cm)", 140, 220, 170)
    
    with col2:
        energy_level = st.slider("Current energy level", 1, 10, 6)
        sleep_quality = st.slider("Sleep quality", 1, 10, 6)
        stress_level = st.slider("Stress level", 1, 10, 5)
    
    with col3:
        exercise_frequency = st.selectbox("Current exercise frequency", [
            "Never", "1-2 times/week", "3-4 times/week", "5-6 times/week", "Daily"
        ])
        water_intake = st.number_input("Daily water intake (glasses)", 0, 20, 6)
        screen_time = st.number_input("Daily screen time (hours)", 0, 16, 8)
    
    if st.button("🎯 Generate Personalized Plan", use_container_width=True):
        # Calculate current BMI and target BMI
        current_bmi = current_weight / ((height/100) ** 2)
        target_bmi = target_weight / ((height/100) ** 2)
        weight_goal = target_weight - current_weight
        
        # Generate comprehensive personalized recommendations
        st.markdown("""
        <div class="prediction-card">
            <h2>🎯 Your Personalized Health Optimization Plan</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Goal-specific recommendations
        st.subheader(f"🎯 {primary_goal} Action Plan")
        
        if primary_goal == "Improve Cardiovascular Health":
            tracking_metrics.extend([
                "💗 **Heart Rate**: Resting HR weekly, exercise HR during workouts",
                "🩺 **Blood Pressure**: Weekly if elevated, monthly if normal",
                "🏃‍♀️ **Cardio Performance**: Distance, time, perceived exertion"
            ])
        
        if primary_goal == "Manage Stress":
            tracking_metrics.extend([
                "😌 **Stress Level**: Daily 1-10 rating",
                "😴 **Sleep Quality**: Hours and quality rating",
                "🧘‍♀️ **Mindfulness**: Minutes of meditation/relaxation daily"
            ])
        
        # Universal tracking metrics
        tracking_metrics.extend([
            "📱 **Health App**: Use smartphone or fitness tracker for daily metrics",
            "📝 **Journal**: Weekly reflection on progress and challenges",
            "📅 **Monthly Review**: Assess progress and adjust plan as needed"
        ])
        
        for metric in tracking_metrics:
            st.markdown(f"• {metric}")
        
        # Timeline and milestones
        st.markdown("""
        <div class="warning-box">
            <h4>⏰ Your Success Timeline</h4>
            <p><strong>Week 1-2:</strong> Habit formation, baseline establishment</p>
            <p><strong>Week 3-4:</strong> Initial improvements, routine solidification</p>
            <p><strong>Month 2:</strong> Noticeable progress, potential plan adjustments</p>
            <p><strong>Month 3:</strong> Significant results, long-term strategy development</p>
            <p><strong>Ongoing:</strong> Maintenance and continuous improvement</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Personalized tips based on constraints
        if lifestyle_constraints:
            st.markdown("""
            <div class="prediction-card">
                <h3>🎯 Solutions for Your Lifestyle Constraints</h3>
            </div>
            """, unsafe_allow_html=True)
            
            constraint_solutions = {
                "Limited time": [
                    "⏰ **Time-Efficient Workouts**: HIIT, compound exercises, active commuting",
                    "🥗 **Meal Prep**: Batch cooking on weekends, simple one-pot meals",
                    "📱 **Micro-Habits**: 5-minute movement breaks, stairs instead of elevators"
                ],
                "Physical limitations": [
                    "♿ **Adapted Exercise**: Chair exercises, water workouts, gentle yoga",
                    "🏥 **Professional Guidance**: Physical therapist or adapted fitness specialist",
                    "🎯 **Focus on Nutrition**: Greater emphasis on dietary improvements"
                ],
                "Travel frequently": [
                    "✈️ **Travel Workouts**: Bodyweight exercises, hotel gym routines",
                    "🍎 **Portable Nutrition**: Healthy snacks, meal replacement options",
                    "📱 **Apps & Videos**: Workout apps that work anywhere"
                ],
                "Irregular schedule": [
                    "🔄 **Flexible Planning**: Multiple workout time options",
                    "🥗 **Prep-Ahead Meals**: Foods that keep well, easy assembly",
                    "⏰ **Minimum Effective Dose**: Short, efficient routines"
                ],
                "No equipment access": [
                    "🏠 **Bodyweight Training**: Push-ups, squats, planks, lunges",
                    "🏃‍♀️ **Outdoor Activities**: Walking, hiking, running, park workouts",
                    "📦 **Household Items**: Water bottles as weights, stairs for cardio"
                ]
            }
            
            for constraint in lifestyle_constraints:
                if constraint in constraint_solutions:
                    st.markdown(f"**{constraint}:**")
                    for solution in constraint_solutions[constraint]:
                        st.markdown(f"• {solution}")
        
        # Success strategies
        st.markdown("""
        <div class="success-box">
            <h4>🏆 Your Success Strategies</h4>
            <p><strong>Habit Stacking:</strong> Attach new habits to existing routines</p>
            <p><strong>Environment Design:</strong> Set up your space for success</p>
            <p><strong>Social Support:</strong> Share goals with family/friends for accountability</p>
            <p><strong>Progress Celebration:</strong> Acknowledge small wins along the way</p>
            <p><strong>Flexibility:</strong> Adapt the plan as life circumstances change</p>
            <p><strong>Professional Support:</strong> Consider coaches, trainers, or healthcare providers when needed</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
           color: white; padding: 2rem; border-radius: 15px; text-align: center; margin-top: 3rem;'>
    <h3>⚠️ Important Medical Disclaimer</h3>
    <p style='font-size: 1.1em; margin-bottom: 1rem;'>
        <strong>This tool provides educational health information only.</strong><br>
        It is not a substitute for professional medical advice, diagnosis, or treatment.
    </p>
    <p style='font-size: 1em; opacity: 0.9;'>
        Always consult qualified healthcare providers for medical decisions.<br>
        In case of emergency, contact your local emergency services immediately.
    </p>
    <hr style='margin: 1.5rem 0; opacity: 0.3;'>
    <div style='display: flex; justify-content: center; align-items: center; gap: 2rem; flex-wrap: wrap;'>
        <div>
            <strong>🧑‍⚕️ AI Health Copilot</strong><br>
            <small>Professional Health Assessment Platform</small>
        </div>
        <div>
            <strong>📊 Evidence-Based</strong><br>
            <small>Clinical Guidelines & Research</small>
        </div>
        <div>
            <strong>🔒 Privacy Focused</strong><br>
            <small>No Data Storage</small>
        </div>
    </div>
    <p style='margin-top: 1rem; font-size: 0.9em; opacity: 0.8;'>
        © 2025 Advanced Health Copilot • Built with Streamlit • Made with ❤️ for better health
    </p>
</div>
""", unsafe_allow_html=True)_goal == "Lose Weight":
            calorie_deficit = abs(weight_goal) * 7700 / 90  # Assuming 3 months
            daily_deficit = calorie_deficit / 90
            
            st.markdown(f"""
            <div class="success-box">
                <h4>🎯 Weight Loss Strategy</h4>
                <p><strong>Target:</strong> Lose {abs(weight_goal):.1f} kg in 3 months</p>
                <p><strong>Weekly goal:</strong> {abs(weight_goal)/12:.1f} kg per week</p>
                <p><strong>Daily calorie deficit needed:</strong> ~{daily_deficit:.0f} calories</p>
                <p><strong>Approach:</strong> 70% nutrition, 30% exercise</p>
            </div>
            """, unsafe_allow_html=True)
            
            recommendations = [
                f"🥗 **Nutrition (70% of results)**: Create {daily_deficit*0.7:.0f} calorie deficit through portion control",
                f"🏃‍♀️ **Exercise (30% of results)**: Burn additional {daily_deficit*0.3:.0f} calories through activity",
                "⚖️ **Tracking**: Weigh yourself weekly, same day and time",
                "📊 **Progress metrics**: Body measurements, progress photos, how clothes fit",
                "🥤 **Hydration**: Drink water before meals to increase satiety"
            ]
            
        elif primary_goal == "Build Muscle":
            recommendations = [
                "💪 **Resistance Training**: 3-4 strength sessions per week, progressive overload",
                "🍖 **Protein Intake**: 1.6-2.2g per kg body weight daily",
                "📈 **Caloric Surplus**: 200-500 calories above maintenance",
                "😴 **Recovery**: 7-9 hours sleep, rest days between muscle groups",
                "📊 **Track Progress**: Strength gains, muscle measurements, progress photos"
            ]
            
        elif primary_goal == "Improve Cardiovascular Health":
            recommendations = [
                "🏃‍♀️ **Cardio Target**: 150 minutes moderate OR 75 minutes vigorous weekly",
                "💗 **Heart Rate Zones**: Train at 50-85% max heart rate",
                "🥗 **DASH Diet**: Emphasize fruits, vegetables, whole grains, lean proteins",
                "🧂 **Sodium Reduction**: Limit to <2,300mg daily (ideally <1,500mg)",
                "📊 **Monitor**: Blood pressure, resting heart rate, cholesterol levels"
            ]
            
        elif primary_goal == "Manage Stress":
            recommendations = [
                "🧘‍♀️ **Daily Mindfulness**: 10-20 minutes meditation or deep breathing",
                "📝 **Stress Journal**: Identify triggers and coping strategies",
                "🏃‍♀️ **Physical Activity**: Regular exercise as stress relief",
                "😴 **Sleep Hygiene**: Consistent bedtime routine, 7-9 hours sleep",
                "👥 **Social Support**: Maintain relationships, consider counseling if needed"
            ]
            
        elif primary_goal == "Better Sleep":
            recommendations = [
                "🕘 **Sleep Schedule**: Consistent bedtime and wake time, even weekends",
                "📱 **Digital Sunset**: No screens 1 hour before bedtime",
                "🌡️ **Sleep Environment**: Cool (65-68°F), dark, quiet bedroom",
                "☕ **Caffeine Cutoff**: No caffeine after 2 PM",
                "😴 **Sleep Routine**: Relaxing activities 30 minutes before bed"
            ]
            
        else:  # General wellness
            recommendations = [
                "🏃‍♀️ **Activity Goal**: 10,000 steps daily or 150 minutes moderate exercise weekly",
                "🥗 **Nutrition Balance**: 50% vegetables, 25% lean protein, 25% whole grains",
                "💧 **Hydration**: 8-10 glasses water daily",
                "😴 **Sleep Target**: 7-9 hours quality sleep nightly",
                "🧘‍♀️ **Stress Management**: Daily relaxation or mindfulness practice"
            ]
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
        
        # Personalized exercise plan
        st.markdown("""
        <div class="prediction-card">
            <h3>💪 Personalized Exercise Program</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Exercise recommendations based on preferences and constraints
        if time_commitment == "Less than 30 minutes/day":
            exercise_plan = [
                "🏃‍♀️ **HIIT Workouts**: 15-20 minute high-intensity sessions, 3x/week",
                "🚶‍♀️ **Active Breaks**: 5-minute movement every hour",
                "💪 **Bodyweight Circuits**: 15 minutes, no equipment needed"
            ]
        elif time_commitment == "30-60 minutes/day":
            exercise_plan = [
                "🏃‍♀️ **Cardio**: 30 minutes, 3-4x/week (walking, cycling, swimming)",
                "💪 **Strength Training**: 30 minutes, 2-3x/week",
                "🧘‍♀️ **Flexibility**: 15 minutes daily stretching or yoga"
            ]
        else:
            exercise_plan = [
                "🏃‍♀️ **Cardio**: 45-60 minutes, 4-5x/week",
                "💪 **Strength Training**: 45 minutes, 3-4x/week",
                "🧘‍♀️ **Recovery**: Yoga, stretching, or mobility work",
                "🎯 **Sport/Activity**: Pursue preferred activities for enjoyment"
            ]
        
        # Adapt based on fitness level
        if fitness_level == "Beginner":
            exercise_plan.append("📈 **Progression**: Start slow, increase intensity by 10% weekly")
        elif fitness_level == "Advanced":
            exercise_plan.append("🎯 **Advanced Training**: Periodization, sport-specific training")
        
        for plan in exercise_plan:
            st.markdown(f"• {plan}")
        
        # Personalized nutrition plan
        st.markdown("""
        <div class="prediction-card">
            <h3>🥗 Personalized Nutrition Strategy</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate nutritional needs
        if current_weight <= target_weight:  # Maintenance or gain
            calorie_target = int(current_weight * 24 + 500)  # Rough estimate
        else:  # Weight loss
            calorie_target = int(current_weight * 22)  # Deficit
        
        protein_target = int(current_weight * 1.8)  # grams
        
        st.markdown(f"""
        <div class="info-box">
            <h4>📊 Your Nutrition Targets</h4>
            <p><strong>Daily Calories:</strong> ~{calorie_target}</p>
            <p><strong>Protein:</strong> {protein_target}g daily</p>
            <p><strong>Hydration:</strong> {int(current_weight * 35)}ml water daily</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Diet-specific recommendations
        if dietary_style == "Vegetarian":
            nutrition_plan = [
                "🌱 **Protein Sources**: Legumes, quinoa, tofu, tempeh, eggs, dairy",
                "🥬 **Iron Absorption**: Combine iron-rich foods with vitamin C",
                "💊 **B12 Supplement**: Essential for vegetarians",
                "🥜 **Healthy Fats**: Nuts, seeds, avocado, olive oil"
            ]
        elif dietary_style == "Keto":
            nutrition_plan = [
                "🥓 **Macros**: 70% fat, 25% protein, 5% carbs",
                "🥬 **Vegetables**: Focus on low-carb leafy greens",
                "💧 **Electrolytes**: Increase sodium, potassium, magnesium",
                "📊 **Ketone Tracking**: Monitor ketosis status"
            ]
        elif dietary_style == "Mediterranean":
            nutrition_plan = [
                "🫒 **Olive Oil**: Primary fat source for cooking and dressing",
                "🐟 **Fish**: 2-3 servings weekly, especially fatty fish",
                "🥜 **Nuts & Seeds**: Daily handful as snacks",
                "🍷 **Red Wine**: Optional, 1 glass with dinner if desired"
            ]
        else:  # General healthy eating
            nutrition_plan = [
                "🥗 **Plate Method**: 50% vegetables, 25% lean protein, 25% whole grains",
                "🍎 **Whole Foods**: Minimize processed foods, choose natural options",
                "⏰ **Meal Timing**: 3 meals + 1-2 snacks, avoid late-night eating",
                "🥤 **Beverages**: Water first, limit sugary drinks"
            ]
        
        for plan in nutrition_plan:
            st.markdown(f"• {plan}")
        
        # Lifestyle optimization
        st.markdown("""
        <div class="prediction-card">
            <h3>🌟 Lifestyle Optimization</h3>
        </div>
        """, unsafe_allow_html=True)
        
        lifestyle_recommendations = []
        
        if energy_level < 6:
            lifestyle_recommendations.extend([
                "⚡ **Energy Boost**: Check for iron deficiency, optimize sleep schedule",
                "☕ **Strategic Caffeine**: Morning only, avoid afternoon crashes",
                "🍎 **Blood Sugar**: Eat balanced meals to maintain steady energy"
            ])
        
        if sleep_quality < 6:
            lifestyle_recommendations.extend([
                "😴 **Sleep Hygiene**: Dark, cool room, consistent schedule",
                "📱 **Digital Detox**: No screens 1 hour before bedtime",
                "🛏️ **Sleep Environment**: Comfortable mattress and pillows"
            ])
        
        if stress_level > 6:
            lifestyle_recommendations.extend([
                "🧘‍♀️ **Stress Reduction**: Daily meditation or mindfulness practice",
                "📝 **Stress Management**: Identify triggers, develop coping strategies",
                "👥 **Social Support**: Maintain relationships, seek help when needed"
            ])
        
        if screen_time > 10:
            lifestyle_recommendations.extend([
                "📱 **Screen Time Limits**: Set daily limits, use blue light filters",
                "👀 **Eye Health**: 20-20-20 rule (every 20 min, look 20 feet away for 20 sec)",
                "🚶‍♀️ **Active Breaks**: Move every hour to counteract sitting"
            ])
        
        if water_intake < 8:
            lifestyle_recommendations.extend([
                "💧 **Hydration Strategy**: Drink glass of water with each meal",
                "📱 **Hydration Apps**: Use reminders to increase water intake",
                "🍋 **Flavor Enhancement**: Add lemon, cucumber, or mint to water"
            ])
        
        for rec in lifestyle_recommendations:
            st.markdown(f"• {rec}")
        
        # Progress tracking plan
        st.markdown("""
        <div class="prediction-card">
            <h3>📊 Progress Tracking Plan</h3>
        </div>
        """, unsafe_allow_html=True)
        
        tracking_metrics = []
        
        if primary_goal in ["Lose Weight", "Gain Weight"]:
            tracking_metrics.extend([
                "⚖️ **Weight**: Weekly, same day/time",
                "📏 **Measurements**: Waist, hips, arms (monthly)",
                "📸 **Progress Photos**: Monthly, same lighting/pose"
            ])
        
        if primary_goal == "Build Muscle":
            tracking_metrics.extend([
                "💪 **Strength**: Track weights/reps for key exercises",
                "📏 **Muscle Measurements**: Arms, chest, thighs monthly",
                "🏋️‍♀️ **Workout Performance**: Energy, endurance, recovery"
            ])
        
# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>⚠️ <strong>Disclaimer:</strong> For educational purposes only. Not medical advice.</p>
    <p>🤖 Powered by streamlit | © 2025 AI Health Copilot</p>
</div>
""", unsafe_allow_html=True)
