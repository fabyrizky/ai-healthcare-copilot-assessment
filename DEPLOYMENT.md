# 🚀 Deployment Guide - AI Health Copilot

## Quick Deploy to Streamlit Cloud (Recommended)

### Step 1: Prepare Repository
1. Fork or upload all files to your GitHub repository
2. Ensure all files are present:
   ```
   ├── app.py
   ├── requirements.txt
   ├── .streamlit/config.toml
   ├── .streamlit/secrets.example.toml
   ├── README.md
   └── .gitignore
   ```

### Step 2: Get OpenRouter API Key
1. Visit [https://openrouter.ai/](https://openrouter.ai/)
2. Sign up for free account
3. Navigate to "API Keys" 
4. Create new API key
5. Copy the key (format: `sk-or-v1-...`)

### Step 3: Deploy on Streamlit Cloud
1. Go to [https://share.streamlit.io/](https://share.streamlit.io/)
2. Click "New app"
3. Connect GitHub and select your repository
4. Set main file path: `app.py`
5. **CRITICAL**: Click "Advanced settings"
6. In the secrets section, add:
   ```toml
   OPENROUTER_API_KEY = "sk-or-v1-your-actual-api-key-here"
   ```
7. Click "Deploy"

### Step 4: Verify Deployment
- Check app loads without errors
- Verify API key connection (green checkmark in sidebar)
- Test one prediction to ensure ML models work
- Test AI explanation to verify OpenRouter connection

## Alternative Deployment Methods

### Option 1: Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Set config vars
heroku config:set OPENROUTER_API_KEY="your-api-key"

# Deploy
git push heroku main
```

### Option 2: Railway
1. Connect GitHub repository
2. Add environment variable: `OPENROUTER_API_KEY`
3. Railway will auto-deploy

### Option 3: Render
1. Connect repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `streamlit run app.py`
4. Add environment variable

## Local Development Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/ai-health-copilot.git
cd ai-health-copilot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup secrets
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
# Edit secrets.toml with your API key

# Run application
streamlit run app.py
```

## Environment Variables

Required variables for deployment:

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key | `sk-or-v1-abc123...` |

Optional variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_NAME` | AI model to use | `qwen/qwq-32b-preview` |
| `MAX_TOKENS` | Max response length | `1000` |
| `TEMPERATURE` | AI creativity level | `0.7` |

## Troubleshooting

### Common Issues

**"API key not found"**
- Verify secrets.toml contains correct API key
- Check environment variable is set correctly
- Ensure API key starts with `sk-or-v1-`

**"Model loading error"**
- Wait for initial model generation (first run)
- Check file permissions in deployment environment
- Verify scikit-learn version compatibility

**"Connection timeout"**
- Check internet connectivity
- Verify OpenRouter service status
- Try reducing request frequency

**"Deployment failed"**
- Check all required files are present
- Verify requirements.txt syntax
- Check Python version compatibility

### Performance Optimization

1. **Caching**: Models auto-cache after first load
2. **API Limits**: Free tier has rate limits
3. **Memory**: App uses ~200MB RAM typically
4. **Loading**: First prediction may take longer

### Security Considerations

1. **Never commit API keys** to version control
2. Use environment variables in production
3. Rotate API keys regularly
4. Monitor API usage for unusual activity
5. Set up rate limiting if needed

## Monitoring & Maintenance

### Health Checks
- Monitor prediction accuracy
- Check API response times
- Verify model loading success
- Monitor error rates

### Updates
- Update dependencies regularly
- Test new model versions
- Backup working configurations
- Monitor OpenRouter model updates

## Support

For deployment issues:
1. Check Streamlit Cloud logs
2. Verify all environment variables
3. Test locally first
4. Check OpenRouter dashboard
5. Review GitHub repository structure

## Advanced Configuration

### Custom Domain (Streamlit Cloud)
1. Upgrade to Streamlit Cloud Pro
2. Configure custom domain in settings
3. Update DNS records as instructed

### SSL Certificate
- Automatic on Streamlit Cloud
- Configure manually for other platforms

### Load Balancing
- Not required for typical usage
- Consider for high-traffic applications

---

**Need Help?** Check the main README.md or create an issue in the repository.
