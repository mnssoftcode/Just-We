import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import json
import logging
from datetime import datetime

# Import our custom modules
from openai_handler import OpenAIHandler
from utils.crisis_filter import CrisisFilter
from utils.emotion_detector import EmotionDetector

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize our handlers
openai_handler = OpenAIHandler()
crisis_filter = CrisisFilter()
emotion_detector = EmotionDetector()


@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages with mental health support"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        conversation_history = data.get('history', [])
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Log the incoming message (without sensitive data)
        logger.info(f"Received message from user at {datetime.now()}")
        
        # Phase 2: Crisis Detection
        crisis_level = crisis_filter.detect_crisis(user_message)
        
        if crisis_level == "high":
            # High crisis detected - respond with emergency protocol
            response = {
                'message': crisis_filter.get_crisis_response(),
                'crisis_detected': True,
                'crisis_level': 'high',
                'emotion': 'crisis',
                'timestamp': datetime.now().isoformat()
            }
            logger.warning(f"High crisis detected in user message")
            return jsonify(response)
        
        # Phase 2: Emotion Detection
        emotion = emotion_detector.detect_emotion(user_message)
        logger.info(f"Detected emotion: {emotion}")
        
        # Phase 1: OpenAI Integration with enhanced context
        try:
            # Prepare conversation context for OpenAI
            context = openai_handler.prepare_context(user_message, conversation_history, emotion)
            
            # Get response from OpenAI
            ai_response = openai_handler.get_response(context, emotion)
            
            # Check if response came from dataset or AI
            dataset_match = openai_handler.dataset_handler.find_best_match(user_message, emotion, threshold=0.3)
            
            response = {
                'message': ai_response,
                'crisis_detected': False,
                'crisis_level': crisis_level,
                'emotion': emotion,
                'timestamp': datetime.now().isoformat(),
                'dataset_match': dataset_match if dataset_match else None,
                'response_source': 'dataset' if dataset_match else 'ai'
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            # Fallback to dataset responses if OpenAI fails
            fallback_response = openai_handler.get_fallback_response(user_message, emotion)
            response = {
                'message': fallback_response,
                'crisis_detected': False,
                'crisis_level': crisis_level,
                'emotion': emotion,
                'timestamp': datetime.now().isoformat(),
                'fallback': True,
                'response_source': 'fallback'
            }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'features': {
            'crisis_detection': True,
            'emotion_detection': True,
            'openai_integration': True
        }
    })

@app.route('/api/resources', methods=['GET'])
def get_resources():
    """Get mental health resources"""
    resources = {
        'crisis_hotlines': {
            'national_suicide_prevention': '988',
            'crisis_text_line': 'Text HOME to 741741',
            'emergency': '911'
        },
        'mental_health_resources': [
            'Talk to a trusted friend or family member',
            'Consider speaking with a mental health professional',
            'Practice deep breathing exercises',
            'Try journaling your thoughts and feelings',
            'Take a walk in nature',
            'Practice mindfulness or meditation'
        ]
    }
    return jsonify(resources)

@app.route('/api/dataset-stats', methods=['GET'])
def get_dataset_stats():
    """Get dataset statistics"""
    try:
        stats = openai_handler.get_dataset_stats()
        return jsonify({
            'status': 'success',
            'datasets': stats,
            'total_entries': sum(dataset['rows'] for dataset in stats.values())
        })
    except Exception as e:
        logger.error(f"Error getting dataset stats: {str(e)}")
        return jsonify({'error': 'Could not retrieve dataset statistics'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run(host='0.0.0.0', port=port, debug=True) 