#!/usr/bin/env python3
"""
Startup script for CalmSpace Mental Health AI Assistant
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import openai
        import requests
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("Creating .env file from template...")
        
        template_file = Path('env_template.txt')
        if template_file.exists():
            with open(template_file, 'r') as f:
                template_content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(template_content)
            
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file and add your OpenAI API key")
            return False
        else:
            print("❌ env_template.txt not found")
            return False
    
    # Check if OpenAI API key is set
    with open(env_file, 'r') as f:
        content = f.read()
        if 'your_openai_api_key_here' in content:
            print("⚠️  Please set your OpenAI API key in .env file")
            return False
    
    print("✅ Environment file configured")
    return True

def start_server():
    """Start the Flask server"""
    print("\n🚀 Starting CalmSpace Mental Health AI Assistant...")
    print("=" * 50)
    
    # Change to backend directory
    backend_dir = Path('backend')
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    os.chdir(backend_dir)
    
    # Start the server
    try:
        print("Starting Flask server...")
        print("The app will be available at: http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        subprocess.run([sys.executable, 'app.py'])
        return True
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def main():
    """Main startup function"""
    print("🌿 CalmSpace Mental Health AI Assistant")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check environment
    if not check_env_file():
        print("\n📝 Setup Instructions:")
        print("1. Edit the .env file")
        print("2. Add your OpenAI API key")
        print("3. Run this script again")
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main() 