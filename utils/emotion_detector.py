import re
from typing import Dict, List, Optional, Tuple
import random
from datetime import datetime

class EmotionDetector:
    def __init__(self):
        """Initialize enhanced emotion detection with multi-label classification"""
        
        # Enhanced emotion patterns with intensity indicators
        self.emotion_patterns = {
            'anxious': {
                'high': [
                    r'\b(panic attack|hyperventilating|can\'t breathe|heart racing|sweating|shaking|trembling)\b',
                    r'\b(overwhelming anxiety|extreme worry|terrified|fearful|scared)\b',
                    r'\b(racing thoughts|mind won\'t stop|obsessive thoughts)\b'
                ],
                'medium': [
                    r'\b(anxious|anxiety|worried|worry|nervous|stressed|stress)\b',
                    r'\b(what if|what\'s going to happen|afraid|scared|fear)\b',
                    r'\b(overthinking|restless|on edge|tense)\b'
                ],
                'low': [
                    r'\b(slightly anxious|a bit worried|concerned|uneasy)\b',
                    r'\b(not sure|uncertain|hesitant)\b'
                ]
            },
            'sad': {
                'high': [
                    r'\b(depressed|hopeless|worthless|empty|numb|suicidal)\b',
                    r'\b(crying uncontrollably|sobbing|weeping|miserable|devastated)\b',
                    r'\b(don\'t care|nothing matters|pointless|meaningless|life is worthless)\b'
                ],
                'medium': [
                    r'\b(sad|down|blue|unhappy|melancholy|gloomy)\b',
                    r'\b(tears|crying|weeping|miserable|heartbroken)\b',
                    r'\b(lonely|alone|isolated|no one understands)\b'
                ],
                'low': [
                    r'\b(slightly sad|a bit down|melancholy|quiet)\b',
                    r'\b(not feeling great|off|not myself)\b'
                ]
            },
            'angry': {
                'high': [
                    r'\b(furious|rage|livid|enraged|hate everything|violent)\b',
                    r'\b(want to scream|want to break something|out of control)\b',
                    r'\b(hate myself|hate everyone|pissed off|fuming)\b'
                ],
                'medium': [
                    r'\b(angry|mad|irritated|annoyed|frustrated|upset)\b',
                    r'\b(unfair|unjust|wrong|stupid|idiot|dumb)\b',
                    r'\b(fed up|sick of|tired of)\b'
                ],
                'low': [
                    r'\b(slightly annoyed|irritated|frustrated)\b',
                    r'\b(not happy|disappointed)\b'
                ]
            },
            'stressed': {
                'high': [
                    r'\b(overwhelmed|can\'t handle|breaking point|burned out)\b',
                    r'\b(exhausted|drained|fatigued|mentally exhausted)\b',
                    r'\b(too many things|everything at once|piling up|drowning)\b'
                ],
                'medium': [
                    r'\b(stressed|pressure|busy|rushed|deadline|work|job)\b',
                    r'\b(responsibilities|obligations|commitments)\b',
                    r'\b(tired|exhausted|burned out|drained)\b'
                ],
                'low': [
                    r'\b(slightly stressed|busy|a bit overwhelmed)\b',
                    r'\b(have a lot on my plate)\b'
                ]
            },
            'lonely': {
                'high': [
                    r'\b(completely alone|no one cares|no one understands|isolated)\b',
                    r'\b(empty house|silence|no one to talk to|abandoned)\b',
                    r'\b(miss someone desperately|longing|yearning)\b'
                ],
                'medium': [
                    r'\b(lonely|alone|no friends|no one around)\b',
                    r'\b(by myself|no one to talk to|no one understands)\b',
                    r'\b(miss someone|missing|wish someone was here)\b'
                ],
                'low': [
                    r'\b(slightly lonely|missing someone|quiet)\b',
                    r'\b(wish I had company)\b'
                ]
            },
            'happy': {
                'high': [
                    r'\b(ecstatic|elated|thrilled|overjoyed|euphoric)\b',
                    r'\b(so happy|extremely happy|delighted|excited)\b',
                    r'\b(best day ever|amazing|wonderful|fantastic)\b'
                ],
                'medium': [
                    r'\b(happy|glad|pleased|content|satisfied)\b',
                    r'\b(good mood|feeling good|positive|optimistic)\b',
                    r'\b(relieved|grateful|thankful)\b'
                ],
                'low': [
                    r'\b(slightly happy|okay|fine|alright)\b',
                    r'\b(not bad|doing okay)\b'
                ]
            },
            'confused': {
                'high': [
                    r'\b(completely lost|don\'t know what to do|overwhelmed by choices)\b',
                    r'\b(mixed up|contradictory feelings|conflicted)\b',
                    r'\b(unsure about everything|uncertain about future)\b'
                ],
                'medium': [
                    r'\b(confused|unsure|don\'t know|uncertain|mixed up)\b',
                    r'\b(what should i do|what do i want|lost|directionless)\b',
                    r'\b(not sure|maybe|perhaps|possibly)\b'
                ],
                'low': [
                    r'\b(slightly confused|unsure|not certain)\b',
                    r'\b(maybe|perhaps)\b'
                ]
            }
        }
        
        # Compile regex patterns
        self.compiled_patterns = {}
        for emotion, intensities in self.emotion_patterns.items():
            self.compiled_patterns[emotion] = {}
            for intensity, patterns in intensities.items():
                self.compiled_patterns[emotion][intensity] = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        
        # Emotion tracking for conversation context
        self.emotion_history = []
        self.max_history = 10

    def detect_emotion(self, message: str) -> Dict[str, any]:
        """
        Enhanced emotion detection with multi-label classification
        Returns: Dict with 'primary_emotion', 'intensity', 'all_emotions', 'confidence'
        """
        message_lower = message.lower()
        emotion_scores = {}
        all_emotions = []
        
        # Score each emotion and intensity
        for emotion, intensities in self.compiled_patterns.items():
            emotion_score = 0
            max_intensity = 'low'
            
            for intensity, patterns in intensities.items():
                intensity_score = 0
                for pattern in patterns:
                    matches = pattern.findall(message_lower)
                    intensity_score += len(matches)
                
                if intensity_score > 0:
                    emotion_score += intensity_score
                    # Track highest intensity for this emotion
                    if intensity == 'high' or (intensity == 'medium' and max_intensity == 'low'):
                        max_intensity = intensity
                    elif intensity == 'medium' and max_intensity == 'low':
                        max_intensity = intensity
            
            if emotion_score > 0:
                emotion_scores[emotion] = {
                    'score': emotion_score,
                    'intensity': max_intensity
                }
                all_emotions.append({
                    'emotion': emotion,
                    'intensity': max_intensity,
                    'score': emotion_score
                })
        
        # Determine primary emotion
        if emotion_scores:
            primary_emotion = max(emotion_scores, key=lambda x: emotion_scores[x]['score'])
            primary_intensity = emotion_scores[primary_emotion]['intensity']
            confidence = min(emotion_scores[primary_emotion]['score'] / 3, 1.0)  # Normalize confidence
        else:
            primary_emotion = 'neutral'
            primary_intensity = 'low'
            confidence = 0.0
            all_emotions = [{'emotion': 'neutral', 'intensity': 'low', 'score': 0}]
        
        # Update emotion history
        self._update_emotion_history(primary_emotion, primary_intensity, confidence)
        
        return {
            'primary_emotion': primary_emotion,
            'intensity': primary_intensity,
            'all_emotions': all_emotions,
            'confidence': confidence,
            'emotion_trend': self._get_emotion_trend()
        }

    def _update_emotion_history(self, emotion: str, intensity: str, confidence: float):
        """Update emotion history for trend analysis"""
        timestamp = datetime.now()
        self.emotion_history.append({
            'emotion': emotion,
            'intensity': intensity,
            'confidence': confidence,
            'timestamp': timestamp
        })
        
        # Keep only recent history
        if len(self.emotion_history) > self.max_history:
            self.emotion_history.pop(0)

    def _get_emotion_trend(self) -> str:
        """Analyze emotion trend over recent messages"""
        if len(self.emotion_history) < 3:
            return 'stable'
        
        recent_emotions = [entry['emotion'] for entry in self.emotion_history[-3:]]
        
        # Check for improving trend
        if recent_emotions.count('happy') >= 2:
            return 'improving'
        elif recent_emotions.count('sad') >= 2 or recent_emotions.count('anxious') >= 2:
            return 'declining'
        else:
            return 'stable'

    def get_emotion_context(self, emotion_data: Dict) -> str:
        """Get enhanced context about detected emotion for AI response"""
        emotion = emotion_data['primary_emotion']
        intensity = emotion_data['intensity']
        trend = emotion_data.get('emotion_trend', 'stable')
        
        base_contexts = {
            'anxious': {
                'high': "The user is experiencing high anxiety with intense physical and emotional symptoms. Focus on immediate grounding techniques and crisis intervention if needed.",
                'medium': "The user appears to be experiencing moderate anxiety. Focus on grounding techniques, breathing exercises, and reassurance.",
                'low': "The user shows mild anxiety. Offer gentle support and coping strategies."
            },
            'sad': {
                'high': "The user is experiencing intense sadness or depression. Offer immediate comfort and consider crisis assessment.",
                'medium': "The user seems to be feeling sad or depressed. Offer comfort, validation, and gentle encouragement.",
                'low': "The user shows mild sadness. Provide gentle support and understanding."
            },
            'angry': {
                'high': "The user is experiencing intense anger. Acknowledge their feelings and help them find healthy ways to express anger.",
                'medium': "The user appears to be angry or frustrated. Acknowledge their feelings and help them find healthy outlets.",
                'low': "The user shows mild irritation. Offer understanding and support."
            },
            'stressed': {
                'high': "The user is experiencing high stress and overwhelm. Help them break things down and find immediate coping strategies.",
                'medium': "The user is feeling stressed or overwhelmed. Help them break things down and find coping strategies.",
                'low': "The user shows mild stress. Offer support and practical suggestions."
            },
            'lonely': {
                'high': "The user is experiencing intense loneliness. Offer connection and immediate support.",
                'medium': "The user is feeling lonely or isolated. Offer connection and suggest reaching out to others.",
                'low': "The user shows mild loneliness. Offer gentle support and connection."
            },
            'happy': {
                'high': "The user is experiencing joy and positive emotions. Celebrate with them and encourage continued positive activities.",
                'medium': "The user appears to be in a positive mood. Support their positive state and encourage healthy habits.",
                'low': "The user shows mild positive emotions. Support their positive state."
            },
            'confused': {
                'high': "The user is experiencing significant confusion. Help them clarify their thoughts and feelings.",
                'medium': "The user seems confused or uncertain. Help them clarify their thoughts and feelings.",
                'low': "The user shows mild confusion. Offer gentle guidance and support."
            },
            'neutral': {
                'low': "The user's emotional state appears neutral. Maintain supportive and empathetic tone."
            }
        }
        
        context = base_contexts.get(emotion, {}).get(intensity, "The user's emotional state requires attention and support.")
        
        # Add trend information
        if trend == 'improving':
            context += " Note: The user's emotional state appears to be improving."
        elif trend == 'declining':
            context += " Note: The user's emotional state appears to be declining and may need increased support."
        
        return context

    def get_emotion_suggestions(self, emotion_data: Dict) -> List[str]:
        """Get enhanced coping suggestions based on detected emotion and intensity"""
        emotion = emotion_data['primary_emotion']
        intensity = emotion_data['intensity']
        
        suggestions = {
            'anxious': {
                'high': [
                    "Try the 4-7-8 breathing technique: inhale for 4, hold for 7, exhale for 8",
                    "Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste",
                    "Take a short walk to help ground yourself",
                    "Write down your worries to get them out of your head",
                    "Consider calling a crisis hotline if anxiety is overwhelming"
                ],
                'medium': [
                    "Try the 4-7-8 breathing technique: inhale for 4, hold for 7, exhale for 8",
                    "Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste",
                    "Take a short walk to help ground yourself",
                    "Write down your worries to get them out of your head"
                ],
                'low': [
                    "Take a few deep breaths",
                    "Try a simple grounding exercise",
                    "Talk to someone about what's on your mind"
                ]
            },
            'sad': {
                'high': [
                    "Allow yourself to feel sad - it's a normal emotion",
                    "Try doing something small that usually brings you joy",
                    "Talk to someone you trust about how you're feeling",
                    "Consider journaling your thoughts and feelings",
                    "Consider reaching out to a mental health professional"
                ],
                'medium': [
                    "Allow yourself to feel sad - it's a normal emotion",
                    "Try doing something small that usually brings you joy",
                    "Talk to someone you trust about how you're feeling",
                    "Consider journaling your thoughts and feelings"
                ],
                'low': [
                    "It's okay to feel sad sometimes",
                    "Try doing something you enjoy",
                    "Talk to someone about how you're feeling"
                ]
            },
            'angry': {
                'high': [
                    "Take a few deep breaths to help calm your nervous system",
                    "Try counting to 10 before responding",
                    "Write down what you're angry about",
                    "Find a physical outlet like exercise or punching a pillow",
                    "Consider stepping away from the situation temporarily"
                ],
                'medium': [
                    "Take a few deep breaths to help calm your nervous system",
                    "Try counting to 10 before responding",
                    "Write down what you're angry about",
                    "Find a physical outlet like exercise"
                ],
                'low': [
                    "Take a few deep breaths",
                    "Try counting to 10",
                    "Express your feelings in a healthy way"
                ]
            },
            'stressed': {
                'high': [
                    "Break down what's stressing you into smaller, manageable pieces",
                    "Take a 5-minute break to do something you enjoy",
                    "Try progressive muscle relaxation",
                    "Make a list of what you can control vs. what you can't",
                    "Consider asking for help or delegating tasks"
                ],
                'medium': [
                    "Break down what's stressing you into smaller, manageable pieces",
                    "Take a 5-minute break to do something you enjoy",
                    "Try progressive muscle relaxation",
                    "Make a list of what you can control vs. what you can't"
                ],
                'low': [
                    "Take a short break",
                    "Try organizing your tasks",
                    "Ask for help if needed"
                ]
            },
            'lonely': {
                'high': [
                    "Reach out to someone you haven't talked to in a while",
                    "Consider joining a group or community around your interests",
                    "Try volunteering to connect with others",
                    "Write a letter to someone you care about",
                    "Consider professional support if loneliness is persistent"
                ],
                'medium': [
                    "Reach out to someone you haven't talked to in a while",
                    "Consider joining a group or community around your interests",
                    "Try volunteering to connect with others",
                    "Write a letter to someone you care about"
                ],
                'low': [
                    "Reach out to a friend or family member",
                    "Try a new activity or hobby",
                    "Consider joining a group"
                ]
            },
            'happy': {
                'high': [
                    "Celebrate your positive feelings!",
                    "Share your joy with someone you care about",
                    "Use this positive energy to do something you enjoy",
                    "Remember this feeling for when times are harder"
                ],
                'medium': [
                    "Enjoy your positive mood",
                    "Share your good feelings with others",
                    "Use this energy for something productive"
                ],
                'low': [
                    "It's good to feel positive",
                    "Build on this positive feeling"
                ]
            },
            'confused': {
                'high': [
                    "Take time to sit with your feelings without judgment",
                    "Try writing down your thoughts to clarify them",
                    "Talk to someone you trust about what's on your mind",
                    "Remember that it's okay to not have all the answers",
                    "Consider talking to a counselor for clarity"
                ],
                'medium': [
                    "Take time to sit with your feelings without judgment",
                    "Try writing down your thoughts to clarify them",
                    "Talk to someone you trust about what's on your mind",
                    "Remember that it's okay to not have all the answers"
                ],
                'low': [
                    "Take time to think things through",
                    "Talk to someone about your thoughts",
                    "It's okay to be unsure sometimes"
                ]
            }
        }
        
        return suggestions.get(emotion, {}).get(intensity, ["Remember that your feelings are valid and it's okay to not be okay sometimes."])

    def get_emotion_intensity(self, message: str, emotion: str) -> str:
        """Enhanced emotion intensity detection"""
        if emotion == 'neutral':
            return 'low'
        
        # Use the enhanced detection method
        emotion_data = self.detect_emotion(message)
        return emotion_data['intensity']

    def enhance_with_ml(self, message: str) -> Dict[str, any]:
        """
        Enhanced emotion detection with multi-label classification
        Returns comprehensive emotion analysis
        """
        return self.detect_emotion(message)

    def get_emotion_summary(self) -> Dict[str, any]:
        """Get summary of recent emotion patterns"""
        if not self.emotion_history:
            return {'trend': 'stable', 'primary_emotion': 'neutral', 'intensity': 'low'}
        
        recent_emotions = [entry['emotion'] for entry in self.emotion_history[-5:]]
        recent_intensities = [entry['intensity'] for entry in self.emotion_history[-5:]]
        
        # Find most common emotion
        emotion_counts = {}
        for emotion in recent_emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        primary_emotion = max(emotion_counts, key=emotion_counts.get) if emotion_counts else 'neutral'
        
        # Determine average intensity
        intensity_scores = {'low': 1, 'medium': 2, 'high': 3}
        avg_intensity_score = sum(intensity_scores.get(intensity, 1) for intensity in recent_intensities) / len(recent_intensities)
        
        if avg_intensity_score >= 2.5:
            avg_intensity = 'high'
        elif avg_intensity_score >= 1.5:
            avg_intensity = 'medium'
        else:
            avg_intensity = 'low'
        
        return {
            'trend': self._get_emotion_trend(),
            'primary_emotion': primary_emotion,
            'intensity': avg_intensity,
            'recent_emotions': recent_emotions,
            'confidence': sum(entry['confidence'] for entry in self.emotion_history[-5:]) / len(self.emotion_history[-5:]) if self.emotion_history else 0
        } 