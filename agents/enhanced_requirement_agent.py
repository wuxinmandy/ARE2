from services.llm_service import llm_service
from services.knowledge_base import knowledge_base_service
import asyncio
import logging
from typing import Dict, List, Any

class EnhancedRequirementAgent:
    """Enhanced requirement analysis agent integrated with knowledge base"""
    
    def __init__(self):
        self.system_prompt = """You are an advanced requirements analyst with access to a comprehensive knowledge base. Your task is to help users refine and enhance their requirement descriptions using best practices and industry standards.

Please follow these principles:
1. Analyze user requirements using knowledge base insights
2. Identify gaps and missing information based on similar projects
3. Ask targeted questions derived from domain expertise
4. Provide structured, comprehensive requirement documents
5. Include both functional and non-functional requirements
6. Suggest best practices and potential risks

Format your responses clearly using Markdown, and always explain your reasoning for suggested improvements."""

    async def enhance_requirement_with_kb(self, user_input: str, model: str = None) -> Dict[str, Any]:
        """Enhance requirement analysis using knowledge base"""
        try:
            # 1. First query knowledge base for relevant suggestions
            kb_result = await knowledge_base_service.query_knowledge_base(user_input)
            
            # 2. Build enhanced prompt including knowledge base suggestions
            prompt = self._build_enhanced_prompt(user_input, kb_result)
            
            # 3. Use LLM to generate enhanced requirements
            enhanced_requirement = await llm_service.generate_completion(
                prompt, model, self.system_prompt
            )
            
            return {
                "success": True,
                "original_requirement": user_input,
                "enhanced_requirement": enhanced_requirement,
                "kb_suggestions": kb_result.get("suggestions", []),
                "clarification_questions": kb_result.get("questions", []),
                "knowledge_base_used": kb_result.get("success", False),
                "timestamp": "2024-01-01 12:00:00"
            }
            
        except Exception as e:
            logging.error(f"Enhanced requirement analysis failed: {e}")
            # Fall back to basic mode
            return await self._fallback_enhance_requirement(user_input, model)
    
    def _build_enhanced_prompt(self, user_input: str, kb_result: Dict[str, Any]) -> str:
        """Build enhanced prompt including knowledge base information"""
        base_prompt = f"""User's original requirement:
"{user_input}"

"""
        
        if kb_result.get("success") and kb_result.get("suggestions"):
            base_prompt += f"""Knowledge Base Suggestions:
{chr(10).join(f"- {suggestion}" for suggestion in kb_result["suggestions"])}

"""
        
        if kb_result.get("questions"):
            base_prompt += f"""Key Questions to Address:
{chr(10).join(f"- {question}" for question in kb_result["questions"])}

"""
        
        base_prompt += """Please analyze this requirement and provide:
1. A comprehensive, enhanced requirement document
2. Identification of any missing critical information
3. Specific recommendations based on industry best practices
4. Potential risks or challenges to consider
5. Suggested next steps for requirement clarification

Make your response detailed, structured, and actionable."""
        
        return base_prompt
    
    async def _fallback_enhance_requirement(self, user_input: str, model: str = None) -> Dict[str, Any]:
        """Fallback basic requirement enhancement method"""
        prompt = f"""User's original requirement:
"{user_input}"

Please help me analyze and enhance this requirement, providing a more detailed and complete requirement description. If key information is missing, please point out what needs further clarification."""

        try:
            enhanced_requirement = await llm_service.generate_completion(
                prompt, model, self.system_prompt
            )
            
            return {
                "success": True,
                "original_requirement": user_input,
                "enhanced_requirement": enhanced_requirement,
                "kb_suggestions": [],
                "clarification_questions": self._generate_basic_questions(user_input),
                "knowledge_base_used": False,
                "timestamp": "2024-01-01 12:00:00"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": "2024-01-01 12:00:00"
            }
    
    def _generate_basic_questions(self, requirement_text: str) -> List[str]:
        """Generate basic clarification questions"""
        return [
            "What is the main goal of this system?",
            "Who are the primary users?",
            "What is the expected number of users?",
            "Are there any special technical requirements?",
            "What are the project time and budget constraints?"
        ]
    
    async def clarify_requirement_with_kb(self, requirement: str, user_question: str, model: str = None) -> Dict[str, Any]:
        """Clarify requirements using knowledge base"""
        try:
            # Query knowledge base for relevant context
            context_query = f"{requirement}\n\nUser question: {user_question}"
            kb_result = await knowledge_base_service.query_knowledge_base(context_query)
            
            # Build clarification prompt
            prompt = f"""Current requirement document:
"{requirement}"

User question or additional information:
"{user_question}"

"""
            
            if kb_result.get("success") and kb_result.get("suggestions"):
                prompt += f"""Relevant knowledge base insights:
{chr(10).join(f"- {suggestion}" for suggestion in kb_result["suggestions"])}

"""
            
            prompt += """Please update and refine the requirement document based on the user's input and knowledge base insights. Ensure the new requirement is clearer, more complete, and follows best practices."""
            
            clarified_requirement = await llm_service.generate_completion(
                prompt, model, self.system_prompt
            )
            
            return {
                "success": True,
                "clarified_requirement": clarified_requirement,
                "additional_suggestions": kb_result.get("suggestions", []),
                "knowledge_base_used": kb_result.get("success", False),
                "timestamp": "2024-01-01 12:00:00"
            }
            
        except Exception as e:
            logging.error(f"Requirement clarification failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": "2024-01-01 12:00:00"
            }
    
    def get_smart_questions(self, requirement_text: str) -> List[str]:
        """Generate smart questions based on knowledge base"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            kb_result = loop.run_until_complete(
                knowledge_base_service.query_knowledge_base(requirement_text)
            )
            
            if kb_result.get("success"):
                return kb_result.get("questions", [])
            else:
                return self._generate_basic_questions(requirement_text)
                
        except Exception as e:
            logging.error(f"Failed to get smart questions: {e}")
            return self._generate_basic_questions(requirement_text)
        finally:
            loop.close()
    
    async def suggest_requirement_improvements(self, requirement_text: str) -> Dict[str, Any]:
        """Suggest requirement improvements"""
        try:
            kb_result = await knowledge_base_service.query_knowledge_base(requirement_text)
            
            improvements = {
                "completeness_score": self._assess_completeness(requirement_text),
                "missing_elements": self._identify_missing_elements(requirement_text),
                "suggestions": kb_result.get("suggestions", []),
                "best_practices": self._get_relevant_best_practices(requirement_text),
                "potential_risks": self._identify_potential_risks(requirement_text)
            }
            
            return {
                "success": True,
                "improvements": improvements
            }
            
        except Exception as e:
            logging.error(f"Failed to suggest improvements: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _assess_completeness(self, requirement_text: str) -> int:
        """Assess requirement completeness score (1-10)"""
        score = 5  # Base score
        text_lower = requirement_text.lower()
        
        # Check for key elements
        if any(word in text_lower for word in ['user', 'function', 'feature']):
            score += 1
        if any(word in text_lower for word in ['performance', 'security', 'scalability']):
            score += 1
        if any(word in text_lower for word in ['interface', 'ui', 'ux']):
            score += 1
        if len(requirement_text.split()) > 50:  # Detailed description
            score += 1
        if any(word in text_lower for word in ['technology', 'platform', 'system']):
            score += 1
        
        return min(10, max(1, score))
    
    def _identify_missing_elements(self, requirement_text: str) -> List[str]:
        """Identify missing requirement elements"""
        missing = []
        text_lower = requirement_text.lower()
        
        if not any(word in text_lower for word in ['user', 'customer', 'client']):
            missing.append("Target user identification")
        
        if not any(word in text_lower for word in ['function', 'feature', 'capability']):
            missing.append("Core functionality description")
        
        if not any(word in text_lower for word in ['performance', 'speed', 'load']):
            missing.append("Performance requirements")
        
        if not any(word in text_lower for word in ['security', 'authentication', 'authorization']):
            missing.append("Security requirements")
        
        if not any(word in text_lower for word in ['interface', 'ui', 'design']):
            missing.append("User interface requirements")
        
        return missing
    
    def _get_relevant_best_practices(self, requirement_text: str) -> List[str]:
        """Get relevant best practices based on requirement type"""
        practices = []
        text_lower = requirement_text.lower()
        
        if 'web' in text_lower:
            practices.extend([
                "Responsive design for mobile compatibility",
                "SEO optimization for search visibility",
                "Progressive web app features"
            ])
        
        if 'mobile' in text_lower or 'app' in text_lower:
            practices.extend([
                "Cross-platform compatibility consideration",
                "Offline functionality for poor network areas",
                "Battery optimization design"
            ])
        
        if 'ecommerce' in text_lower or 'shopping' in text_lower:
            practices.extend([
                "PCI DSS compliance for payment security",
                "Multi-payment gateway integration",
                "Inventory management system"
            ])
        
        # Generic best practices
        practices.extend([
            "User-centered design approach",
            "Scalable architecture design",
            "Comprehensive testing strategy"
        ])
        
        return practices[:5]  # Limit to 5 practices
    
    def _identify_potential_risks(self, requirement_text: str) -> List[str]:
        """Identify potential project risks"""
        risks = []
        text_lower = requirement_text.lower()
        
        if 'complex' in text_lower or 'integration' in text_lower:
            risks.append("Technical integration complexity")
        
        if 'real-time' in text_lower or 'live' in text_lower:
            risks.append("Real-time performance challenges")
        
        if 'payment' in text_lower or 'financial' in text_lower:
            risks.append("Financial transaction security risks")
        
        if 'scale' in text_lower or 'large' in text_lower:
            risks.append("Scalability and performance bottlenecks")
        
        # Generic risks
        risks.extend([
            "User adoption and change management",
            "Data privacy and compliance requirements",
            "Technical debt accumulation"
        ])
        
        return risks[:4]  # Limit to 4 risks

# Create global enhanced requirement agent instance
enhanced_requirement_agent = EnhancedRequirementAgent() 