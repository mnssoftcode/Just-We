# 🚀 CalmSpace Deployment Guide

## 📋 **Prerequisites**

1. **GROQ API Key**: Get your free API key from [https://console.groq.com/](https://console.groq.com/)
2. **GitHub Account**: Your code is already on GitHub
3. **Streamlit Cloud Account**: Free deployment platform

## 🎯 **Option 1: Deploy on Streamlit Cloud (Recommended)**

### **Step 1: Get Your GROQ API Key**
1. Go to [https://console.groq.com/](https://console.groq.com/)
2. Sign up for a free account
3. Navigate to "API Keys" section
4. Create a new API key
5. Copy the key (starts with `gsk_`)

### **Step 2: Deploy on Streamlit Cloud**
1. Go to [https://share.streamlit.io/](https://share.streamlit.io/)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `mnssoftcode/Just-We`
5. Set the main file path: `streamlit_app.py`
6. Click "Deploy"

### **Step 3: Configure API Key**
1. In your deployed app, go to the sidebar
2. Enter your GROQ API key in the "GROQ API Key" field
3. Click outside the field to save
4. Start chatting!

## 🎯 **Option 2: Deploy Backend + Frontend**

### **Step 1: Deploy Backend (Flask)**
You can deploy your Flask backend on:
- **Railway**: [https://railway.app/](https://railway.app/)
- **Render**: [https://render.com/](https://render.com/)
- **Heroku**: [https://heroku.com/](https://heroku.com/)

### **Step 2: Update Streamlit App**
Replace the URL in `streamlit_app.py`:
```python
url = "https://your-backend-url.com/api/chat"
```

### **Step 3: Deploy Streamlit**
Follow the same steps as Option 1.

## 🔧 **Local Testing**

### **Step 1: Install Dependencies**
```bash
pip install -r streamlit_requirements.txt
```

### **Step 2: Run Locally**
```bash
streamlit run streamlit_app.py
```

### **Step 3: Test**
1. Open [http://localhost:8501](http://localhost:8501)
2. Add your GROQ API key
3. Start chatting!

## 🔑 **API Key Security**

### **For Production:**
1. Use environment variables
2. Never commit API keys to Git
3. Use Streamlit's secrets management

### **For Development:**
1. Use the sidebar input (as implemented)
2. Key is stored in session state only
3. Refreshes when you restart the app

## 📊 **Features Available**

✅ **Emotion Detection**: Detects 6 emotions  
✅ **Crisis Detection**: Identifies dangerous messages  
✅ **Fast Responses**: Dataset-based instant replies  
✅ **Beautiful UI**: Soft blue theme  
✅ **Mobile Friendly**: Works on all devices  
✅ **Resource Access**: Crisis hotlines in sidebar  

## 🚨 **Important Notes**

1. **API Costs**: GROQ is very affordable (~$0.10 per 1M tokens)
2. **Privacy**: No data is stored permanently
3. **Crisis Support**: Always direct to professional help
4. **Limitations**: Not a replacement for professional therapy

## 🆘 **Troubleshooting**

### **Common Issues:**
1. **API Key Error**: Make sure you copied the full key
2. **Slow Responses**: Check your internet connection
3. **Deployment Failed**: Check the logs in Streamlit Cloud

### **Get Help:**
- Check the Streamlit documentation
- Review the GROQ API documentation
- Contact support if needed

## 🎉 **Success!**

Once deployed, your mental health chatbot will be available at:
`https://your-app-name.streamlit.app`

Share the link with others who might benefit from mental health support! 