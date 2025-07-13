import re
from typing import List, Dict, Optional
from datetime import datetime

class CrisisFilter:
    def __init__(self):
        """Initialize enhanced crisis detection with multi-level assessment"""
        
        # Enhanced crisis keywords with intensity levels
        self.crisis_patterns = {
            'immediate': [
                r'\b(kill myself|want to die|end my life|suicide|kill me)\b',
                r'\b(i want to die|i\'m worthless|no one cares|everyone would be better off)\b',
                r'\b(i can\'t take it anymore|i give up|i\'m done|goodbye forever)\b',
                r'\b(self harm|cut myself|hurt myself|bleed out|overdose)\b',
                r'\b(take pills|swallow pills|hang myself|jump off|crash my car)\b',
                r'\b(going to end it|final goodbye|last message|never see me again)\b'
            ],
            'high': [
                r'\b(i hate myself|i\'m a failure|i can\'t do this|i\'m hopeless)\b',
                r'\b(nothing matters|i\'m alone|no one understands|i\'m tired of living)\b',
                r'\b(i feel empty|i\'m broken|i can\'t cope|i\'m overwhelmed)\b',
                r'\b(i don\'t want to be here|i wish i was dead|life is pointless)\b',
                r'\b(thinking about suicide|suicidal thoughts|want to disappear)\b',
                r'\b(no reason to live|better off dead|no point in trying)\b'
            ],
            'medium': [
                r'\b(i\'m struggling|having a hard time|feeling down|not okay)\b',
                r'\b(don\'t know how to cope|feeling overwhelmed|really stressed)\b',
                r'\b(lonely|isolated|no one to talk to|feeling lost)\b',
                r'\b(anxious|worried|scared|afraid|panic)\b',
                r'\b(depressed|sad|hopeless|worthless|empty)\b',
                r'\b(need help|can\'t handle this|breaking point)\b'
            ],
            'low': [
                r'\b(not feeling great|having a rough day|feeling off)\b',
                r'\b(stressed|worried|concerned|uneasy)\b',
                r'\b(sad|down|blue|melancholy)\b',
                r'\b(lonely|missing someone|wish I had company)\b'
            ]
        }
        
        # Compile regex patterns
        self.compiled_patterns = {}
        for level, patterns in self.crisis_patterns.items():
            self.compiled_patterns[level] = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        
        # Crisis escalation tracking
        self.crisis_history = []
        self.max_history = 10
        
        # Crisis resources by level
        self.crisis_resources = {
            'immediate': {
                'hotlines': {
                    'suicide_prevention': '988',
                    'crisis_text': 'Text HOME to 741741',
                    'emergency': '911'
                },
                'actions': [
                    'Call 988 immediately',
                    'Text HOME to 741741',
                    'Call 911 if immediate danger',
                    'Remove any means of self-harm',
                    'Stay with the person if possible'
                ]
            },
            'high': {
                'hotlines': {
                    'suicide_prevention': '988',
                    'crisis_text': 'Text HOME to 741741',
                    'mental_health': '1-800-273-8255'
                },
                'actions': [
                    'Call a crisis hotline',
                    'Talk to a mental health professional',
                    'Reach out to a trusted person',
                    'Consider emergency services if needed'
                ]
            },
            'medium': {
                'hotlines': {
                    'mental_health': '1-800-273-8255',
                    'crisis_text': 'Text HOME to 741741'
                },
                'actions': [
                    'Talk to someone you trust',
                    'Consider professional help',
                    'Practice self-care',
                    'Reach out to support networks'
                ]
            },
            'low': {
                'hotlines': {
                    'mental_health': '1-800-273-8255'
                },
                'actions': [
                    'Practice self-care',
                    'Talk to a friend or family member',
                    'Consider talking to a counselor',
                    'Engage in activities you enjoy'
                ]
            }
        }

    def detect_crisis(self, message: str) -> Dict[str, any]:
        """
        Enhanced crisis detection with multi-level assessment
        Returns: Dict with 'level', 'confidence', 'indicators', 'escalation_needed'
        """
        message_lower = message.lower()
        crisis_scores = {}
        indicators = []
        
        # Score each crisis level
        for level, patterns in self.compiled_patterns.items():
            score = 0
            level_indicators = []
            
            for pattern in patterns:
                matches = pattern.findall(message_lower)
                if matches:
                    score += len(matches)
                    level_indicators.extend(matches)
            
            if score > 0:
                crisis_scores[level] = score
                indicators.extend(level_indicators)
        
        # Determine crisis level
        if crisis_scores:
            # Prioritize higher levels
            if 'immediate' in crisis_scores:
                crisis_level = 'immediate'
                confidence = min(crisis_scores['immediate'] / 2, 1.0)
            elif 'high' in crisis_scores:
                crisis_level = 'high'
                confidence = min(crisis_scores['high'] / 3, 1.0)
            elif 'medium' in crisis_scores:
                crisis_level = 'medium'
                confidence = min(crisis_scores['medium'] / 2, 1.0)
            else:
                crisis_level = 'low'
                confidence = min(crisis_scores['low'] / 2, 1.0)
        else:
            crisis_level = 'none'
            confidence = 0.0
        
        # Update crisis history
        self._update_crisis_history(crisis_level, confidence, indicators)
        
        # Determine if escalation is needed
        escalation_needed = self._assess_escalation_needed()
        
        return {
            'level': crisis_level,
            'confidence': confidence,
            'indicators': indicators,
            'escalation_needed': escalation_needed,
            'trend': self._get_crisis_trend(),
            'resources': self._get_crisis_resources(crisis_level)
        }

    def _update_crisis_history(self, level: str, confidence: float, indicators: List[str]):
        """Update crisis history for trend analysis"""
        timestamp = datetime.now()
        self.crisis_history.append({
            'level': level,
            'confidence': confidence,
            'indicators': indicators,
            'timestamp': timestamp
        })
        
        # Keep only recent history
        if len(self.crisis_history) > self.max_history:
            self.crisis_history.pop(0)

    def _get_crisis_trend(self) -> str:
        """Analyze crisis trend over recent messages"""
        if len(self.crisis_history) < 3:
            return 'stable'
        
        recent_levels = [entry['level'] for entry in self.crisis_history[-3:]]
        
        # Check for escalating trend
        if any(level in ['immediate', 'high'] for level in recent_levels):
            return 'escalating'
        elif recent_levels.count('none') >= 2:
            return 'improving'
        else:
            return 'stable'

    def _assess_escalation_needed(self) -> bool:
        """Determine if immediate escalation is needed"""
        if not self.crisis_history:
            return False
        
        recent_entries = self.crisis_history[-3:]
        
        # Check for immediate crisis indicators
        for entry in recent_entries:
            if entry['level'] in ['immediate', 'high']:
                return True
        
        # Check for escalating pattern
        if self._get_crisis_trend() == 'escalating':
            return True
        
        return False

    def _get_crisis_resources(self, level: str) -> Dict[str, any]:
        """Get appropriate resources for crisis level"""
        return self.crisis_resources.get(level, self.crisis_resources['low'])

    def get_crisis_response(self, crisis_data: Dict) -> str:
        """Get enhanced crisis response based on level and context"""
        level = crisis_data['level']
        trend = crisis_data.get('trend', 'stable')
        resources = crisis_data.get('resources', {})
        
        base_responses = {
            'immediate': """🚨 **I'm very concerned about what you're sharing with me, and I want you to know that your life has value and you matter.**

If you're having thoughts of harming yourself, please know that help is available right now:

🆘 **Immediate Help:**
• **National Suicide Prevention Lifeline: 988** (available 24/7)
• **Crisis Text Line: Text HOME to 741741**
• **Emergency Services: 911**

You don't have to go through this alone. There are people who care about you and want to help. Please reach out to one of these resources immediately, or talk to someone you trust - a friend, family member, teacher, or mental health professional.

Your feelings are valid, and it's okay to ask for help. You deserve support and care.""",
            
            'high': """I'm really concerned about what you're sharing with me, and I want you to know that your life has value and you matter.

If you're having thoughts of harming yourself, please know that help is available:

🆘 **Help Available:**
• National Suicide Prevention Lifeline: 988 (available 24/7)
• Crisis Text Line: Text HOME to 741741
• Emergency Services: 911

You don't have to go through this alone. There are people who care about you and want to help. Please reach out to one of these resources, or talk to someone you trust - a friend, family member, teacher, or mental health professional.

Your feelings are valid, and it's okay to ask for help. You deserve support and care.""",
            
            'medium': """I can hear that you're really struggling right now, and I want you to know that your feelings are valid. It sounds like you're going through a very difficult time.

While I'm here to listen and support you, it might be helpful to also talk to someone who can provide more specialized support:

💙 **Support Options:**
• Talk to a trusted friend or family member
• Consider speaking with a mental health professional
• Call a helpline to talk to someone trained to help

You don't have to face this alone. Sometimes the bravest thing we can do is ask for help. Your feelings matter, and you deserve support.""",
            
            'low': """I can hear that you're having a difficult time, and I want you to know that your feelings are valid. It's okay to not be okay sometimes.

While I'm here to listen and support you, consider reaching out to someone you trust or a mental health professional if these feelings persist.

Remember that you don't have to go through difficult times alone. Your feelings matter, and you deserve support.""",
            
            'none': """I'm here to listen and support you. Sometimes just talking about what's on our minds can help us feel a little better. Would you like to share what's going on?"""
        }
        
        response = base_responses.get(level, base_responses['none'])
        
        # Add trend information
        if trend == 'escalating':
            response += "\n\n⚠️ **Note:** I've noticed your distress seems to be increasing. Please consider reaching out for professional help if these feelings continue or worsen."
        elif trend == 'improving':
            response += "\n\n💚 **Note:** I'm glad to see you're doing better. Remember that it's okay to reach out for support whenever you need it."
        
        return response

    def get_escalation_guidance(self) -> Dict[str, any]:
        """Get comprehensive guidance for crisis escalation"""
        return {
            'immediate_actions': [
                'Stay with the person if possible',
                'Remove any means of self-harm',
                'Call emergency services if immediate danger',
                'Contact crisis hotline',
                'Ensure the person is not alone'
            ],
            'warning_signs': [
                'Talking about wanting to die',
                'Looking for ways to kill themselves',
                'Talking about feeling hopeless',
                'Talking about being a burden',
                'Increasing alcohol or drug use',
                'Acting anxious or agitated',
                'Sleeping too little or too much',
                'Withdrawing or feeling isolated',
                'Showing rage or talking about seeking revenge',
                'Displaying extreme mood swings'
            ],
            'hotlines': {
                'suicide_prevention': '988',
                'crisis_text': 'Text HOME to 741741',
                'emergency': '911',
                'mental_health': '1-800-273-8255'
            },
            'resources': {
                'immediate': 'Call 988 or 911 immediately',
                'high': 'Call crisis hotline or mental health professional',
                'medium': 'Consider professional help',
                'low': 'Talk to someone you trust'
            }
        }

    def should_escalate(self, message: str) -> bool:
        """Determine if message requires immediate escalation"""
        crisis_data = self.detect_crisis(message)
        return crisis_data['escalation_needed']

    def get_crisis_summary(self) -> Dict[str, any]:
        """Get summary of recent crisis patterns"""
        if not self.crisis_history:
            return {'trend': 'stable', 'level': 'none', 'escalation_needed': False}
        
        recent_levels = [entry['level'] for entry in self.crisis_history[-5:]]
        
        # Find most severe recent level
        level_priority = {'immediate': 4, 'high': 3, 'medium': 2, 'low': 1, 'none': 0}
        max_level = max(recent_levels, key=lambda x: level_priority.get(x, 0))
        
        # Check for escalation
        escalation_needed = any(level in ['immediate', 'high'] for level in recent_levels[-3:])
        
        return {
            'trend': self._get_crisis_trend(),
            'level': max_level,
            'escalation_needed': escalation_needed,
            'recent_levels': recent_levels,
            'confidence': sum(entry['confidence'] for entry in self.crisis_history[-5:]) / len(self.crisis_history[-5:]) if self.crisis_history else 0
        } 