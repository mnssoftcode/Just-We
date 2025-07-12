import pandas as pd
import numpy as np
import json
import re
from typing import List, Dict, Optional, Tuple
import os

class DatasetHandler:
    def __init__(self):
        """Initialize dataset handler for Fast Chatbot Strategy"""
        self.datasets = {}
        self.load_datasets()
        
    def load_datasets(self):
        """Load all datasets and prepare them for fast searching"""
        try:
            # Get the correct path to dataset files
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dataset_dir = os.path.join(current_dir, '..', 'dataset')
            
            # Load EmotionChat dataset
            emotion_path = os.path.join(dataset_dir, 'EmotionChat_69k.csv')
            emotion_df = pd.read_csv(emotion_path)
            self.datasets['emotion'] = emotion_df
            print(f"✅ Loaded EmotionChat dataset: {len(emotion_df)} entries")
            
            # Load MentalChat datasets
            mental_6k_path = os.path.join(dataset_dir, 'MentalChat_6K.csv')
            mental_10k_path = os.path.join(dataset_dir, 'MentalChat_10K.csv')
            
            mental_6k_df = pd.read_csv(mental_6k_path)
            mental_10k_df = pd.read_csv(mental_10k_path)
            
            # Combine mental health datasets
            mental_df = pd.concat([mental_6k_df, mental_10k_df], ignore_index=True)
            self.datasets['mental'] = mental_df
            print(f"✅ Loaded MentalChat datasets: {len(mental_df)} total entries")
            
        except Exception as e:
            print(f"❌ Error loading datasets: {e}")
            self.datasets = {}
    
    def find_best_match(self, user_message: str, emotion: str = None, threshold: float = 0.3) -> Optional[Dict]:
        """
        Find the best matching response from datasets using keyword matching
        Returns: Dict with 'response', 'source', 'similarity_score', 'dataset'
        """
        best_match = None
        best_score = 0
        
        # Clean user message
        clean_message = self._clean_text(user_message)
        user_keywords = set(clean_message.split())
        
        # Search in emotion dataset if emotion is detected
        if emotion and emotion != 'neutral':
            emotion_match = self._search_emotion_dataset(clean_message, user_keywords, emotion, threshold)
            if emotion_match and emotion_match['similarity_score'] > best_score:
                best_match = emotion_match
                best_score = emotion_match['similarity_score']
        
        # Search in mental health dataset
        mental_match = self._search_mental_dataset(clean_message, user_keywords, threshold)
        if mental_match and mental_match['similarity_score'] > best_score:
            best_match = mental_match
            best_score = mental_match['similarity_score']
        
        return best_match if best_score >= threshold else None
    
    def _search_emotion_dataset(self, user_message: str, user_keywords: set, emotion: str, threshold: float) -> Optional[Dict]:
        """Search emotion dataset for similar situations using keyword matching"""
        try:
            df = self.datasets['emotion']
            
            # Filter by emotion if specified
            emotion_filter = df['emotion'].str.contains(emotion, case=False, na=False)
            filtered_df = df[emotion_filter]
            
            if len(filtered_df) == 0:
                return None
            
            best_score = 0
            best_row = None
            
            # Search through filtered dataset
            for idx, row in filtered_df.iterrows():
                # Combine situation and emotion for search
                search_text = f"{row['Situation']} {row['emotion']}"
                search_keywords = set(self._clean_text(search_text).split())
                
                # Calculate keyword overlap
                overlap = len(user_keywords.intersection(search_keywords))
                total_keywords = len(user_keywords.union(search_keywords))
                
                if total_keywords > 0:
                    similarity = overlap / total_keywords
                    if similarity > best_score:
                        best_score = similarity
                        best_row = row
            
            if best_score >= threshold and best_row is not None:
                return {
                    'response': self._extract_response_from_emotion(best_row),
                    'source': 'emotion_dataset',
                    'similarity_score': float(best_score),
                    'dataset': 'emotion',
                    'emotion': best_row['emotion']
                }
            
        except Exception as e:
            print(f"Error searching emotion dataset: {e}")
        
        return None
    
    def _search_mental_dataset(self, user_message: str, user_keywords: set, threshold: float) -> Optional[Dict]:
        """Search mental health dataset for similar questions using keyword matching"""
        try:
            df = self.datasets['mental']
            
            best_score = 0
            best_row = None
            
            # Search through dataset
            for idx, row in df.iterrows():
                search_text = row['input']
                search_keywords = set(self._clean_text(search_text).split())
                
                # Calculate keyword overlap
                overlap = len(user_keywords.intersection(search_keywords))
                total_keywords = len(user_keywords.union(search_keywords))
                
                if total_keywords > 0:
                    similarity = overlap / total_keywords
                    if similarity > best_score:
                        best_score = similarity
                        best_row = row
            
            if best_score >= threshold and best_row is not None:
                return {
                    'response': best_row['output'],
                    'source': 'mental_health_dataset',
                    'similarity_score': float(best_score),
                    'dataset': 'mental',
                    'input': best_row['input']
                }
            
        except Exception as e:
            print(f"Error searching mental dataset: {e}")
        
        return None
    
    def _extract_response_from_emotion(self, row) -> str:
        """Extract the agent response from emotion dialogue"""
        try:
            dialogue = row['empathetic_dialogues']
            # Look for "Agent :" pattern
            if 'Agent :' in dialogue:
                agent_part = dialogue.split('Agent :')[1].strip()
                return agent_part
            else:
                # Fallback: return the whole dialogue
                return dialogue
        except:
            return str(row['empathetic_dialogues'])
    
    def _clean_text(self, text: str) -> str:
        """Clean text for better matching"""
        # Remove special characters and normalize
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def get_dataset_stats(self) -> Dict:
        """Get statistics about loaded datasets"""
        stats = {}
        
        for dataset_name, df in self.datasets.items():
            stats[dataset_name] = {
                'total_entries': len(df),
                'columns': list(df.columns)
            }
        
        return stats
    
    def get_fallback_response(self, emotion: str = None) -> str:
        """Get a fallback response when no good match is found"""
        fallback_responses = {
            'anxious': [
                "I can sense you're feeling anxious right now. That's completely okay. Let's take a moment together - try taking three deep breaths with me. Inhale slowly for 4 counts, hold for 4, then exhale for 4. How does that feel?",
                "Anxiety can be really overwhelming. Remember, it's okay to feel this way. Sometimes talking about what's on your mind can help. Would you like to share what's making you feel anxious?"
            ],
            'sad': [
                "I'm so sorry you're feeling sad right now. Your feelings are valid, and it's okay to not be okay. Sometimes just acknowledging how we feel can be the first step toward feeling better. Would you like to talk about what's on your mind?",
                "Sadness can feel really heavy and isolating. Remember that you're not alone in feeling this way. Sometimes the simple act of expressing our feelings can help lighten the load a little. I'm here to listen."
            ],
            'stressed': [
                "Stress can feel really overwhelming, like everything is piling up at once. It's okay to feel this way. Sometimes breaking things down into smaller steps can help. What's one small thing you could do right now that might help you feel a little better?",
                "I can hear how stressed you're feeling. That's completely understandable. Sometimes the best thing we can do is give ourselves permission to take a break. Even just a few minutes of deep breathing can help reset our nervous system."
            ],
            'lonely': [
                "Loneliness can be one of the hardest feelings to sit with. It's completely normal to feel this way, and your feelings are valid. Sometimes reaching out to someone we trust, even just to say hello, can help. Is there someone you could reach out to?",
                "I hear how lonely you're feeling right now. That's a really difficult place to be. Remember that you're not alone in feeling this way - many people experience loneliness, even when surrounded by others."
            ],
            'default': [
                "I'm here to listen and support you. Sometimes just talking about what's on our minds can help us feel a little better. Would you like to share what's going on?",
                "I hear you, and I want you to know that your feelings are valid. It's okay to not be okay sometimes. I'm here to listen whenever you're ready to talk."
            ]
        }
        
        if emotion and emotion in fallback_responses:
            import random
            return random.choice(fallback_responses[emotion])
        else:
            import random
            return random.choice(fallback_responses['default']) 