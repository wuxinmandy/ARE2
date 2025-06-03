import os
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import asyncio
from dataclasses import dataclass

try:
    from lightrag import LightRAG, QueryParam
    from lightrag.llm import gpt_4o_mini_complete, gpt_4o_complete
    from lightrag.utils import EmbeddingFunc
    import pandas as pd
    LIGHTRAG_AVAILABLE = True
except ImportError:
    LIGHTRAG_AVAILABLE = False
    logging.warning("LightRAG not available. Knowledge base features will be disabled.")

from config import Config

@dataclass
class RequirementTemplate:
    """需求模板数据结构"""
    category: str
    subcategory: str
    template: str
    questions: List[str]
    examples: List[str]
    best_practices: List[str]

class KnowledgeBaseService:
    """基于LightRAG的知识库服务"""
    
    def __init__(self):
        self.working_dir = Path("./rag_storage")
        self.working_dir.mkdir(exist_ok=True)
        
        self.rag = None
        self.templates_data = {}
        self.is_initialized = False
        
        if LIGHTRAG_AVAILABLE:
            self._initialize_rag()
            self._load_knowledge_base()
    
    def _initialize_rag(self):
        """初始化LightRAG系统"""
        try:
            # 简化的LLM模型函数
            async def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs) -> str:
                # 这里使用我们现有的LLM服务
                from services.llm_service import llm_service
                full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
                return await llm_service.generate_completion(full_prompt, "demo")
            
            # 简化的嵌入函数
            async def embedding_func(texts: list[str]):
                # 返回模拟的嵌入向量
                import numpy as np
                return np.random.rand(len(texts), 768).astype(np.float32)
            
            # 初始化LightRAG
            self.rag = LightRAG(
                working_dir=str(self.working_dir),
                llm_model_func=llm_model_func,
                embedding_func=EmbeddingFunc(
                    embedding_dim=768,
                    max_token_size=8192,
                    func=embedding_func
                ),
            )
            
            self.is_initialized = True
            logging.info("LightRAG initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize LightRAG: {e}")
            self.is_initialized = False
    
    def _load_knowledge_base(self):
        """加载需求分析知识库"""
        if not self.is_initialized:
            return
            
        # 预定义的需求分析知识库数据
        knowledge_data = self._get_requirements_knowledge()
        
        try:
            # 将知识库数据插入到LightRAG中
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            for category, content in knowledge_data.items():
                loop.run_until_complete(self.rag.ainsert(content))
            
            logging.info("Knowledge base loaded successfully")
            
        except Exception as e:
            logging.error(f"Failed to load knowledge base: {e}")
        finally:
            loop.close()
    
    def _get_requirements_knowledge(self) -> Dict[str, str]:
        """获取需求分析知识库数据"""
        return {
            "web_applications": """
            Web应用需求分析指南：
            
            功能需求：
            - 用户注册和登录系统
            - 用户角色和权限管理
            - 数据CRUD操作
            - 搜索和过滤功能
            - 文件上传和下载
            - 通知系统
            - 报表和数据可视化
            
            非功能需求：
            - 响应时间：页面加载时间<3秒
            - 并发用户：支持1000+同时在线用户
            - 安全性：HTTPS、SQL注入防护、XSS防护
            - 兼容性：支持主流浏览器
            - 可用性：99.9%正常运行时间
            
            技术架构：
            - 前端：React/Vue/Angular
            - 后端：Node.js/Python/Java
            - 数据库：MySQL/PostgreSQL/MongoDB
            - 部署：Docker、云服务
            
            需要明确的问题：
            1. 预期用户数量和并发量？
            2. 需要支持哪些设备和浏览器？
            3. 数据安全和隐私要求？
            4. 是否需要第三方集成？
            5. 维护和更新频率？
            """,
            
            "mobile_applications": """
            移动应用需求分析指南：
            
            功能需求：
            - 用户界面设计和用户体验
            - 离线功能支持
            - 推送通知
            - 相机和媒体功能
            - GPS定位服务
            - 社交分享功能
            - 支付集成
            
            非功能需求：
            - 启动时间：<3秒
            - 电池优化
            - 内存使用优化
            - 网络适应性（2G/3G/4G/5G/WiFi）
            - 应用大小控制
            
            平台考虑：
            - iOS vs Android vs 跨平台
            - 最低支持版本
            - 设备适配（手机、平板）
            - 应用商店发布要求
            
            需要明确的问题：
            1. 目标平台（iOS/Android/跨平台）？
            2. 是否需要离线功能？
            3. 需要哪些设备权限？
            4. 推送通知策略？
            5. 应用商店发布计划？
            """,
            
            "e_commerce": """
            电商系统需求分析指南：
            
            核心功能：
            - 商品管理（分类、库存、价格）
            - 购物车和订单流程
            - 支付系统集成
            - 用户账户管理
            - 评价和评论系统
            - 促销和优惠券
            - 物流跟踪
            
            管理功能：
            - 商家管理后台
            - 订单管理
            - 财务报表
            - 客户服务工具
            - 数据分析仪表板
            
            安全要求：
            - PCI DSS合规
            - 用户数据保护
            - 防欺诈机制
            - 安全支付处理
            
            需要明确的问题：
            1. B2C、B2B还是B2B2C模式？
            2. 支持的支付方式？
            3. 配送范围和物流合作？
            4. 多语言和多货币支持？
            5. 移动端需求？
            """,
            
            "data_management": """
            数据管理系统需求分析指南：
            
            数据功能：
            - 数据收集和导入
            - 数据清洗和验证
            - 数据存储和备份
            - 数据查询和检索
            - 数据可视化
            - 数据导出和报告
            
            数据质量：
            - 数据准确性验证
            - 重复数据处理
            - 数据完整性检查
            - 数据更新机制
            
            安全和合规：
            - 数据加密
            - 访问控制
            - 审计日志
            - GDPR/隐私法规合规
            
            需要明确的问题：
            1. 数据来源和格式？
            2. 数据量级和增长预期？
            3. 实时性要求？
            4. 数据保留政策？
            5. 集成其他系统的需求？
            """
        }
    
    async def query_knowledge_base(self, requirement_text: str, query_mode: str = "hybrid") -> Dict[str, Any]:
        """查询知识库获取相关建议"""
        if not self.is_initialized or not self.rag:
            return {
                "success": False,
                "error": "Knowledge base not initialized",
                "suggestions": [],
                "questions": []
            }
        
        try:
            # 构建查询
            query = f"分析以下需求并提供改进建议：{requirement_text}"
            
            # 查询知识库
            response = await self.rag.aquery(
                query, 
                param=QueryParam(mode=query_mode)
            )
            
            # 解析响应并生成建议
            suggestions = self._parse_suggestions(response)
            questions = self._generate_clarification_questions(requirement_text, response)
            
            return {
                "success": True,
                "suggestions": suggestions,
                "questions": questions,
                "raw_response": response
            }
            
        except Exception as e:
            logging.error(f"Knowledge base query failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "suggestions": [],
                "questions": []
            }
    
    def _parse_suggestions(self, response: str) -> List[str]:
        """解析知识库响应生成建议"""
        suggestions = []
        
        # 简单的响应解析逻辑
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line and ('建议' in line or '推荐' in line or '应该' in line):
                suggestions.append(line)
        
        # 如果没有找到建议，返回通用建议
        if not suggestions:
            suggestions = [
                "建议明确目标用户群体和使用场景",
                "需要详细说明核心功能和用户流程",
                "考虑非功能需求如性能、安全性、可扩展性",
                "明确技术栈和部署环境要求"
            ]
        
        return suggestions[:5]  # 限制返回5个建议
    
    def _generate_clarification_questions(self, requirement_text: str, context: str) -> List[str]:
        """基于需求和上下文生成澄清问题"""
        questions = []
        
        # 基于需求类型生成问题
        requirement_lower = requirement_text.lower()
        
        if 'web' in requirement_lower or '网站' in requirement_lower:
            questions.extend([
                "这个Web应用的主要用户群体是谁？",
                "预期的并发用户数量是多少？",
                "需要支持哪些浏览器和设备？",
                "是否需要移动端适配？"
            ])
        
        if 'mobile' in requirement_lower or '移动' in requirement_lower or 'app' in requirement_lower:
            questions.extend([
                "需要开发iOS版本、Android版本还是跨平台应用？",
                "应用是否需要离线功能？",
                "需要集成哪些设备功能（相机、GPS、推送等）？"
            ])
        
        if 'ecommerce' in requirement_lower or '电商' in requirement_lower or '购物' in requirement_lower:
            questions.extend([
                "支持哪些支付方式？",
                "配送范围是什么？",
                "是否需要多商家入驻功能？",
                "需要支持哪些促销活动类型？"
            ])
        
        if 'management' in requirement_lower or '管理' in requirement_lower:
            questions.extend([
                "系统将有多少用户同时使用？",
                "需要哪些用户角色和权限？",
                "是否需要移动端管理功能？",
                "数据导入导出需求是什么？"
            ])
        
        # 通用问题
        if not questions:
            questions = [
                "这个系统的主要目标是什么？",
                "谁是主要用户？",
                "有什么特殊的安全或合规要求？",
                "预期的用户数量和数据量级？",
                "有哪些现有系统需要集成？"
            ]
        
        return questions[:6]  # 限制返回6个问题
    
    def get_requirement_template(self, category: str) -> Optional[RequirementTemplate]:
        """获取需求模板"""
        templates = {
            "web_app": RequirementTemplate(
                category="Web应用",
                subcategory="标准Web应用",
                template="""
# {项目名称} 需求文档

## 1. 项目概述
- **项目目标**: 
- **目标用户**: 
- **核心价值**: 

## 2. 功能需求
### 2.1 用户管理
- 用户注册和登录
- 用户角色管理
- 个人资料管理

### 2.2 核心功能
- [具体功能列表]

### 2.3 管理功能
- 后台管理界面
- 数据管理
- 系统配置

## 3. 非功能需求
- **性能**: 页面加载时间 < 3秒
- **安全**: HTTPS、数据加密
- **兼容性**: 支持主流浏览器
- **可用性**: 99.9%正常运行时间

## 4. 技术要求
- **前端技术**: 
- **后端技术**: 
- **数据库**: 
- **部署环境**: 
                """,
                questions=[
                    "网站的主要功能是什么？",
                    "预期有多少用户使用？",
                    "需要支持哪些浏览器？",
                    "是否需要移动端适配？",
                    "有什么特殊的安全要求？"
                ],
                examples=[
                    "企业官网",
                    "在线商城",
                    "内容管理系统",
                    "社交平台"
                ],
                best_practices=[
                    "响应式设计",
                    "SEO优化",
                    "安全性设计",
                    "用户体验优化"
                ]
            )
        }
        
        return templates.get(category)

# 创建全局知识库服务实例
knowledge_base_service = KnowledgeBaseService() 