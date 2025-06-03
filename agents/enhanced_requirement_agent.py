from services.llm_service import llm_service
from services.knowledge_base import knowledge_base_service
import asyncio
import logging
from typing import Dict, List, Any

class EnhancedRequirementAgent:
    """集成知识库的增强需求分析Agent"""
    
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
        """使用知识库增强需求分析"""
        try:
            # 1. 首先查询知识库获取相关建议
            kb_result = await knowledge_base_service.query_knowledge_base(user_input)
            
            # 2. 构建增强的prompt，包含知识库建议
            prompt = self._build_enhanced_prompt(user_input, kb_result)
            
            # 3. 使用LLM生成增强的需求
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
            # 退回到基础模式
            return await self._fallback_enhance_requirement(user_input, model)
    
    def _build_enhanced_prompt(self, user_input: str, kb_result: Dict[str, Any]) -> str:
        """构建包含知识库信息的增强prompt"""
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
        """备用的基础需求增强方法"""
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
        """生成基础澄清问题"""
        return [
            "这个系统的主要目标是什么？",
            "谁是主要用户？",
            "预期的用户数量是多少？",
            "有什么特殊的技术要求？",
            "项目的时间和预算限制是什么？"
        ]
    
    async def clarify_requirement_with_kb(self, requirement: str, user_question: str, model: str = None) -> Dict[str, Any]:
        """使用知识库澄清需求"""
        try:
            # 查询知识库获取相关上下文
            context_query = f"{requirement}\n\n用户问题：{user_question}"
            kb_result = await knowledge_base_service.query_knowledge_base(context_query)
            
            # 构建澄清prompt
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
        """基于知识库生成智能问题"""
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
        """建议需求改进"""
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
        """评估需求完整性（1-10分）"""
        score = 5  # 基础分
        
        # 检查关键要素
        key_elements = [
            "用户", "功能", "性能", "安全", "接口", "数据", "技术"
        ]
        
        for element in key_elements:
            if element in requirement_text:
                score += 0.7
        
        return min(10, int(score))
    
    def _identify_missing_elements(self, requirement_text: str) -> List[str]:
        """识别缺失的需求要素"""
        missing = []
        
        required_elements = {
            "目标用户": ["用户", "客户", "角色"],
            "核心功能": ["功能", "特性", "能力"],
            "性能要求": ["性能", "速度", "响应时间"],
            "安全要求": ["安全", "权限", "认证"],
            "技术栈": ["技术", "平台", "框架"],
            "数据要求": ["数据", "存储", "数据库"]
        }
        
        for element, keywords in required_elements.items():
            if not any(keyword in requirement_text for keyword in keywords):
                missing.append(element)
        
        return missing
    
    def _get_relevant_best_practices(self, requirement_text: str) -> List[str]:
        """获取相关最佳实践"""
        practices = []
        
        if "web" in requirement_text.lower():
            practices.extend([
                "采用响应式设计确保移动端兼容性",
                "实施HTTPS和安全认证机制",
                "优化页面加载速度和SEO",
                "设计清晰的用户导航和交互流程"
            ])
        
        if "mobile" in requirement_text.lower() or "app" in requirement_text.lower():
            practices.extend([
                "遵循平台设计规范（iOS HIG / Material Design）",
                "优化电池使用和内存管理",
                "实现离线功能和数据同步",
                "确保应用启动速度和响应性"
            ])
        
        return practices[:4]  # 限制返回数量
    
    def _identify_potential_risks(self, requirement_text: str) -> List[str]:
        """识别潜在风险"""
        risks = []
        
        if "大量用户" in requirement_text or "高并发" in requirement_text:
            risks.append("需要考虑系统可扩展性和负载均衡")
        
        if "支付" in requirement_text or "金融" in requirement_text:
            risks.append("需要满足金融合规和安全标准")
        
        if "数据" in requirement_text:
            risks.append("需要考虑数据隐私保护和GDPR合规")
        
        if "第三方" in requirement_text or "集成" in requirement_text:
            risks.append("第三方服务依赖可能影响系统稳定性")
        
        return risks

# 创建全局增强需求分析agent实例
enhanced_requirement_agent = EnhancedRequirementAgent() 