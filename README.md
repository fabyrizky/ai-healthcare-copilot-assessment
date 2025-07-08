# 🧑‍⚕️ AI Health Copilot

A comprehensive health prediction and analysis application powered by Machine Learning and Qwen QwQ 32B AI model via OpenRouter.

## 🌟 Features

- **Diabetes Prediction**: ML-based diabetes risk assessment
- **Heart Disease Prediction**: Cardiovascular health analysis
- **Parkinson's Disease Prediction**: Neurological condition screening using voice analysis
- **Personalized Health Plans**: AI-generated diet and fitness recommendations
- **Intelligent Explanations**: Medical insights powered by Meta Llama 4 Maverick

## 🚀 Quick Deploy on Streamlit Cloud

### 1. Fork/Clone this Repository
```bash
git clone https://github.com/yourusername/ai-health-copilot.git
cd ai-health-copilot
```

### 2. Get OpenRouter API Key
1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up for a free account
3. Generate an API key
4. Copy your API key (starts with `sk-or-v1-...`)

### 3. Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Connect your GitHub account
3. Choose this repository
4. Set the main file path: `app.py`
5. **Important**: In the "Advanced settings" section, add your secrets:
   ```
   OPENROUTER_API_KEY = "sk-or-v1-your-actual-api-key-here"
   ```

### 4. Alternative Local Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create secrets file
mkdir .streamlit
echo 'OPENROUTER_API_KEY = "sk-or-v1-your-actual-api-key-here"' > .streamlit/secrets.toml

# Run the app
streamlit run app.py
```

## 📁 Project Structure

```
ai-health-copilot/
├── app.py                          # Main Streamlit application
├── requirements.txt                 # Python dependencies
├── .streamlit/
│   ├── secrets.toml                # API keys (hidden)
│   └── config.toml                 # App configuration
├── saved_models/                   # ML models (auto-generated)
│   ├── diabetes_model.sav
│   ├── heart_disease_model.sav
│   └── parkinsons_model.sav
└── README.md                       # This file
```

## 🔧 Configuration

### API Configuration
The app uses OpenRouter's Qwen QwQ 32B model. Make sure to:
1. Get a free API key from [OpenRouter](https://openrouter.ai/)
2. Add it to your `.streamlit/secrets.toml` file
3. Keep your API key secure and never commit it to public repositories

### Model Information
- **Diabetes Model**: SVM classifier trained on PIMA diabetes dataset
- **Heart Disease Model**: Logistic Regression on UCI heart disease dataset  
- **Parkinson's Model**: SVM classifier using voice measurement features

## 💡 Usage

1. **Health Predictions**: Enter your health parameters to get ML-based predictions
2. **AI Explanations**: Get detailed medical insights for each prediction
3. **Health Planning**: Generate personalized diet and fitness plans
4. **Track Results**: Monitor your health metrics over time

## ⚠️ Important Disclaimers

- This application is for **informational purposes only**
- Results are **not a substitute** for professional medical advice
- Always consult healthcare providers for medical decisions
- Predictions are based on statistical models and may not be 100% accurate

## 🛠️ Technical Details

- **Frontend**: Streamlit
- **ML Libraries**: scikit-learn, numpy, pandas
- **AI Model**: Qwen QwQ 32B via OpenRouter API
- **Deployment**: Streamlit Cloud compatible
- **Python Version**: 3.8+

## 📊 Model Performance

- **Diabetes Model**: ~77% accuracy on test data
- **Heart Disease Model**: ~82% accuracy on test data
- **Parkinson's Model**: ~87% accuracy on test data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:
1. Check that your OpenRouter API key is correctly configured
2. Ensure all requirements are installed
3. Verify your internet connection for API calls
4. Check the Streamlit Cloud logs for deployment issues

## 🔮 Future Enhancements

- [ ] Additional disease prediction models
- [ ] Health data visualization dashboard
- [ ] Integration with wearable devices
- [ ] Multi-language support
- [ ] Advanced AI health coaching
- [ ] Telemedicine features

---

**Developed by Faby Rizky using Streamlit and Meta Llama 4 Maverick**

*Pasar Rebo Public Hospital© 2025*
