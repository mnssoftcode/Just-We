# 🌿 CalmSpace - Mental Health AI Assistant

A free, empathetic chatbot web app designed to provide supportive mental health conversations with AI-generated responses, safety layers, and resource recommendations.

## 🚀 Features

### ✅ Phase 1: Base Chatbot with OpenAI Integration
- **Beautiful Mobile-Friendly UI**: Modern chat interface with smooth animations
- **OpenAI GPT-3.5 Integration**: Intelligent, empathetic responses
- **Real-time Chat**: Instant messaging with typing indicators
- **Responsive Design**: Works perfectly on mobile and desktop

### ✅ Phase 2: Crisis Detection & Emotion Analysis
- **Crisis Detection**: Identifies high-risk messages and provides immediate help
- **Emotion Detection**: Analyzes user emotions (anxious, sad, angry, stressed, lonely)
- **Safety Protocols**: Automatic crisis response with emergency resources
- **Emotion-Based Responses**: Tailored responses based on detected emotional state

### 🔄 Phase 3: Dataset Integration (Ready for Implementation)
- **Mental Health Dataset**: Ready to integrate with MentalChat16K or similar datasets
- **Fallback Responses**: Comprehensive fallback system when OpenAI is unavailable
- **Context Enhancement**: Dataset-driven response improvements

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI**: OpenAI GPT-3.5-turbo
- **Emotion Detection**: Keyword-based with ML-ready architecture
- **Crisis Detection**: Advanced keyword matching with regex patterns
- **Styling**: Modern CSS with gradients and animations

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd mental-health-chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Copy the environment template and add your API keys:
```bash
cp env_template.txt .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### 4. Run the Application
```bash
cd backend
python app.py
```

The app will be available at `http://localhost:5000`

## 🎯 Key Features

### 🧠 Mental Health Focus
- **Empathetic Responses**: AI trained specifically for mental health conversations
- **No Medical Advice**: Clear disclaimers and appropriate referrals
- **Supportive Tone**: Warm, kind, and non-judgmental communication

### 🚨 Safety Features
- **Crisis Detection**: Monitors for high-risk keywords and phrases
- **Emergency Resources**: Immediate access to crisis hotlines
- **Escalation Protocol**: Automatic crisis response system

### 💙 Emotion Intelligence
- **Real-time Analysis**: Detects user emotions from message content
- **Tailored Responses**: Adjusts communication style based on emotional state
- **Coping Suggestions**: Provides emotion-specific coping strategies

### 📱 User Experience
- **Mobile-First Design**: Optimized for mobile devices
- **Smooth Animations**: Professional chat interface with typing indicators
- **Resource Access**: Easy access to mental health resources
- **Privacy-Focused**: No login required, localStorage for conversation history

## 🔧 API Endpoints

### POST `/api/chat`
Send a message and receive an AI response.

**Request:**
```json
{
  "message": "I'm feeling really anxious today",
  "history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How are you feeling today?"}
  ]
}
```

**Response:**
```json
{
  "message": "I can sense you're feeling anxious right now...",
  "crisis_detected": false,
  "crisis_level": "low",
  "emotion": "anxious",
  "timestamp": "2024-01-01T12:00:00"
}
```

### GET `/api/health`
Health check endpoint.

### GET `/api/resources`
Get mental health resources and crisis hotlines.

## 🚨 Crisis Detection

The system monitors for:
- **High Crisis**: Immediate intervention needed (suicidal thoughts, self-harm)
- **Medium Crisis**: Concerning but not immediate (hopelessness, worthlessness)
- **Low Crisis**: Normal conversation

### Crisis Response Protocol
1. **Detection**: Keyword and pattern matching
2. **Assessment**: Crisis level determination
3. **Response**: Appropriate crisis response with resources
4. **Resources**: Emergency hotlines and professional help

## 🎨 UI Features

- **Modern Design**: Gradient backgrounds and smooth animations
- **Mobile Responsive**: Perfect on all device sizes
- **Dark/Light Mode**: Automatic theme detection
- **Typing Indicators**: Real-time feedback
- **Crisis Alerts**: Visual indicators for crisis messages
- **Resource Modal**: Easy access to mental health resources

## 🔒 Privacy & Security

- **No User Accounts**: No login required
- **Local Storage**: Conversations stored locally only
- **No Data Collection**: No personal information collected
- **Secure API**: HTTPS recommended for production

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set up environment variables
2. Use a production WSGI server (Gunicorn)
3. Configure reverse proxy (Nginx)
4. Enable HTTPS

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 📊 Future Enhancements

### Phase 3 Implementation
- [ ] Integrate MentalChat16K dataset
- [ ] Train custom emotion detection models
- [ ] Implement conversation memory
- [ ] Add user feedback system

### Additional Features
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Integration with mental health professionals

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Important Disclaimer

**This is not a replacement for professional mental health care.** CalmSpace is designed to provide supportive conversation and resources, but it is not a substitute for professional therapy or medical treatment. If you're experiencing a mental health crisis, please contact emergency services or a mental health professional immediately.

## 🆘 Crisis Resources

- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: 911

---

**Built with ❤️ for mental health support** # Just-We
