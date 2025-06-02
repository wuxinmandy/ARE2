from services.llm_service import llm_service
import asyncio
import json
import re

class ReviewAgent:
    def __init__(self):
        self.knowledge_base = {
            "common_issues": [
                "Requirements are unclear or ambiguous",
                "Missing specific acceptance criteria",
                "Functional and non-functional requirements are confused",
                "Lack of user role definitions",
                "No clear priorities defined",
                "Technical implementation details are too complex",
                "Missing error handling and boundary conditions",
                "Performance requirements are unclear",
                "Insufficient security considerations",
                "Missing scalability requirements"
            ],
            "best_practices": [
                "Use user story format: As [role], I want [function], so that [value]",
                "Each requirement should be testable",
                "Avoid technical jargon, use business language",
                "Clearly define acceptance criteria",
                "Consider exceptions and boundary conditions",
                "Include non-functional requirements (performance, security, usability, etc.)",
                "Ensure requirement completeness and consistency"
            ]
        }

        self.system_prompt = """You are a senior requirements review expert. You need to review requirement documents according to software engineering best practices, identify potential issues and provide improvement suggestions.

Review focus:
1. Clarity and completeness of requirements
2. Testability and implementability
3. Consistency and unambiguity
4. Consideration of non-functional requirements
5. User experience and usability
6. Technical feasibility
7. Risk identification

Output format requirements:
- Return results in JSON format
- Include issues array, each issue contains:
  - type: "error" | "warning" | "suggestion"
  - text: Issue description
  - location: Location description in the original text
  - suggestion: Improvement suggestion
- Include summary field for overall evaluation
- Include score field with quality rating from 1-10

Please conduct the review and provide feedback in English. Ensure the returned JSON format is correct."""

    def review_requirement(self, requirement: str, model: str = None):
        """Review requirement document"""
        prompt = f"""Please review the following requirement document:

"{requirement}"

Based on software engineering best practices, identify issues and improvement points. Pay special attention to:
- Whether requirements are clear and specific
- Whether key information is missing
- Whether there are ambiguities or contradictions
- Whether non-functional requirements are sufficient
- Whether user experience is considered

Please return the review results in JSON format."""

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            review_result = loop.run_until_complete(
                llm_service.generate_completion(prompt, model, self.system_prompt)
            )
            
            # Try to parse JSON result
            try:
                parsed_result = json.loads(review_result)
            except json.JSONDecodeError:
                # If parsing fails, try to extract JSON part
                json_match = re.search(r'\{.*\}', review_result, re.DOTALL)
                if json_match:
                    try:
                        parsed_result = json.loads(json_match.group())
                    except:
                        parsed_result = self._create_fallback_result(review_result)
                else:
                    parsed_result = self._create_fallback_result(review_result)
            
            return {
                "success": True,
                "requirement": requirement,
                "review": parsed_result,
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

    def _create_fallback_result(self, review_text):
        """Create fallback review result structure"""
        return {
            "issues": [{
                "type": "warning",
                "text": "Review result parsing failed, please check original review content",
                "location": "Overall",
                "suggestion": "Please conduct review again"
            }],
            "summary": review_text,
            "score": 5
        }

    def highlight_issues(self, requirement: str, issues: list):
        """Add issue highlighting to requirement document"""
        highlighted_text = requirement
        
        # Add highlight markers for each issue
        for i, issue in enumerate(issues):
            if issue["type"] in ["error", "warning"]:
                # Simple keyword matching to determine highlight position
                keywords = self._extract_keywords(issue["text"])
                
                for keyword in keywords:
                    if keyword in highlighted_text:
                        # Use HTML markers for highlighting
                        highlighted_pattern = f'<mark style="background-color: #fef3c7; padding: 2px 4px; border-radius: 3px;" title="{issue["suggestion"]}">{keyword}</mark>'
                        highlighted_text = highlighted_text.replace(keyword, highlighted_pattern, 1)
        
        return highlighted_text

    def _extract_keywords(self, issue_text: str):
        """Extract keywords from issue description"""
        common_words = ["requirement", "function", "user", "system", "interface", "performance", "security", "test", "acceptance", "criteria"]
        return [word for word in common_words if word in issue_text.lower()]

    def get_knowledge_base(self):
        """Get knowledge base"""
        return {
            "success": True,
            "knowledge_base": self.knowledge_base,
            "timestamp": "2024-01-01 12:00:00"
        }

# Create global review agent instance
review_agent = ReviewAgent() 