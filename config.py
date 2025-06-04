import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Default Model
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "openai")
    
    # OpenAI Configuration
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    
    # Anthropic Configuration
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
    
    # Application Configuration
    APP_TITLE = "BA Copilot"
    APP_DESCRIPTION = "Intelligent Business Analysis Assistant powered by Generative AI"
    
    @classmethod
    def get_available_models(cls):
        """Get list of available models"""
        models = []
        
        if cls.OPENAI_API_KEY:
            models.append({
                "id": "openai",
                "name": "OpenAI GPT-4",
                "enabled": True,
                "description": "OpenAI's GPT-4 model, suitable for complex requirement analysis"
            })
        
        if cls.ANTHROPIC_API_KEY:
            models.append({
                "id": "anthropic", 
                "name": "Anthropic Claude",
                "enabled": True,
                "description": "Anthropic's Claude model, excellent at logical reasoning"
            })
        
        if not models:
            models.append({
                "id": "demo",
                "name": "Demo Mode",
                "enabled": True,
                "description": "Demo mode, no API key required"
            })
            
        return models 