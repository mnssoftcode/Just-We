#!/usr/bin/env python3
"""
Simple test script for CalmSpace Mental Health AI Assistant
"""

import requests
import json
import time

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get('http://localhost:5000/api/health')
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {data['status']}")
            print(f"   Features: {data['features']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the app is running.")
        return False

def test_resources_endpoint():
    """Test the resources endpoint"""
    try:
        response = requests.get('http://localhost:5000/api/resources')
        if response.status_code == 200:
            data = response.json()
            print("✅ Resources endpoint working")
            print(f"   Crisis hotlines: {len(data['crisis_hotlines'])} available")
            print(f"   Mental health resources: {len(data['mental_health_resources'])} available")
            return True
        else:
            print(f"❌ Resources endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server.")
        return False

def test_chat_endpoint():
    """Test the chat endpoint with different types of messages"""
    test_cases = [
        {
            "name": "Normal greeting",
            "message": "Hello, how are you?",
            "expected_emotion": "neutral"
        },
        {
            "name": "Anxiety message",
            "message": "I'm feeling really anxious today",
            "expected_emotion": "anxious"
        },
        {
            "name": "Sadness message",
            "message": "I'm so sad and lonely",
            "expected_emotion": "sad"
        },
        {
            "name": "Stress message",
            "message": "I'm really stressed about work",
            "expected_emotion": "stressed"
        }
    ]
    
    for test_case in test_cases:
        try:
            response = requests.post('http://localhost:5000/api/chat', 
                                  json={'message': test_case['message'], 'history': []})
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {test_case['name']}: {data['emotion']}")
                print(f"   Crisis detected: {data['crisis_detected']}")
                print(f"   Response length: {len(data['message'])} characters")
            else:
                print(f"❌ {test_case['name']}: HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {test_case['name']}: Connection error")
            
        time.sleep(1)  # Small delay between requests

def test_crisis_detection():
    """Test crisis detection with high-risk messages"""
    crisis_test_cases = [
        {
            "name": "High crisis detection",
            "message": "I want to die",
            "expected_crisis": True
        },
        {
            "name": "Medium crisis detection",
            "message": "I feel worthless and hopeless",
            "expected_crisis": False  # Should be medium, not high
        },
        {
            "name": "Normal message",
            "message": "I had a good day today",
            "expected_crisis": False
        }
    ]
    
    for test_case in crisis_test_cases:
        try:
            response = requests.post('http://localhost:5000/api/chat', 
                                  json={'message': test_case['message'], 'history': []})
            
            if response.status_code == 200:
                data = response.json()
                crisis_detected = data.get('crisis_detected', False)
                crisis_level = data.get('crisis_level', 'low')
                
                if test_case['name'] == "High crisis detection" and crisis_detected:
                    print(f"✅ {test_case['name']}: Crisis properly detected")
                elif test_case['name'] == "Normal message" and not crisis_detected:
                    print(f"✅ {test_case['name']}: No false positive")
                else:
                    print(f"⚠️  {test_case['name']}: Crisis level {crisis_level}")
            else:
                print(f"❌ {test_case['name']}: HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {test_case['name']}: Connection error")
            
        time.sleep(1)

def main():
    """Run all tests"""
    print("🧪 Testing CalmSpace Mental Health AI Assistant")
    print("=" * 50)
    
    # Test basic endpoints
    print("\n1. Testing basic endpoints...")
    health_ok = test_health_endpoint()
    resources_ok = test_resources_endpoint()
    
    if not health_ok or not resources_ok:
        print("\n❌ Basic tests failed. Make sure the app is running with:")
        print("   cd backend")
        print("   python app.py")
        return
    
    # Test chat functionality
    print("\n2. Testing chat functionality...")
    test_chat_endpoint()
    
    # Test crisis detection
    print("\n3. Testing crisis detection...")
    test_crisis_detection()
    
    print("\n🎉 All tests completed!")
    print("\nTo run the application:")
    print("1. Set your OpenAI API key in .env file")
    print("2. cd backend")
    print("3. python app.py")
    print("4. Open http://localhost:5000 in your browser")

if __name__ == "__main__":
    main() 