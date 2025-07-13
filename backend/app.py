import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, render_template, send_from_directory
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

app = Flask(__name__, static_folder='static')
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize our enhanced handlers
openai_handler = OpenAIHandler()
crisis_filter = CrisisFilter()
emotion_detector = EmotionDetector()


@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/manifest.json')
def manifest():
    """Serve the PWA manifest"""
    return send_from_directory('static', 'manifest.json')

@app.route('/sw.js')
def service_worker():
    """Serve the service worker"""
    return send_from_directory('static', 'sw.js')

@app.route('/icon-<size>.png')
def icon(size):
    """Serve PWA icons"""
    return send_from_directory('static', f'icon-{size}.png')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages with enhanced mental health support"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        conversation_history = data.get('history', [])
        user_id = data.get('user_id', 'default_user')  # For conversation memory
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Log the incoming message (without sensitive data)
        logger.info(f"Received message from user {user_id} at {datetime.now()}")
        
        # Enhanced Phase 1: Crisis Detection with multi-level assessment
        crisis_data = crisis_filter.detect_crisis(user_message)
        logger.info(f"Detected crisis level: {crisis_data['level']} (confidence: {crisis_data['confidence']:.2f})")
        
        # Handle immediate crisis situations
        if crisis_data['level'] in ['immediate', 'high']:
            crisis_response = crisis_filter.get_crisis_response(crisis_data)
            response = {
                'message': crisis_response,
                'crisis_detected': True,
                'crisis_level': crisis_data['level'],
                'crisis_confidence': crisis_data['confidence'],
                'crisis_indicators': crisis_data['indicators'],
                'escalation_needed': crisis_data['escalation_needed'],
                'crisis_trend': crisis_data['trend'],
                'crisis_resources': crisis_data['resources'],
                'emotion': 'crisis',
                'timestamp': datetime.now().isoformat(),
                'response_source': 'crisis_protocol'
            }
            logger.warning(f"{crisis_data['level'].upper()} crisis detected for user {user_id}")
            return jsonify(response)
        
        # Enhanced Phase 2: Emotion Detection with multi-label classification
        emotion_data = emotion_detector.detect_emotion(user_message)
        logger.info(f"Detected emotion: {emotion_data['primary_emotion']} ({emotion_data['intensity']} intensity, confidence: {emotion_data['confidence']:.2f})")
        
        # Enhanced Phase 3: Response Generation with quality scoring
        try:
            # Prepare enhanced conversation context
            context = openai_handler.prepare_context(user_message, conversation_history, emotion_data, crisis_data)
            
            # Get enhanced response with quality scoring
            response_data = openai_handler.get_response(context, emotion_data, crisis_data)
            
            # Update conversation memory
            openai_handler.update_conversation_memory(user_id, user_message, response_data['response'], emotion_data, crisis_data)
            
            # Get conversation summary
            conversation_summary = openai_handler.get_conversation_summary(user_id)
            
            response = {
                'message': response_data['response'],
                'crisis_detected': False,
                'crisis_level': crisis_data['level'],
                'crisis_confidence': crisis_data['confidence'],
                'crisis_indicators': crisis_data['indicators'],
                'escalation_needed': crisis_data['escalation_needed'],
                'crisis_trend': crisis_data['trend'],
                'emotion': emotion_data['primary_emotion'],
                'emotion_intensity': emotion_data['intensity'],
                'emotion_confidence': emotion_data['confidence'],
                'emotion_trend': emotion_data['emotion_trend'],
                'all_emotions': emotion_data['all_emotions'],
                'response_source': response_data['source'],
                'response_quality_score': response_data['quality_score'],
                'emotion_appropriate': response_data['emotion_appropriate'],
                'crisis_appropriate': response_data['crisis_appropriate'],
                'conversation_summary': conversation_summary,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Enhanced response generation error: {str(e)}")
            # Enhanced fallback response
            fallback_response = openai_handler.get_fallback_response(user_message, emotion_data, crisis_data)
            response = {
                'message': fallback_response,
                'crisis_detected': False,
                'crisis_level': crisis_data['level'],
                'crisis_confidence': crisis_data['confidence'],
                'emotion': emotion_data['primary_emotion'],
                'emotion_intensity': emotion_data['intensity'],
                'emotion_confidence': emotion_data['confidence'],
                'emotion_trend': emotion_data['emotion_trend'],
                'all_emotions': emotion_data['all_emotions'],
                'fallback': True,
                'response_source': 'fallback',
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in enhanced chat endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/emotion-analysis', methods=['POST'])
def analyze_emotion():
    """Analyze emotion in a message"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        emotion_data = emotion_detector.detect_emotion(message)
        emotion_summary = emotion_detector.get_emotion_summary()
        
        return jsonify({
            'emotion_data': emotion_data,
            'emotion_summary': emotion_summary,
            'suggestions': emotion_detector.get_emotion_suggestions(emotion_data),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in emotion analysis: {str(e)}")
        return jsonify({'error': 'Could not analyze emotion'}), 500

@app.route('/api/crisis-assessment', methods=['POST'])
def assess_crisis():
    """Assess crisis level in a message"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        crisis_data = crisis_filter.detect_crisis(message)
        crisis_summary = crisis_filter.get_crisis_summary()
        escalation_guidance = crisis_filter.get_escalation_guidance()
        
        return jsonify({
            'crisis_data': crisis_data,
            'crisis_summary': crisis_summary,
            'escalation_guidance': escalation_guidance,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in crisis assessment: {str(e)}")
        return jsonify({'error': 'Could not assess crisis level'}), 500

@app.route('/api/conversation-summary/<user_id>', methods=['GET'])
def get_conversation_summary(user_id):
    """Get conversation summary for a user"""
    try:
        summary = openai_handler.get_conversation_summary(user_id)
        return jsonify({
            'user_id': user_id,
            'summary': summary,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting conversation summary: {str(e)}")
        return jsonify({'error': 'Could not retrieve conversation summary'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Enhanced health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'features': {
            'enhanced_crisis_detection': True,
            'multi_label_emotion_detection': True,
            'enhanced_response_generation': True,
            'conversation_memory': True,
            'response_quality_scoring': True,
            'emotion_trend_analysis': True,
            'crisis_escalation_tracking': True,
            'pwa_support': True,
            'mobile_optimized': True,
            'offline_capable': True
        },
        'capabilities': {
            'emotion_intensities': ['low', 'medium', 'high'],
            'crisis_levels': ['none', 'low', 'medium', 'high', 'immediate'],
            'supported_emotions': ['anxious', 'sad', 'angry', 'stressed', 'lonely', 'happy', 'confused', 'neutral'],
            'response_sources': ['dataset', 'groq_api', 'fallback', 'crisis_protocol'],
            'pwa_features': ['installable', 'offline_support', 'push_notifications']
        }
    })

@app.route('/api/resources', methods=['GET'])
def get_resources():
    """Get enhanced mental health resources"""
    resources = {
        'crisis_hotlines': {
            'national_suicide_prevention': '988',
            'crisis_text_line': 'Text HOME to 741741',
            'emergency': '911',
            'mental_health': '1-800-273-8255'
        },
        'crisis_resources': {
            'immediate': [
                'Call 988 immediately',
                'Text HOME to 741741',
                'Call 911 if immediate danger',
                'Remove any means of self-harm',
                'Stay with the person if possible'
            ],
            'high': [
                'Call a crisis hotline',
                'Talk to a mental health professional',
                'Reach out to a trusted person',
                'Consider emergency services if needed'
            ],
            'medium': [
                'Talk to someone you trust',
                'Consider professional help',
                'Practice self-care',
                'Reach out to support networks'
            ],
            'low': [
                'Practice self-care',
                'Talk to a friend or family member',
                'Consider talking to a counselor',
                'Engage in activities you enjoy'
            ]
        },
        'coping_strategies': {
            'anxious': [
                'Deep breathing exercises',
                'Grounding techniques (5-4-3-2-1)',
                'Progressive muscle relaxation',
                'Mindfulness meditation'
            ],
            'sad': [
                'Gentle physical activity',
                'Creative expression (art, music, writing)',
                'Connecting with loved ones',
                'Practicing self-compassion'
            ],
            'stressed': [
                'Time management techniques',
                'Setting boundaries',
                'Regular exercise',
                'Adequate sleep and nutrition'
            ],
            'lonely': [
                'Reaching out to friends/family',
                'Joining community groups',
                'Volunteering',
                'Pursuing hobbies and interests'
            ]
        }
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
            'total_entries': sum(dataset['rows'] for dataset in stats.values()),
            'enhanced_features': {
                'emotion_aware_search': True,
                'similarity_threshold': 0.3,
                'fallback_threshold': 0.1
            }
        })
    except Exception as e:
        logger.error(f"Error getting dataset stats: {str(e)}")
        return jsonify({'error': 'Could not retrieve dataset statistics'}), 500

@app.route('/api/emotion-suggestions', methods=['POST'])
def get_emotion_suggestions():
    """Get coping suggestions based on emotion"""
    try:
        data = request.get_json()
        emotion_data = data.get('emotion_data', {})
        
        if not emotion_data:
            return jsonify({'error': 'Emotion data required'}), 400
        
        suggestions = emotion_detector.get_emotion_suggestions(emotion_data)
        
        return jsonify({
            'suggestions': suggestions,
            'emotion': emotion_data.get('primary_emotion', 'neutral'),
            'intensity': emotion_data.get('intensity', 'low'),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting emotion suggestions: {str(e)}")
        return jsonify({'error': 'Could not retrieve suggestions'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run(host='0.0.0.0', port=port, debug=True) 