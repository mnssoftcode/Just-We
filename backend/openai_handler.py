import requests
import os
import json
import random
from typing import List, Dict, Optional
import sys
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.dataset_handler import DatasetHandler
from datetime import datetime

class OpenAIHandler:
    def __init__(self):
        """Initialize enhanced GROQ handler with mental health focus and Fast Chatbot Strategy"""
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ API key not found in environment variables")
        
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Initialize dataset handler for Fast Chatbot Strategy
        self.dataset_handler = DatasetHandler()
        
        # Enhanced mental health system prompt
        self.system_prompt = """
You are \"Just We,\" a supportive, empathetic mental health assistant. Always sound human, warm, and natural (never robotic). Keep responses short and concise (1-3 sentences max). Use relevant emojis in every response (1-2 per message, placed naturally). Respond as a supportive, friendly human. Keep replies short (1-3 sentences), use emojis, and sound natural.

Your enhanced capabilities include:
- Emotion-Aware Responses: Adapt your tone and approach based on the user's emotional state
- Crisis Intervention: Recognize crisis situations and provide appropriate resources
- Personalized Support: Tailor responses to individual needs and preferences
- Multi-Turn Memory: Remember context from previous messages in the conversation
- Response Quality: Ensure responses are helpful, supportive, and appropriate

Your role is to:
- Listen actively and non-judgmentally
- Ask gentle, open-ended questions that encourage reflection
- Offer grounding exercises and coping strategies
- Provide emotional validation and support
- Recommend professional help when appropriate
- Maintain consistent, caring presence throughout conversations

Response Guidelines:
- For Crisis Situations: Provide immediate resources and encourage professional help
- For High Emotion: Offer immediate grounding and support
- For Moderate Distress: Provide coping strategies and validation
- For Positive Emotions: Celebrate and encourage continued positive activities
- For Neutral States: Maintain supportive presence and gentle engagement

Tone Guidelines:
- Warm, kind, and reassuring
- Never robotic or overly cheerful
- Respectful and non-judgmental
- Adapt tone to match user's emotional intensity
- Use simple, clear language

Always end your response with a gentle invitation to continue the conversation.
"""
        
        # Enhanced fallback responses with emotion-specific variations
        self.fallback_responses = {
            'anxious': {
                'high': [
                    "I can sense you're experiencing intense anxiety right now. Let's take a moment together - try taking three deep breaths with me. Inhale slowly for 4 counts, hold for 4, then exhale for 4. How does that feel?",
                    "Your anxiety is really intense right now, and that's completely okay. Sometimes the simple act of being heard can help. Would you like to share what's making you feel this way?",
                    "I hear how overwhelming this anxiety feels. Have you tried any grounding techniques? One simple one is to name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste."
                ],
                'medium': [
                    "I can sense you're feeling anxious right now. That's completely okay. Let's take a moment together - try taking three deep breaths with me. Inhale slowly for 4 counts, hold for 4, then exhale for 4. How does that feel?",
                    "Anxiety can be really overwhelming. Remember, it's okay to feel this way. Sometimes talking about what's on your mind can help. Would you like to share what's making you feel anxious?",
                    "I hear you're feeling anxious. That's a really tough feeling to sit with. Have you tried any grounding techniques? One simple one is to name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste."
                ],
                'low': [
                    "I notice you're feeling a bit anxious. That's completely normal. Sometimes just talking about what's on your mind can help. Would you like to share?",
                    "It's okay to feel anxious sometimes. Taking a few deep breaths can help. How are you feeling right now?",
                    "I'm here to listen if you want to talk about what's making you feel anxious."
                ]
            },
            'sad': {
                'high': [
                    "I'm so sorry you're feeling this deeply sad right now. Your feelings are completely valid, and it's okay to not be okay. Sometimes just acknowledging how we feel can be the first step. Would you like to talk about what's on your mind?",
                    "This sadness feels really heavy for you right now. Remember that you're not alone in feeling this way. Sometimes the simple act of expressing our feelings can help lighten the load a little. I'm here to listen.",
                    "It sounds like you're going through a really difficult time. Your feelings matter, and it's okay to take time to process them. Sometimes talking to someone we trust can help. Is there someone in your life you feel comfortable reaching out to?"
                ],
                'medium': [
                    "I'm so sorry you're feeling sad right now. Your feelings are valid, and it's okay to not be okay. Sometimes just acknowledging how we feel can be the first step toward feeling better. Would you like to talk about what's on your mind?",
                    "Sadness can feel really heavy and isolating. Remember that you're not alone in feeling this way. Sometimes the simple act of expressing our feelings can help lighten the load a little. I'm here to listen.",
                    "It sounds like you're going through a really difficult time. Your feelings matter, and it's okay to take time to process them. Sometimes talking to someone we trust can help. Is there someone in your life you feel comfortable reaching out to?"
                ],
                'low': [
                    "It's okay to feel sad sometimes. Your feelings are valid. Would you like to talk about what's on your mind?",
                    "I'm here to listen if you want to share what's making you feel this way.",
                    "Sometimes just talking about our feelings can help. I'm here to listen."
                ]
            },
            'angry': {
                'high': [
                    "I can hear how intense this anger feels for you right now. It's completely okay to feel angry - it's a normal emotion. Sometimes taking a moment to breathe can help. Would you like to talk about what's making you feel this way?",
                    "Your anger is really strong right now, and that's okay. Sometimes finding healthy ways to express anger can help. Would you like to talk about what's going on?",
                    "I hear how frustrated and angry you're feeling. It's okay to feel this way. Sometimes talking about what's bothering us can help us process these feelings."
                ],
                'medium': [
                    "I can hear how angry and frustrated you're feeling. It's completely okay to feel this way. Sometimes taking a moment to breathe can help. Would you like to talk about what's making you feel this way?",
                    "Your anger is valid, and it's okay to feel this way. Sometimes finding healthy ways to express anger can help. Would you like to talk about what's going on?",
                    "I hear how frustrated you're feeling. It's okay to feel this way. Sometimes talking about what's bothering us can help us process these feelings."
                ],
                'low': [
                    "It's okay to feel irritated or frustrated. Would you like to talk about what's bothering you?",
                    "I'm here to listen if you want to share what's making you feel this way.",
                    "Sometimes talking about our frustrations can help. I'm here to listen."
                ]
            },
            'stressed': {
                'high': [
                    "I can hear how overwhelmed and stressed you're feeling. That's completely understandable. Sometimes breaking things down into smaller steps can help. What's one small thing you could do right now that might help you feel a little better?",
                    "Stress can feel really overwhelming, like everything is piling up at once. It's okay to feel this way. Sometimes the best thing we can do is give ourselves permission to take a break. Even just a few minutes of deep breathing can help reset our nervous system.",
                    "You're dealing with a lot right now, and that stress is completely valid. Remember that it's okay to ask for help and to take things one step at a time. What's one thing that usually helps you feel more grounded when you're stressed?"
                ],
                'medium': [
                    "Stress can feel really overwhelming, like everything is piling up at once. It's okay to feel this way. Sometimes breaking things down into smaller steps can help. What's one small thing you could do right now that might help you feel a little better?",
                    "I can hear how stressed you're feeling. That's completely understandable. Sometimes the best thing we can do is give ourselves permission to take a break. Even just a few minutes of deep breathing can help reset our nervous system.",
                    "Stress can make everything feel more difficult than it needs to be. Remember that it's okay to ask for help and to take things one step at a time. What's one thing that usually helps you feel more grounded when you're stressed?"
                ],
                'low': [
                    "It's normal to feel stressed sometimes. Would you like to talk about what's on your mind?",
                    "I'm here to listen if you want to share what's stressing you.",
                    "Sometimes talking about our stress can help us feel better. I'm here to listen."
                ]
            },
            'lonely': {
                'high': [
                    "Loneliness can be one of the hardest feelings to sit with, especially when it feels so intense. It's completely normal to feel this way, and your feelings are valid. Sometimes reaching out to someone we trust, even just to say hello, can help. Is there someone you could reach out to?",
                    "I hear how deeply lonely you're feeling right now. That's a really difficult place to be. Remember that you're not alone in feeling this way - many people experience loneliness, even when surrounded by others. Sometimes joining a community or group activity can help. What interests you?",
                    "Loneliness can feel really isolating and overwhelming. It's okay to feel this way. Sometimes the simple act of being heard can help us feel less alone. I'm here to listen, and I want you to know that your feelings matter."
                ],
                'medium': [
                    "Loneliness can be one of the hardest feelings to sit with. It's completely normal to feel this way, and your feelings are valid. Sometimes reaching out to someone we trust, even just to say hello, can help. Is there someone you could reach out to?",
                    "I hear how lonely you're feeling right now. That's a really difficult place to be. Remember that you're not alone in feeling this way - many people experience loneliness, even when surrounded by others. Sometimes joining a community or group activity can help. What interests you?",
                    "Loneliness can feel really isolating. It's okay to feel this way. Sometimes the simple act of being heard can help us feel less alone. I'm here to listen, and I want you to know that your feelings matter."
                ],
                'low': [
                    "It's okay to feel lonely sometimes. Would you like to talk about what's on your mind?",
                    "I'm here to listen if you want to share what's making you feel this way.",
                    "Sometimes talking about our feelings can help. I'm here to listen."
                ]
            },
            'happy': {
                'high': [
                    "I'm so glad you're feeling this happy! It's wonderful to see you in such a positive state. What's contributing to this good feeling?",
                    "Your joy is contagious! It's great to see you feeling so positive. How can we build on this good energy?",
                    "This happiness sounds really wonderful! What's making you feel this way? I'd love to hear more about it."
                ],
                'medium': [
                    "It's great to see you in a positive mood! What's contributing to this good feeling?",
                    "I'm glad you're feeling good. How can we build on this positive energy?",
                    "It's wonderful to see you feeling positive. What's on your mind?"
                ],
                'low': [
                    "It's good to see you feeling okay. How are things going?",
                    "I'm glad you're doing alright. What's on your mind?",
                    "It's nice to see you in a good mood. How can I support you today?"
                ]
            },
            'confused': {
                'high': [
                    "I can hear how confused and uncertain you're feeling right now. That's completely okay - sometimes things can feel really unclear. Would you like to talk through what's on your mind? Sometimes just talking about our thoughts can help clarify them.",
                    "It sounds like you're feeling really uncertain about things right now. That's a difficult place to be. Sometimes taking time to sit with our feelings without judgment can help. What's on your mind?",
                    "Confusion can feel really overwhelming when it's this intense. Remember that it's okay to not have all the answers right now. Sometimes talking to someone we trust can help us sort through our thoughts."
                ],
                'medium': [
                    "I can hear how confused and uncertain you're feeling. That's completely okay - sometimes things can feel really unclear. Would you like to talk through what's on your mind? Sometimes just talking about our thoughts can help clarify them.",
                    "It sounds like you're feeling uncertain about things right now. That's a difficult place to be. Sometimes taking time to sit with our feelings without judgment can help. What's on your mind?",
                    "Confusion can feel really overwhelming. Remember that it's okay to not have all the answers right now. Sometimes talking to someone we trust can help us sort through our thoughts."
                ],
                'low': [
                    "It's okay to feel uncertain sometimes. Would you like to talk about what's on your mind?",
                    "I'm here to listen if you want to share what's making you feel this way.",
                    "Sometimes talking through our thoughts can help clarify them. I'm here to listen."
                ]
            },
            'default': [
                "I'm here to listen and support you. Sometimes just talking about what's on our minds can help us feel a little better. Would you like to share what's going on?",
                "I hear you, and I want you to know that your feelings are valid. It's okay to not be okay sometimes. I'm here to listen whenever you're ready to talk.",
                "Thank you for reaching out. Sometimes the bravest thing we can do is ask for support. I'm here to listen and support you however I can."
            ]
        }

        # Conversation memory for multi-turn context
        self.conversation_memory = {}
        self.max_memory_length = 20

    def prepare_context(self, user_message: str, conversation_history: List[Dict], emotion_data: Dict, crisis_data: Dict) -> List[Dict]:
        """Prepare enhanced conversation context for GROQ API"""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add emotion-specific context
        if emotion_data['primary_emotion'] != 'neutral':
            emotion_context = self._build_emotion_context(emotion_data)
            messages.append({"role": "system", "content": emotion_context})
        
        # Add crisis-specific context if needed
        if crisis_data['level'] != 'none':
            crisis_context = self._build_crisis_context(crisis_data)
            messages.append({"role": "system", "content": crisis_context})
        
        # Add conversation history with enhanced context
        enhanced_history = self._enhance_conversation_history(conversation_history, emotion_data)
        for msg in enhanced_history[-10:]:
            if msg.get('role') and msg.get('content'):
                messages.append({"role": msg['role'], "content": msg['content']})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return messages

    def _build_emotion_context(self, emotion_data: Dict) -> str:
        """Build detailed emotion context for AI response"""
        emotion = emotion_data['primary_emotion']
        intensity = emotion_data['intensity']
        trend = emotion_data.get('emotion_trend', 'stable')
        confidence = emotion_data.get('confidence', 0.0)
        
        context = f"EMOTION CONTEXT: The user appears to be feeling {emotion} with {intensity} intensity (confidence: {confidence:.2f}). "
        
        if trend == 'improving':
            context += "Their emotional state appears to be improving. "
        elif trend == 'declining':
            context += "Their emotional state appears to be declining and may need increased support. "
        
        # Add emotion-specific guidance
        emotion_guidance = {
            'anxious': f"Focus on grounding techniques, breathing exercises, and reassurance. Offer immediate support for {intensity} anxiety.",
            'sad': f"Offer comfort, validation, and gentle encouragement. Provide support appropriate for {intensity} sadness.",
            'angry': f"Acknowledge their feelings and help them find healthy ways to express anger. Address {intensity} anger appropriately.",
            'stressed': f"Help them break things down and find coping strategies. Provide support for {intensity} stress.",
            'lonely': f"Offer connection and suggest reaching out to others. Address {intensity} loneliness with appropriate support.",
            'happy': f"Celebrate their positive emotions and encourage continued positive activities. Support their {intensity} positive state.",
            'confused': f"Help them clarify their thoughts and feelings. Provide guidance for {intensity} confusion."
        }
        
        context += emotion_guidance.get(emotion, "Provide appropriate support for their emotional state.")
        
        return context

    def _build_crisis_context(self, crisis_data: Dict) -> str:
        """Build crisis context for AI response"""
        level = crisis_data['level']
        trend = crisis_data.get('trend', 'stable')
        escalation_needed = crisis_data.get('escalation_needed', False)
        
        context = f"CRISIS CONTEXT: User shows {level} crisis indicators. "
        
        if escalation_needed:
            context += "IMMEDIATE ESCALATION NEEDED. "
        
        if trend == 'escalating':
            context += "Crisis level appears to be escalating. "
        elif trend == 'improving':
            context += "Crisis level appears to be improving. "
        
        # Add crisis-specific guidance
        crisis_guidance = {
            'immediate': "Provide immediate crisis resources and encourage professional help. Stay calm and supportive.",
            'high': "Provide crisis resources and encourage professional help. Offer immediate support.",
            'medium': "Offer support and suggest professional help if needed. Monitor for escalation.",
            'low': "Provide gentle support and monitor for changes."
        }
        
        context += crisis_guidance.get(level, "Provide appropriate support.")
        
        return context

    def _enhance_conversation_history(self, conversation_history: List[Dict], emotion_data: Dict) -> List[Dict]:
        """Enhance conversation history with emotion context"""
        enhanced_history = []
        
        for msg in conversation_history:
            if msg.get('role') and msg.get('content'):
                # Add emotion context to user messages if available
                if msg['role'] == 'user' and emotion_data['primary_emotion'] != 'neutral':
                    enhanced_content = f"[User appears {emotion_data['primary_emotion']} with {emotion_data['intensity']} intensity] {msg['content']}"
                    enhanced_history.append({"role": msg['role'], "content": enhanced_content})
                else:
                    enhanced_history.append(msg)
        
        return enhanced_history

    def get_response(self, messages: List[Dict], emotion_data: Dict = None, crisis_data: Dict = None) -> Dict[str, any]:
        """Get enhanced response using Fast Chatbot Strategy with quality scoring"""
        user_message = messages[-1]['content']
        
        # Step 1: Search datasets for close match (FAST)
        dataset_match = self.dataset_handler.find_best_match(user_message, emotion_data['primary_emotion'] if emotion_data else None, threshold=0.3)
        
        if dataset_match:
            print(f"✅ Found dataset match: {dataset_match['source']} (score: {dataset_match['similarity_score']:.3f})")
            response_data = {
                'response': dataset_match['response'],
                'source': 'dataset',
                'quality_score': self._score_response_quality(dataset_match['response'], emotion_data, crisis_data),
                'emotion_appropriate': True,
                'crisis_appropriate': True
            }
            return response_data
        
        # Step 2: If no good match found, call GROQ API
        print("🔍 No good dataset match found, calling GROQ API...")
        try:
            data = {
                "model": "llama-3.3-70b-versatile",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 300,
                "presence_penalty": 0.1,
                "frequency_penalty": 0.1
            }
            
            response = requests.post(self.url, headers=self.headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"].strip()
                print("✅ GROQ API response successful")
                # --- Post-process for human-like, concise, emoji-rich replies ---
                ai_response = self._shorten_response(ai_response)
                ai_response = self._add_emoji_to_response(ai_response, emotion_data['primary_emotion'] if emotion_data else None)
                if len(ai_response) > 300:
                    ai_response = ai_response[:297] + "...";
                emotion = emotion_data['primary_emotion'] if emotion_data and 'primary_emotion' in emotion_data else 'neutral'
                heading = self._get_heading_for_emotion(emotion)
                label = f"<span style='font-size:0.9em;color:#2196F3;'>Mood: {emotion.capitalize() if emotion != 'neutral' else 'Checking in'}</span><br>"
                ai_response = f"<strong>{heading}</strong><br>{label}{ai_response}"
                response_data = {
                    'response': ai_response,
                    'source': 'groq_api',
                    'quality_score': self._score_response_quality(ai_response, emotion_data, crisis_data),
                    'emotion_appropriate': self._check_emotion_appropriateness(ai_response, emotion_data),
                    'crisis_appropriate': self._check_crisis_appropriateness(ai_response, crisis_data)
                }
                return response_data
            else:
                print(f"❌ GROQ API error: {response.status_code} - {response.text}")
                # Return fallback response
                fallback_response = self.get_fallback_response(user_message, emotion_data, crisis_data)
                return {
                    'response': fallback_response,
                    'source': 'fallback',
                    'quality_score': 0.5,
                    'emotion_appropriate': True,
                    'crisis_appropriate': True
                }
            
        except Exception as e:
            print(f"❌ GROQ API error: {str(e)}")
            # Return fallback response
            fallback_response = self.get_fallback_response(user_message, emotion_data, crisis_data)
            return {
                'response': fallback_response,
                'source': 'fallback',
                'quality_score': 0.5,
                'emotion_appropriate': True,
                'crisis_appropriate': True
            }

    def _score_response_quality(self, response: str, emotion_data: Dict, crisis_data: Dict) -> float:
        """Score response quality based on appropriateness and helpfulness"""
        score = 0.5  # Base score
        
        # Check for appropriate length
        if 50 <= len(response) <= 300:
            score += 0.1
        
        # Check for supportive language
        supportive_words = ['support', 'listen', 'understand', 'valid', 'okay', 'help', 'care']
        if any(word in response.lower() for word in supportive_words):
            score += 0.1
        
        # Check for appropriate tone
        if '?' in response:  # Shows engagement
            score += 0.1
        
        # Check for crisis appropriateness
        if crisis_data and crisis_data['level'] != 'none':
            if any(word in response.lower() for word in ['help', 'support', 'professional', 'crisis']):
                score += 0.2
        
        # Check for emotion appropriateness
        if emotion_data and emotion_data['primary_emotion'] != 'neutral':
            emotion_words = {
                'anxious': ['breathe', 'ground', 'calm', 'anxiety'],
                'sad': ['sad', 'feel', 'valid', 'okay'],
                'angry': ['angry', 'frustrated', 'understand', 'express'],
                'stressed': ['stress', 'overwhelmed', 'break', 'step'],
                'lonely': ['lonely', 'alone', 'connect', 'reach'],
                'happy': ['happy', 'good', 'positive', 'celebrate'],
                'confused': ['confused', 'uncertain', 'clarify', 'understand']
            }
            
            emotion = emotion_data['primary_emotion']
            if emotion in emotion_words:
                if any(word in response.lower() for word in emotion_words[emotion]):
                    score += 0.1
        
        return min(score, 1.0)

    def _check_emotion_appropriateness(self, response: str, emotion_data: Dict) -> bool:
        """Check if response is appropriate for the detected emotion"""
        if not emotion_data or emotion_data['primary_emotion'] == 'neutral':
            return True
        
        emotion = emotion_data['primary_emotion']
        intensity = emotion_data['intensity']
        
        # Check for appropriate emotion-specific content
        emotion_indicators = {
            'anxious': ['breathe', 'ground', 'calm', 'anxiety', 'worried'],
            'sad': ['sad', 'feel', 'valid', 'okay', 'understand'],
            'angry': ['angry', 'frustrated', 'express', 'understand'],
            'stressed': ['stress', 'overwhelmed', 'break', 'step'],
            'lonely': ['lonely', 'alone', 'connect', 'reach'],
            'happy': ['happy', 'good', 'positive', 'celebrate'],
            'confused': ['confused', 'uncertain', 'clarify', 'understand']
        }
        
        if emotion in emotion_indicators:
            return any(word in response.lower() for word in emotion_indicators[emotion])
        
        return True

    def _check_crisis_appropriateness(self, response: str, crisis_data: Dict) -> bool:
        """Check if response is appropriate for the crisis level"""
        if not crisis_data or crisis_data['level'] == 'none':
            return True
        
        level = crisis_data['level']
        
        # Check for crisis-appropriate content
        if level in ['immediate', 'high']:
            crisis_indicators = ['help', 'support', 'professional', 'crisis', '988', '911']
            return any(word in response.lower() for word in crisis_indicators)
        
        return True

    def get_fallback_response(self, user_message: str, emotion_data: Dict = None, crisis_data: Dict = None) -> str:
        """Get enhanced fallback response when GROQ is unavailable"""
        # Try dataset fallback first
        emotion = emotion_data['primary_emotion'] if emotion_data else None
        fallback_match = self.dataset_handler.find_best_match(user_message, emotion, threshold=0.1)
        if fallback_match:
            return fallback_match['response']
        
        # Use enhanced fallbacks with emotion and intensity
        if emotion_data and emotion_data['primary_emotion'] in self.fallback_responses:
            emotion = emotion_data['primary_emotion']
            intensity = emotion_data['intensity']
            
            if emotion in self.fallback_responses and intensity in self.fallback_responses[emotion]:
                return random.choice(self.fallback_responses[emotion][intensity])
            elif emotion in self.fallback_responses:
                # Fall back to medium intensity if specific intensity not available
                return random.choice(self.fallback_responses[emotion]['medium'])
        
        return random.choice(self.fallback_responses['default'])

    def enhance_with_dataset(self, user_message: str, emotion_data: Dict) -> str:
        """Enhance response with mental health dataset context"""
        response_data = self.get_response([{"role": "user", "content": user_message}], emotion_data)
        return response_data['response']
    
    def get_dataset_stats(self) -> Dict:
        """Get dataset statistics"""
        return self.dataset_handler.get_dataset_stats()

    def update_conversation_memory(self, user_id: str, message: str, response: str, emotion_data: Dict, crisis_data: Dict):
        """Update conversation memory for multi-turn context"""
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
        
        memory_entry = {
            'timestamp': datetime.now(),
            'user_message': message,
            'response': response,
            'emotion': emotion_data,
            'crisis': crisis_data
        }
        
        self.conversation_memory[user_id].append(memory_entry)
        
        # Keep only recent memory
        if len(self.conversation_memory[user_id]) > self.max_memory_length:
            self.conversation_memory[user_id].pop(0)

    def get_conversation_summary(self, user_id: str) -> Dict[str, any]:
        """Get summary of conversation for a user"""
        if user_id not in self.conversation_memory:
            return {'message_count': 0, 'emotion_trend': 'stable', 'crisis_level': 'none'}
        
        memory = self.conversation_memory[user_id]
        
        if not memory:
            return {'message_count': 0, 'emotion_trend': 'stable', 'crisis_level': 'none'}
        
        # Analyze emotion trends
        emotions = [entry['emotion']['primary_emotion'] for entry in memory if entry['emotion']]
        crisis_levels = [entry['crisis']['level'] for entry in memory if entry['crisis']]
        
        # Find most common emotion
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        primary_emotion = max(emotion_counts, key=emotion_counts.get) if emotion_counts else 'neutral'
        
        # Find highest crisis level
        level_priority = {'immediate': 4, 'high': 3, 'medium': 2, 'low': 1, 'none': 0}
        max_crisis_level = max(crisis_levels, key=lambda x: level_priority.get(x, 0)) if crisis_levels else 'none'
        
        return {
            'message_count': len(memory),
            'primary_emotion': primary_emotion,
            'crisis_level': max_crisis_level,
            'emotion_trend': self._analyze_emotion_trend(emotions),
            'crisis_trend': self._analyze_crisis_trend(crisis_levels),
            'last_interaction': memory[-1]['timestamp'] if memory else None
        }
    
    def _shorten_response(self, response: str) -> str:
         # Keep only the first 2-3 sentences
        sentences = re.split(r'(?<=[.!?]) +', response)
        short = ' '.join(sentences[:3]).strip()
        return short     

    def _add_emoji_to_response(self, response: str, emotion: str = None) -> str:
        # If response already has an emoji, return as is
    
        if re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', response):
            return response
        # Choose emoji based on emotion
        emoji_map = {
            'anxious': '😟',
            'sad': '😢',
            'angry': '😠',
            'stressed': '😣',
            'lonely': '🤗',
            'happy': '😊',
            'confused': '🤔',
            'default': '💚'
        }
        emoji = emoji_map.get(emotion, emoji_map['default'])
        # Add emoji at the end if not present
        return response + " " + emoji       
    

    def _analyze_emotion_trend(self, emotions: List[str]) -> str:
        """Analyze emotion trend from conversation history"""
        if len(emotions) < 3:
            return 'stable'
        
        recent_emotions = emotions[-3:]
        
        if recent_emotions.count('happy') >= 2:
            return 'improving'
        elif recent_emotions.count('sad') >= 2 or recent_emotions.count('anxious') >= 2:
            return 'declining'
        else:
            return 'stable'

    def _analyze_crisis_trend(self, crisis_levels: List[str]) -> str:
        """Analyze crisis trend from conversation history"""
        if len(crisis_levels) < 3:
            return 'stable'
        
        recent_levels = crisis_levels[-3:]
        
        if any(level in ['immediate', 'high'] for level in recent_levels):
            return 'escalating'
        elif recent_levels.count('none') >= 2:
            return 'improving'
        else:
            return 'stable' 

    def _get_heading_for_emotion(self, emotion: str) -> str:
        headings = {
            'anxious': "🌱 Here for You",
            'sad': "💙 Gentle Support",
            'angry': "🔥 Let's Cool Down",
            'stressed': "🧘 Quick Tip",
            'lonely': "🤗 You're Not Alone",
            'happy': "🌞 Celebrate!",
            'confused': "❓ Let's Clarify",
            'neutral': "💬 Checking In",
            'default': "💬 Support Message"
        }
        return headings.get(emotion, headings['default']) 