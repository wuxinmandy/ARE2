from services.llm_service import llm_service
import asyncio

class RequirementAgent:
    def __init__(self):
        self.system_prompt = """You are a professional requirements analyst. Your task is to help users refine and enhance their requirement descriptions.

Please follow these principles:
1. Carefully analyze the simple requirements provided by users
2. Identify missing key information in the requirements
3. Ask specific questions to clarify requirements
4. Expand simple requirements into detailed, clear, actionable requirement documents
5. Ensure requirements include both functional and non-functional requirements
6. Use structured format to organize requirements

Format requirements:
- Use clear headings and subheadings
- List specific functional requirements
- Include user interface requirements
- Specify performance and security requirements
- Mention technology stack or platform requirements

Please respond in English and use Markdown format for better presentation."""

    def enhance_requirement(self, user_input: str, model: str = None):
        """Enhance user requirements"""
        prompt = f"""User's original requirement:
"{user_input}"

Please help me analyze and enhance this requirement, providing a more detailed and complete requirement description. If key information is missing, please point out what needs further clarification."""

        try:
            # Using synchronous approach for Streamlit environment
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            enhanced_requirement = loop.run_until_complete(
                llm_service.generate_completion(prompt, model, self.system_prompt)
            )
            
            return {
                "success": True,
                "original_requirement": user_input,
                "enhanced_requirement": enhanced_requirement,
                "timestamp": "2024-01-01 12:00:00"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": "2024-01-01 12:00:00"
            }
        finally:
            loop.close()

    def clarify_requirement(self, requirement: str, user_question: str, model: str = None):
        """Clarify requirements"""
        prompt = f"""Current requirement:
"{requirement}"

User question or additional information:
"{user_question}"

Please update and refine the requirement document based on the user's question or additional information. Ensure the new requirement is clearer and more complete."""

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            clarified_requirement = loop.run_until_complete(
                llm_service.generate_completion(prompt, model, self.system_prompt)
            )
            
            return {
                "success": True,
                "clarified_requirement": clarified_requirement,
                "timestamp": "2024-01-01 12:00:00"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": "2024-01-01 12:00:00"
            }
        finally:
            loop.close()

# Create global requirement agent instance
requirement_agent = RequirementAgent() 