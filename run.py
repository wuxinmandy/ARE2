#!/usr/bin/env python3
"""
AI Requirements Management System Startup Script
Run 'python run.py' to start the application
"""

import subprocess
import sys
import os

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python version check passed: {sys.version.split()[0]}")

def check_requirements():
    """Check and install dependencies"""
    print("📦 Checking dependencies...")
    
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("📥 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installation completed")

def check_env_file():
    """Check environment file"""
    if not os.path.exists('.env'):
        print("⚠️  .env file not found, creating default configuration")
        if os.path.exists('env.example'):
            import shutil
            shutil.copy('env.example', '.env')
            print("✅ Created .env file, please edit to configure your API keys")
        else:
            with open('.env', 'w', encoding='utf-8') as f:
                f.write("""# LLM API Keys (Optional, demo mode works without API keys)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Default LLM Model
DEFAULT_MODEL=demo

# OpenAI Configuration  
OPENAI_MODEL=gpt-4-turbo-preview

# Anthropic Configuration
ANTHROPIC_MODEL=claude-3-sonnet-20240229
""")
            print("✅ Created default .env file")
    else:
        print("✅ Environment configuration file exists")

def start_application():
    """Start Streamlit application"""
    print("\n🚀 Starting AI Requirements Management System...")
    print("🌐 Application will open automatically in your browser")
    print("📍 If it doesn't open automatically, visit: http://localhost:8501")
    print("\n💡 Tips:")
    print("   - System supports demo mode, no API keys required for basic experience")
    print("   - Configure real API keys for more accurate AI analysis")
    print("   - Press Ctrl+C to stop the application")
    print("\n" + "="*50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "main.py",
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Thank you for using AI Requirements Management System!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Startup failed: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print("🤖 AI Requirements Management System")
    print("="*50)
    
    check_python_version()
    check_requirements()
    check_env_file()
    start_application()

if __name__ == "__main__":
    main() 