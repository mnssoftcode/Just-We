import re
from typing import Dict, List, Optional
import random

class EmotionDetector:
    def __init__(self):
        """Initialize emotion detection with keyword patterns"""
        
        # Emotion keywords and patterns
        self.emotion_patterns = {
            'anxious': [
                r'\b(anxious|anxiety|worried|worry|nervous|panic|overwhelmed|stressed|stress)\b',
                r'\b(can\'t breathe|heart racing|sweating|shaking|trembling)\b',
                r'\b(what if|what\'s going to happen|afraid|scared|fear)\b',
                r'\b(overthinking|racing thoughts|mind won\'t stop)\b'
            ],
            'sad': [
                r'\b(sad|depressed|down|blue|hopeless|worthless|empty|numb)\b',
                r'\b(crying|tears|sobbing|weeping|miserable|unhappy)\b',
                r'\b(don\'t care|nothing matters|pointless|meaningless)\b',
                r'\b(lonely|alone|isolated|no one understands)\b'
            ],
            'angry': [
                r'\b(angry|mad|furious|rage|irritated|annoyed|frustrated)\b',
                r'\b(hate|hate myself|hate everything|pissed off)\b',
                r'\b(unfair|unjust|wrong|stupid|idiot|dumb)\b',
                r'\b(want to scream|want to break something|violent)\b'
            ],
            'stressed': [
                r'\b(stressed|overwhelmed|too much|can\'t handle|pressure)\b',
                r'\b(busy|rushed|deadline|work|job|responsibilities)\b',
                r'\b(exhausted|tired|burned out|drained|fatigued)\b',
                r'\b(too many things|everything at once|piling up)\b'
            ],
            'lonely': [
                r'\b(lonely|alone|isolated|no friends|no one cares)\b',
                r'\b(by myself|no one to talk to|no one understands)\b',
                r'\b(miss someone|missing|wish someone was here)\b',
                r'\b(no one around|empty house|quiet|silence)\b'
            ],
            'confused': [
                r'\b(confused|unsure|don\'t know|uncertain|mixed up)\b',
                r'\b(what should i do|what do i want|lost|directionless)\b',
                r'\b(contradictory|mixed feelings|conflicted)\b',
                r'\b(not sure|maybe|perhaps|possibly)\b'
            ]
        }
        
        # Compile regex patterns
        self.compiled_patterns = {}
        for emotion, patterns in self.emotion_patterns.items():
            self.compiled_patterns[emotion] = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]

    def detect_emotion(self, message: str) -> str:
        """
        Detect primary emotion in user message
        Returns: emotion name or 'neutral'
        """
        message_lower = message.lower()
        emotion_scores = {}
        
        # Score each emotion based on pattern matches
        for emotion, patterns in self.compiled_patterns.items():
            score = 0
            for pattern in patterns:
                matches = pattern.findall(message_lower)
                score += len(matches)
            if score > 0:
                emotion_scores[emotion] = score
        
        # Return the emotion with highest score, or 'neutral' if no matches
        if emotion_scores:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            return primary_emotion
        
        return 'neutral'

    def get_emotion_context(self, emotion: str) -> str:
        """Get context about detected emotion for AI response"""
        emotion_contexts = {
            'anxious': "The user appears to be experiencing anxiety. Focus on grounding techniques, breathing exercises, and reassurance.",
            'sad': "The user seems to be feeling sad or depressed. Offer comfort, validation, and gentle encouragement.",
            'angry': "The user appears to be angry or frustrated. Acknowledge their feelings and help them find healthy ways to express anger.",
            'stressed': "The user is feeling stressed or overwhelmed. Help them break things down and find coping strategies.",
            'lonely': "The user is feeling lonely or isolated. Offer connection and suggest reaching out to others.",
            'confused': "The user seems confused or uncertain. Help them clarify their thoughts and feelings.",
            'neutral': "The user's emotional state appears neutral. Maintain supportive and empathetic tone."
        }
        
        return emotion_contexts.get(emotion, emotion_contexts['neutral'])

    def get_emotion_suggestions(self, emotion: str) -> List[str]:
        """Get coping suggestions based on detected emotion"""
        suggestions = {
            'anxious': [
                "Try the 4-7-8 breathing technique: inhale for 4, hold for 7, exhale for 8",
                "Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste",
                "Take a short walk to help ground yourself",
                "Write down your worries to get them out of your head"
            ],
            'sad': [
                "Allow yourself to feel sad - it's a normal emotion",
                "Try doing something small that usually brings you joy",
                "Talk to someone you trust about how you're feeling",
                "Consider journaling your thoughts and feelings"
            ],
            'angry': [
                "Take a few deep breaths to help calm your nervous system",
                "Try counting to 10 before responding",
                "Write down what you're angry about",
                "Find a physical outlet like exercise or punching a pillow"
            ],
            'stressed': [
                "Break down what's stressing you into smaller, manageable pieces",
                "Take a 5-minute break to do something you enjoy",
                "Try progressive muscle relaxation",
                "Make a list of what you can control vs. what you can't"
            ],
            'lonely': [
                "Reach out to someone you haven't talked to in a while",
                "Consider joining a group or community around your interests",
                "Try volunteering to connect with others",
                "Write a letter to someone you care about"
            ],
            'confused': [
                "Take time to sit with your feelings without judgment",
                "Try writing down your thoughts to clarify them",
                "Talk to someone you trust about what's on your mind",
                "Remember that it's okay to not have all the answers"
            ]
        }
        
        return suggestions.get(emotion, ["Remember that your feelings are valid and it's okay to not be okay sometimes."])

    def get_emotion_intensity(self, message: str, emotion: str) -> str:
        """Estimate emotion intensity (mild, moderate, severe)"""
        if emotion == 'neutral':
            return 'mild'
        
        # Count emotion-related words to estimate intensity
        patterns = self.compiled_patterns.get(emotion, [])
        total_matches = 0
        
        for pattern in patterns:
            matches = pattern.findall(message.lower())
            total_matches += len(matches)
        
        if total_matches >= 3:
            return 'severe'
        elif total_matches >= 1:
            return 'moderate'
        else:
            return 'mild'

    def enhance_with_ml(self, message: str) -> str:
        """
        Placeholder for ML-based emotion detection
        This would integrate with Hugging Face models in the future
        """
        # For now, return the keyword-based detection
        return self.detect_emotion(message) 