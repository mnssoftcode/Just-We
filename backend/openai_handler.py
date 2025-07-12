import requests
import os
import json
import random
from typing import List, Dict, Optional
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.dataset_handler import DatasetHandler

class OpenAIHandler:
    def __init__(self):
        """Initialize GROQ handler with mental health focus and Fast Chatbot Strategy"""
        self.api_key = os.getenv('GROQ_API_KEY', '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')
        if not self.api_key:
            raise ValueError("GROQ API key not found in environment variables")
        
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Initialize dataset handler for Fast Chatbot Strategy
        self.dataset_handler = DatasetHandler()
        
        # Mental health system prompt
        self.system_prompt = """You are a supportive, empathetic mental health assistant named "CalmSpace." Your purpose is to help users who may be feeling lonely, anxious, overwhelmed, or sad. You are not a doctor and never give medical advice or diagnosis.

Your role is to:
- Listen actively and non-judgmentally
- Ask gentle, open-ended questions
- Encourage healthy emotional expression
- Offer grounding exercises (like breathing techniques)
- Recommend positive coping strategies (journaling, walking, talking to someone)
- When appropriate, suggest contacting a mental health professional or helpline

If the user expresses suicidal thoughts or says something very serious (like "I want to die", "I'm worthless", etc.), respond calmly and compassionately, and direct them to professional help or crisis hotlines. Never ignore or dismiss their words.

Tone: Warm, kind, reassuring, respectful, never robotic or overly cheerful.
Language: Simple and clear. Avoid complex clinical terms.

Always end your response with a soft invitation: "Would you like to talk more about this?" or "I'm here to listen." """
        
        # Fallback responses for when GROQ is unavailable
        self.fallback_responses = {
            'anxious': [
                "I can sense you're feeling anxious right now. That's completely okay. Let's take a moment together - try taking three deep breaths with me. Inhale slowly for 4 counts, hold for 4, then exhale for 4. How does that feel?",
                "Anxiety can be really overwhelming. Remember, it's okay to feel this way. Sometimes talking about what's on your mind can help. Would you like to share what's making you feel anxious?",
                "I hear you're feeling anxious. That's a really tough feeling to sit with. Have you tried any grounding techniques? One simple one is to name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste."
            ],
            'sad': [
                "I'm so sorry you're feeling sad right now. Your feelings are valid, and it's okay to not be okay. Sometimes just acknowledging how we feel can be the first step toward feeling better. Would you like to talk about what's on your mind?",
                "Sadness can feel really heavy and isolating. Remember that you're not alone in feeling this way. Sometimes the simple act of expressing our feelings can help lighten the load a little. I'm here to listen.",
                "It sounds like you're going through a really difficult time. Your feelings matter, and it's okay to take time to process them. Sometimes talking to someone we trust can help. Is there someone in your life you feel comfortable reaching out to?"
            ],
            'stressed': [
                "Stress can feel really overwhelming, like everything is piling up at once. It's okay to feel this way. Sometimes breaking things down into smaller steps can help. What's one small thing you could do right now that might help you feel a little better?",
                "I can hear how stressed you're feeling. That's completely understandable. Sometimes the best thing we can do is give ourselves permission to take a break. Even just a few minutes of deep breathing can help reset our nervous system.",
                "Stress can make everything feel more difficult than it needs to be. Remember that it's okay to ask for help and to take things one step at a time. What's one thing that usually helps you feel more grounded when you're stressed?"
            ],
            'lonely': [
                "Loneliness can be one of the hardest feelings to sit with. It's completely normal to feel this way, and your feelings are valid. Sometimes reaching out to someone we trust, even just to say hello, can help. Is there someone you could reach out to?",
                "I hear how lonely you're feeling right now. That's a really difficult place to be. Remember that you're not alone in feeling this way - many people experience loneliness, even when surrounded by others. Sometimes joining a community or group activity can help. What interests you?",
                "Loneliness can feel really isolating. It's okay to feel this way. Sometimes the simple act of being heard can help us feel less alone. I'm here to listen, and I want you to know that your feelings matter."
            ],
            'default': [
                "I'm here to listen and support you. Sometimes just talking about what's on our minds can help us feel a little better. Would you like to share what's going on?",
                "I hear you, and I want you to know that your feelings are valid. It's okay to not be okay sometimes. I'm here to listen whenever you're ready to talk.",
                "Thank you for reaching out. Sometimes the bravest thing we can do is ask for support. I'm here to listen and support you however I can."
            ]
        }

    def prepare_context(self, user_message: str, conversation_history: List[Dict], emotion: str) -> List[Dict]:
        """Prepare conversation context for GROQ API"""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add emotion-specific context
        if emotion != 'neutral':
            emotion_context = f"Note: The user appears to be feeling {emotion}. Adjust your response to be particularly supportive for this emotional state."
            messages.append({"role": "system", "content": emotion_context})
        
        # Add conversation history (last 10 messages to stay within limits)
        for msg in conversation_history[-10:]:
            if msg.get('role') and msg.get('content'):
                messages.append({"role": msg['role'], "content": msg['content']})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return messages

    def get_response(self, messages: List[Dict], emotion: str = None) -> str:
        """Get response using Fast Chatbot Strategy"""
        user_message = messages[-1]['content']
        
        # Step 1: Search datasets for close match (FAST)
        dataset_match = self.dataset_handler.find_best_match(user_message, emotion, threshold=0.3)
        
        if dataset_match:
            print(f"✅ Found dataset match: {dataset_match['source']} (score: {dataset_match['similarity_score']:.3f})")
            return dataset_match['response']
        
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
                return ai_response
            else:
                print(f"❌ GROQ API error: {response.status_code} - {response.text}")
                # Return fallback response
                return self.get_fallback_response(user_message, emotion)
            
        except Exception as e:
            print(f"❌ GROQ API error: {str(e)}")
            # Return fallback response
            return self.get_fallback_response(user_message, emotion)

    def get_fallback_response(self, user_message: str, emotion: str = None) -> str:
        """Get fallback response when GROQ is unavailable"""
        # Try dataset fallback first
        fallback_match = self.dataset_handler.find_best_match(user_message, emotion, threshold=0.1)
        if fallback_match:
            return fallback_match['response']
        
        # Use hardcoded fallbacks
        if emotion and emotion in self.fallback_responses:
            return random.choice(self.fallback_responses[emotion])
        else:
            return random.choice(self.fallback_responses['default'])

    def enhance_with_dataset(self, user_message: str, emotion: str) -> str:
        """Enhance response with mental health dataset context (Phase 3)"""
        # This is now handled by the Fast Chatbot Strategy
        return self.get_response([{"role": "user", "content": user_message}], emotion)
    
    def get_dataset_stats(self) -> Dict:
        """Get dataset statistics"""
        return self.dataset_handler.get_dataset_stats() 