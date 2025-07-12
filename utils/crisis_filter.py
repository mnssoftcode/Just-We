import re
from typing import List, Dict

class CrisisFilter:
    def __init__(self):
        """Initialize crisis detection with keywords and patterns"""
        
        # High crisis keywords - immediate intervention needed
        self.high_crisis_keywords = [
            'kill myself', 'want to die', 'end my life', 'suicide', 'kill me',
            'i want to die', 'i\'m worthless', 'no one cares', 'everyone would be better off',
            'i can\'t take it anymore', 'i give up', 'i\'m done', 'goodbye forever',
            'self harm', 'cut myself', 'hurt myself', 'bleed out', 'overdose',
            'take pills', 'swallow pills', 'hang myself', 'jump off', 'crash my car'
        ]
        
        # Medium crisis keywords - concerning but not immediate
        self.medium_crisis_keywords = [
            'i hate myself', 'i\'m a failure', 'i can\'t do this', 'i\'m hopeless',
            'nothing matters', 'i\'m alone', 'no one understands', 'i\'m tired of living',
            'i feel empty', 'i\'m broken', 'i can\'t cope', 'i\'m overwhelmed',
            'i don\'t want to be here', 'i wish i was dead', 'life is pointless'
        ]
        
        # Compile regex patterns for better matching
        self.high_crisis_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.high_crisis_keywords]
        self.medium_crisis_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.medium_crisis_keywords]

    def detect_crisis(self, message: str) -> str:
        """
        Detect crisis level in user message
        Returns: 'high', 'medium', or 'low'
        """
        message_lower = message.lower()
        
        # Check for high crisis indicators
        for pattern in self.high_crisis_patterns:
            if pattern.search(message_lower):
                return 'high'
        
        # Check for medium crisis indicators
        for pattern in self.medium_crisis_patterns:
            if pattern.search(message_lower):
                return 'medium'
        
        return 'low'

    def get_crisis_response(self) -> str:
        """Get appropriate crisis response"""
        return """I'm really concerned about what you're sharing with me, and I want you to know that your life has value and you matter. 

If you're having thoughts of harming yourself, please know that help is available right now:

🆘 **Immediate Help:**
• National Suicide Prevention Lifeline: 988 (available 24/7)
• Crisis Text Line: Text HOME to 741741
• Emergency Services: 911

You don't have to go through this alone. There are people who care about you and want to help. Please reach out to one of these resources, or talk to someone you trust - a friend, family member, teacher, or mental health professional.

Your feelings are valid, and it's okay to ask for help. You deserve support and care. I'm here to listen, but please also connect with someone who can provide immediate support.

Would you like to talk more about what's going on? I'm here to listen."""

    def get_medium_crisis_response(self) -> str:
        """Get response for medium crisis level"""
        return """I can hear that you're really struggling right now, and I want you to know that your feelings are valid. It sounds like you're going through a very difficult time.

While I'm here to listen and support you, it might be helpful to also talk to someone who can provide more specialized support:

💙 **Support Options:**
• Talk to a trusted friend or family member
• Consider speaking with a mental health professional
• Call a helpline to talk to someone trained to help

You don't have to face this alone. Sometimes the bravest thing we can do is ask for help. Your feelings matter, and you deserve support.

Would you like to talk more about what's going on? I'm here to listen."""

    def should_escalate(self, message: str) -> bool:
        """Determine if message requires immediate escalation"""
        crisis_level = self.detect_crisis(message)
        return crisis_level == 'high'

    def get_escalation_guidance(self) -> Dict[str, str]:
        """Get guidance for crisis escalation"""
        return {
            'immediate_actions': [
                'Stay with the person if possible',
                'Remove any means of self-harm',
                'Call emergency services if immediate danger',
                'Contact crisis hotline'
            ],
            'hotlines': {
                'suicide_prevention': '988',
                'crisis_text': 'Text HOME to 741741',
                'emergency': '911'
            },
            'warning_signs': [
                'Talking about wanting to die',
                'Looking for ways to kill themselves',
                'Talking about feeling hopeless',
                'Talking about being a burden',
                'Increasing alcohol or drug use',
                'Acting anxious or agitated',
                'Sleeping too little or too much',
                'Withdrawing or feeling isolated'
            ]
        } 