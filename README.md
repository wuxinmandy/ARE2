# 🤖 AI Requirements Management System

An intelligent requirements management system powered by Generative AI that helps users enhance and review software requirements through AI-driven conversations.

## ✨ Key Features

### 🎯 Core Functionality

1. **Smart Requirements Input** - Users input simple requirement text through a beautiful, ChatGPT-like web interface
2. **AI Requirements Enhancement** - Requirement Agent enhances requirements through large model conversations with users
3. **Intelligent Requirements Review** - Review Agent conducts requirement reviews using knowledge base and LLM
4. **Problem Highlighting** - Issues found are **highlighted in yellow** on the web UI
5. **Multi-Model Support** - Configurable selection of different LLM models (OpenAI, Anthropic, etc.)

### 🎨 Interface Highlights

- **ChatGPT-style Web UI** built with Streamlit
- **Conversational Design** with chat bubbles and smooth flow
- **Responsive Layout** supporting desktop and mobile devices
- **Modern Styling** with gradients, animations, and clean aesthetics
- **Real-time Interactive Conversations** 
- **Intuitive Navigation** with phase indicators and status management

## 🛠 Technology Architecture

### Tech Stack
- **Frontend Interface**: Streamlit (designed for AI applications)
- **Backend Service**: Python
- **AI Integration**: OpenAI API, Anthropic API
- **Data Processing**: Python standard library + third-party packages

### AI Agent Architecture
- **Requirement Agent** - Requirements enhancement agent
- **Review Agent** - Requirements review agent  
- **LLM Service** - Unified large language model service interface

## 🚀 Quick Start

### Method 1: One-Click Launch (Recommended)

```bash
# Clone the project (if from GitHub)
git clone [your-repo-url]
cd ARE2

# One-click start (auto-checks dependencies and configuration)
python run.py
```

### Method 2: Manual Setup

#### 1. Environment Requirements
- Python 3.8 or higher
- pip package manager

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Environment Configuration
```bash
# Copy environment variables file (optional - demo mode works without API keys)
cp env.example .env

# Edit .env file (optional, system supports demo mode)
# OPENAI_API_KEY=your_openai_api_key_here  
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

#### 4. Start Application
```bash
streamlit run main.py
```

#### 5. Access Application
Open browser and visit: **http://localhost:8501**

## 💡 User Guide

### 🔄 Three-Phase Complete Workflow

#### Phase 1: Requirements Input
1. Enter simple requirement descriptions on the welcome screen
2. Use provided example requirements or create your own
3. Select AI model (demo mode supported)
4. Click "Start Analysis"

#### Phase 2: Requirements Enhancement  
1. AI automatically analyzes and enhances your requirements
2. Continue conversation to clarify and refine further
3. Request AI to modify specific parts
4. When satisfied, click "Start Review"

#### Phase 3: Requirements Review
1. Review Agent automatically reviews complete requirements
2. View quality score (1-10 rating)
3. **Problem Highlighting**: Issues highlighted with yellow background
4. Review detailed improvement suggestions

### 🎮 Demo Mode

The system supports **Demo Mode** for immediate experience without API key configuration:
- Simulates real AI responses
- Demonstrates complete functionality workflow
- Perfect for quick testing and demonstrations

## 📁 Project Structure

```
ARE2/
├── main.py                 # Main Streamlit application
├── run.py                  # One-click startup script
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (auto-generated)
├── env.example             # Environment variables example
├── services/               # Service layer
│   └── llm_service.py      # Unified LLM service
├── agents/                 # AI agents
│   ├── requirement_agent.py   # Requirements enhancement agent
│   └── review_agent.py         # Requirements review agent
└── README.md               # Project documentation
```

## 🔧 Configuration Guide

### LLM Model Configuration

Configure API keys in `.env` file:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# Anthropic Configuration  
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Default Model
DEFAULT_MODEL=demo  # Options: openai, anthropic, demo
```

### Supported Models

| Model | Description | Requires API Key |
|-------|-------------|------------------|
| OpenAI GPT-4 | Suitable for complex requirement analysis | ✅ |
| Anthropic Claude | Excellent at logical reasoning | ✅ |
| Demo Mode | Simulates AI responses, no key needed | ❌ |

## 🎯 Core Features Showcase

### 🌟 Problem Highlighting Feature
- Automatically identifies potential issues in requirements
- Uses **yellow background highlighting** for problem areas
- Hover tooltips show improvement suggestions
- Supports multiple issue types: errors, warnings, suggestions

### 💬 Intelligent Conversation
- Natural language interaction
- Context understanding
- Incremental requirement refinement
- Real-time status updates

### 📊 Smart Review
- Based on software engineering best practices
- Multi-dimensional quality assessment
- Structured problem reporting
- Quantified quality scoring

## 🚀 Deployment Guide

### Local Deployment
```bash
python run.py
```

### Docker Deployment
```bash
# Build image
docker build -t ai-requirement-system .

# Run container
docker run -p 8501:8501 ai-requirement-system
```

### Cloud Platform Deployment
- Streamlit Cloud
- Heroku
- AWS/Azure/GCP

## 🔍 Troubleshooting

### Common Issues

1. **Python Version Error**
   ```bash
   # Check Python version
   python --version
   # Requires Python 3.8+
   ```

2. **Dependency Installation Failed**
   ```bash
   # Upgrade pip
   python -m pip install --upgrade pip
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

3. **Port Already in Use**
   ```bash
   # Specify different port
   streamlit run main.py --server.port 8502
   ```

4. **API Key Issues**
   - Check `.env` file format
   - Verify API key validity
   - Use demo mode for testing

## 🎨 Custom Development

### Adding New LLM Models
1. Add new model implementation in `services/llm_service.py`
2. Update model list in `config.py`
3. Configure corresponding environment variables

### Extending AI Agent Features
1. Create new agent in `agents/` directory
2. Implement agent core logic and prompts
3. Integrate new agent in main application

### Customizing UI Styles
1. Modify CSS styles in `main.py`
2. Adjust Streamlit component layouts
3. Add new interactive elements

## 📈 System Advantages

- **Zero-Config Startup**: Demo mode support, ready to use immediately
- **Simple Technology**: Pure Python tech stack, easy to maintain
- **Beautiful Interface**: Modern design with excellent user experience
- **Complete Functionality**: Covers full requirements management workflow
- **Easy to Extend**: Modular architecture, convenient for customization
- **ChatGPT-like UX**: Familiar conversation-based interface

## 🤝 Contributing

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

MIT License

## 📞 Contact

For questions or suggestions, please submit an Issue or contact the developer.

---

**🎯 Make requirements management smarter and more efficient!**

**🚀 Experience the Gen AI-powered intelligent requirements management system now!**

## 🌟 Interface Preview

The new ChatGPT-like interface features:
- **Clean Welcome Screen** with example prompts
- **Chat Bubble Conversations** with smooth animations  
- **Phase Progress Indicators** showing Input → Enhance → Review
- **Modern Color Scheme** with gradients and shadows
- **Responsive Design** that works on all devices
- **Yellow Issue Highlighting** as requested for problem identification

**Access at: http://localhost:8501** 