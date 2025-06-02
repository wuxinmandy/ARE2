import openai
import anthropic
from config import Config
import time

class LLMService:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        
        # Initialize OpenAI client
        if Config.OPENAI_API_KEY:
            self.openai_client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # Initialize Anthropic client
        if Config.ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
    
    async def generate_completion(self, prompt: str, model: str = None, system_prompt: str = ""):
        """Generate AI response"""
        selected_model = model or Config.DEFAULT_MODEL
        
        try:
            if selected_model == "openai" and self.openai_client:
                return await self._openai_completion(prompt, system_prompt)
            elif selected_model == "anthropic" and self.anthropic_client:
                return await self._anthropic_completion(prompt, system_prompt)
            elif selected_model == "demo":
                return self._demo_completion(prompt, system_prompt)
            else:
                raise Exception(f"Model {selected_model} is not available or API key not configured")
        except Exception as e:
            raise Exception(f"LLM service error: {str(e)}")
    
    async def _openai_completion(self, prompt: str, system_prompt: str):
        """OpenAI GPT-4 completion"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.openai_client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    async def _anthropic_completion(self, prompt: str, system_prompt: str):
        """Anthropic Claude completion"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "user", "content": f"{system_prompt}\n\n{prompt}"})
        else:
            messages.append({"role": "user", "content": prompt})
        
        response = self.anthropic_client.messages.create(
            model=Config.ANTHROPIC_MODEL,
            max_tokens=2000,
            temperature=0.7,
            messages=messages
        )
        
        return response.content[0].text
    
    def _demo_completion(self, prompt: str, system_prompt: str):
        """Demo mode response"""
        # Simulate AI thinking time
        time.sleep(1)
        
        if "requirement" in prompt.lower() and "enhance" in system_prompt.lower():
            return """## Enhanced Requirements Document

### Project Overview
Based on your provided requirements, I recommend creating a comprehensive application system.

### Functional Requirements
1. **User Interface Design**
   - Modern, responsive design
   - Intuitive user experience
   - Mobile device support

2. **Core Feature Modules**
   - Data management functionality
   - User authentication system
   - Data analysis and reporting

3. **Technical Requirements**
   - Use modern technology stack
   - Ensure system security
   - Support scalable design

### Non-Functional Requirements
- **Performance Requirements**: Page load time < 3 seconds
- **Security Requirements**: Encrypted data storage, user authentication
- **Availability Requirements**: 99.9% system availability

### Acceptance Criteria
- All core functions operate normally
- Pass security testing
- User-friendly interface

### Recommended Technology Stack
- Frontend: Modern web framework
- Backend: Stable server technology
- Database: Relational database

This is a demo mode response. Please configure real API keys for more accurate requirement analysis."""
        
        elif "review" in system_prompt.lower():
            return """{
    "issues": [
        {
            "type": "warning",
            "text": "Requirements description may not be specific enough",
            "location": "Functional requirements section",
            "suggestion": "Recommend adding more detailed functional descriptions and user scenarios"
        },
        {
            "type": "suggestion", 
            "text": "Recommend adding performance metrics",
            "location": "Non-functional requirements",
            "suggestion": "Specify concrete performance requirements such as response time and concurrent users"
        }
    ],
    "summary": "Overall requirement structure is good, but there is room for improvement in specificity and testability. Recommend adding more detailed acceptance criteria.",
    "score": 7
}"""
        
        return "This is a demo mode response. Please configure API keys for real AI responses."

# Create global LLM service instance
llm_service = LLMService() 