import os
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import asyncio
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import re

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
class UploadedDocument:
    """Uploaded document data structure"""
    filename: str
    content_hash: str
    upload_time: str
    file_size: int
    file_type: str
    content_preview: str  # Preview of first 100 characters
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class RequirementTemplate:
    """Requirement template data structure"""
    category: str
    subcategory: str
    template: str
    questions: List[str]
    examples: List[str]
    best_practices: List[str]

class KnowledgeBaseService:
    """LightRAG-based knowledge base service"""
    
    def __init__(self):
        self.working_dir = Path("./rag_storage")
        self.working_dir.mkdir(exist_ok=True)
        
        # Document storage related paths
        self.documents_dir = self.working_dir / "documents"
        self.documents_dir.mkdir(exist_ok=True)
        self.documents_metadata_file = self.working_dir / "documents_metadata.json"
        
        self.rag = None
        self.templates_data = {}
        self.is_initialized = False
        self.uploaded_documents: List[UploadedDocument] = []
        
        # Load historical documents
        self._load_documents_metadata()
        
        if LIGHTRAG_AVAILABLE:
            self._initialize_rag()
            self._load_knowledge_base()
    
    def _load_documents_metadata(self):
        """Load metadata of uploaded documents"""
        try:
            if self.documents_metadata_file.exists():
                with open(self.documents_metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.uploaded_documents = [
                        UploadedDocument.from_dict(doc_data) 
                        for doc_data in data.get('documents', [])
                    ]
                logging.info(f"Loaded {len(self.uploaded_documents)} documents from history")
            else:
                self.uploaded_documents = []
        except Exception as e:
            logging.error(f"Failed to load documents metadata: {e}")
            self.uploaded_documents = []
    
    def _save_documents_metadata(self):
        """Save document metadata to file"""
        try:
            metadata = {
                'documents': [doc.to_dict() for doc in self.uploaded_documents],
                'last_updated': datetime.now().isoformat()
            }
            with open(self.documents_metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            logging.info(f"Saved metadata for {len(self.uploaded_documents)} documents")
        except Exception as e:
            logging.error(f"Failed to save documents metadata: {e}")
    
    def _calculate_content_hash(self, content: str) -> str:
        """Calculate content hash for deduplication"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    async def add_document(self, filename: str, content: str) -> Dict[str, Any]:
        """Add document to knowledge base"""
        try:
            # Calculate content hash
            content_hash = self._calculate_content_hash(content)
            
            # Check if document with same content already exists
            existing_doc = next(
                (doc for doc in self.uploaded_documents if doc.content_hash == content_hash),
                None
            )
            
            if existing_doc:
                return {
                    "success": False,
                    "error": f"Document with similar content already exists: {existing_doc.filename}",
                    "duplicate": True
                }
            
            # Ensure document directory exists
            self.documents_dir.mkdir(parents=True, exist_ok=True)
            
            # Clean filename to avoid special character issues
            safe_filename = self._sanitize_filename(filename)
            doc_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_filename}"
            doc_path = self.documents_dir / doc_filename
            
            # Save document content to file
            try:
                with open(doc_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logging.info(f"Document saved to: {doc_path}")
            except Exception as e:
                logging.error(f"Failed to save document file: {e}")
                raise
            
            # Create document metadata
            document = UploadedDocument(
                filename=filename,  # Keep original filename
                content_hash=content_hash,
                upload_time=datetime.now().isoformat(),
                file_size=len(content.encode('utf-8')),
                file_type=filename.split('.')[-1].lower() if '.' in filename else 'unknown',
                content_preview=content[:100] + "..." if len(content) > 100 else content
            )
            
            # Add to LightRAG (if available)
            if self.is_initialized and self.rag:
                try:
                    formatted_content = f"""
Document Name: {filename}
Upload Time: {document.upload_time}
File Type: {document.file_type}

Content:
{content}
                    """
                    await self.rag.ainsert(formatted_content)
                    logging.info(f"Document added to LightRAG: {filename}")
                except Exception as e:
                    logging.warning(f"Failed to add document to LightRAG: {e}")
            
            # Save metadata
            self.uploaded_documents.append(document)
            self._save_documents_metadata()
            
            return {
                "success": True,
                "message": f"Document '{filename}' added successfully",
                "document": document.to_dict()
            }
            
        except Exception as e:
            logging.error(f"Failed to add document '{filename}': {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _sanitize_filename(self, filename: str) -> str:
        """Clean filename, remove or replace characters that might cause issues"""
        # Remove or replace unsafe characters
        unsafe_chars = r'[<>:"/\\|?*]'
        safe_filename = re.sub(unsafe_chars, '_', filename)
        
        # Limit length
        if len(safe_filename) > 100:
            name, ext = safe_filename.rsplit('.', 1) if '.' in safe_filename else (safe_filename, '')
            safe_filename = name[:95] + ('.' + ext if ext else '')
        
        return safe_filename
    
    def get_uploaded_documents(self) -> List[Dict[str, Any]]:
        """Get list of uploaded documents"""
        return [doc.to_dict() for doc in self.uploaded_documents]
    
    def get_documents_summary(self) -> Dict[str, Any]:
        """Get document summary information"""
        total_docs = len(self.uploaded_documents)
        total_size = sum(doc.file_size for doc in self.uploaded_documents)
        
        file_types = {}
        for doc in self.uploaded_documents:
            file_types[doc.file_type] = file_types.get(doc.file_type, 0) + 1
        
        return {
            "total_documents": total_docs,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "file_types": file_types,
            "latest_upload": self.uploaded_documents[-1].upload_time if self.uploaded_documents else None
        }
    
    async def remove_document(self, filename: str) -> Dict[str, Any]:
        """Remove document from knowledge base"""
        try:
            # Find document
            document = next(
                (doc for doc in self.uploaded_documents if doc.filename == filename),
                None
            )
            
            if not document:
                return {
                    "success": False,
                    "error": f"Document '{filename}' not found"
                }
            
            # Remove from list
            self.uploaded_documents.remove(document)
            
            # Delete document file (if exists)
            for doc_file in self.documents_dir.glob(f"*_{filename}"):
                try:
                    doc_file.unlink()
                except Exception as e:
                    logging.warning(f"Failed to delete document file {doc_file}: {e}")
            
            # Save updated metadata
            self._save_documents_metadata()
            
            # Note: LightRAG doesn't support deleting specific documents, need to rebuild knowledge base
            # Here we only remove from metadata, actual vector data remains in LightRAG
            
            return {
                "success": True,
                "message": f"Document '{filename}' removed successfully"
            }
            
        except Exception as e:
            logging.error(f"Failed to remove document '{filename}': {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def rebuild_knowledge_base(self):
        """Rebuild knowledge base (reload all documents)"""
        if not self.is_initialized or not self.rag:
            return
        
        try:
            # Reinitialize RAG system
            self._initialize_rag()
            
            # Reload predefined knowledge base
            self._load_knowledge_base()
            
            # Reload all user documents
            for document in self.uploaded_documents:
                # Try to read content from file
                for doc_file in self.documents_dir.glob(f"*_{document.filename}"):
                    try:
                        with open(doc_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        formatted_content = f"""
Document Name: {document.filename}
Upload Time: {document.upload_time}
File Type: {document.file_type}

Content:
{content}
                        """
                        await self.rag.ainsert(formatted_content)
                        break
                    except Exception as e:
                        logging.warning(f"Failed to reload document {document.filename}: {e}")
            
            logging.info("Knowledge base rebuilt successfully")
            
        except Exception as e:
            logging.error(f"Failed to rebuild knowledge base: {e}")
    
    def _initialize_rag(self):
        """Initialize LightRAG system"""
        try:
            # Simplified LLM model function
            async def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs) -> str:
                # Use our existing LLM service here
                from services.llm_service import llm_service
                full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
                return await llm_service.generate_completion(full_prompt, "demo")
            
            # Simplified embedding function
            async def embedding_func(texts: list[str]):
                # Return simulated embedding vectors
                import numpy as np
                return np.random.rand(len(texts), 768).astype(np.float32)
            
            # Initialize LightRAG
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
        """Load requirements analysis knowledge base"""
        if not self.is_initialized:
            return
            
        # Predefined requirements analysis knowledge base data
        knowledge_data = self._get_requirements_knowledge()
        
        try:
            # Insert knowledge base data into LightRAG
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
        """Get requirements analysis knowledge base data"""
        return {
            "web_applications": """
            Web Application Requirements Analysis Guide:
            
            Functional Requirements:
            - User registration and login system
            - User roles and permission management
            - Data CRUD operations
            - Search and filtering functionality
            - File upload and download
            - Notification system
            - Reporting and data visualization
            
            Non-functional Requirements:
            - Response time: Page load time <3 seconds
            - Concurrent users: Support 1000+ simultaneous online users
            - Security: HTTPS, SQL injection protection, XSS protection
            - Compatibility: Support mainstream browsers
            - Availability: 99.9% uptime
            
            Technical Architecture:
            - Frontend: React/Vue/Angular
            - Backend: Node.js/Python/Java
            - Database: MySQL/PostgreSQL/MongoDB
            - Deployment: Docker, cloud services
            
            Questions to clarify:
            1. Expected number of users and concurrent load?
            2. Which devices and browsers need support?
            3. Data security and privacy requirements?
            4. Need for third-party integrations?
            5. Maintenance and update frequency?
            """,
            
            "mobile_applications": """
            Mobile Application Requirements Analysis Guide:
            
            Functional Requirements:
            - User interface design and user experience
            - Offline functionality support
            - Push notifications
            - Camera and media functionality
            - GPS location services
            - Social sharing functionality
            - Payment integration
            
            Non-functional Requirements:
            - Startup time: <3 seconds
            - Battery optimization
            - Memory usage optimization
            - Network adaptability (2G/3G/4G/5G/WiFi)
            - Application size control
            
            Platform Considerations:
            - iOS vs Android vs Cross-platform
            - Minimum supported version
            - Device adaptation (phones, tablets)
            - App store release requirements
            
            Questions to clarify:
            1. Target platform (iOS/Android/Cross-platform)?
            2. Need for offline functionality?
            3. Which device permissions required?
            4. Push notification strategy?
            5. App store release plan?
            """,
            
            "e_commerce": """
            E-commerce System Requirements Analysis Guide:
            
            Core Functionality:
            - Product management (categories, inventory, pricing)
            - Shopping cart and order process
            - Payment system integration
            - User account management
            - Review and rating system
            - Promotions and coupons
            - Logistics tracking
            
            Management Features:
            - Merchant management backend
            - Order management
            - Financial reports
            - Customer service tools
            - Data analysis dashboard
            
            Security Requirements:
            - PCI DSS compliance
            - User data protection
            - Anti-fraud mechanisms
            - Secure payment processing
            
            Questions to clarify:
            1. B2C, B2B or B2B2C model?
            2. Supported payment methods?
            3. Delivery scope and logistics partnerships?
            4. Multi-language and multi-currency support?
            5. Mobile requirements?
            """,
            
            "data_management": """
            Data Management System Requirements Analysis Guide:
            
            Data Functions:
            - Data collection and import
            - Data cleaning and validation
            - Data storage and backup
            - Data querying and retrieval
            - Data visualization
            - Data export and reporting
            
            Data Quality:
            - Data accuracy validation
            - Duplicate data handling
            - Data integrity checks
            - Data update mechanisms
            
            Security and Compliance:
            - Data encryption
            - Access control
            - Audit logs
            - GDPR/privacy law compliance
            
            Questions to clarify:
            1. Data sources and formats?
            2. Data volume scale and growth expectations?
            3. Real-time requirements?
            4. Data retention policies?
            5. Integration with other systems requirements?
            """
        }
    
    async def query_knowledge_base(self, requirement_text: str, query_mode: str = "hybrid") -> Dict[str, Any]:
        """Query knowledge base for relevant suggestions"""
        if not self.is_initialized or not self.rag:
            return {
                "success": False,
                "error": "Knowledge base not initialized",
                "suggestions": [],
                "questions": []
            }
        
        try:
            # Build query
            query = f"Analyze the following requirements and provide improvement suggestions: {requirement_text}"
            
            # Query knowledge base
            response = await self.rag.aquery(
                query, 
                param=QueryParam(mode=query_mode)
            )
            
            # Parse response and generate suggestions
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
        """Parse knowledge base response to generate suggestions"""
        suggestions = []
        
        # Simple response parsing logic
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line and ('suggest' in line.lower() or 'recommend' in line.lower() or 'should' in line.lower()):
                suggestions.append(line)
        
        # If no suggestions found, return generic suggestions
        if not suggestions:
            suggestions = [
                "Suggest clarifying target user groups and use cases",
                "Need detailed description of core functions and user flows",
                "Consider non-functional requirements like performance, security, scalability",
                "Clarify technology stack and deployment environment requirements"
            ]
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def _generate_clarification_questions(self, requirement_text: str, context: str) -> List[str]:
        """Generate clarification questions based on requirements and context"""
        questions = []
        
        # Generate questions based on requirement type
        requirement_lower = requirement_text.lower()
        
        if 'web' in requirement_lower or 'website' in requirement_lower:
            questions.extend([
                "Who is the main user group for this web application?",
                "What is the expected number of concurrent users?",
                "Which browsers and devices need support?",
                "Do you need mobile adaptation?"
            ])
        
        if 'mobile' in requirement_lower or 'app' in requirement_lower:
            questions.extend([
                "Do you need iOS, Android, or cross-platform development?",
                "Does the app need offline functionality?",
                "Which device features need integration (camera, GPS, push, etc.)?",
            ])
        
        if 'ecommerce' in requirement_lower or 'e-commerce' in requirement_lower or 'shopping' in requirement_lower:
            questions.extend([
                "Which payment methods to support?",
                "What is the delivery scope?",
                "Do you need multi-vendor functionality?",
                "Which types of promotional activities to support?"
            ])
        
        if 'management' in requirement_lower or 'manage' in requirement_lower:
            questions.extend([
                "How many users will use the system simultaneously?",
                "Which user roles and permissions are needed?",
                "Do you need mobile management functionality?",
                "What are the data import/export requirements?"
            ])
        
        # Generic questions
        if not questions:
            questions = [
                "What is the main goal of this system?",
                "Who are the primary users?",
                "Are there any special security or compliance requirements?",
                "What are the expected user numbers and data scale?",
                "Which existing systems need integration?"
            ]
        
        return questions[:6]  # Limit to 6 questions
    
    def get_requirement_template(self, category: str) -> Optional[RequirementTemplate]:
        """Get requirement template"""
        templates = {
            "web_app": RequirementTemplate(
                category="Web Application",
                subcategory="Standard Web Application",
                template="""
# {Project Name} Requirements Document

## 1. Project Overview
- **Project Goal**: 
- **Target Users**: 
- **Core Value**: 

## 2. Functional Requirements
### 2.1 User Management
- User registration and login
- User role management
- Profile management

### 2.2 Core Features
- [Specific feature list]

### 2.3 Management Features
- Backend management interface
- Data management
- System configuration

## 3. Non-Functional Requirements
- **Performance**: Page load time < 3 seconds
- **Security**: HTTPS, data encryption
- **Compatibility**: Support mainstream browsers
- **Availability**: 99.9% uptime

## 4. Technical Requirements
- **Frontend Technology**: 
- **Backend Technology**: 
- **Database**: 
- **Deployment Environment**: 
                """,
                questions=[
                    "What are the main functions of the website?",
                    "How many users are expected?",
                    "Which browsers need support?",
                    "Do you need mobile adaptation?",
                    "Are there any special security requirements?"
                ],
                examples=[
                    "Corporate website",
                    "Online store",
                    "Content management system",
                    "Social platform"
                ],
                best_practices=[
                    "Responsive design",
                    "SEO optimization",
                    "Security design",
                    "User experience optimization"
                ]
            )
        }
        
        return templates.get(category)

# Create global knowledge base service instance
knowledge_base_service = KnowledgeBaseService() 