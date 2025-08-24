# Progressive Chatbot Project

A comprehensive implementation of a progressive chatbot system that demonstrates increasing levels of complexity and capability, from basic CLI interaction to advanced multi-step reasoning with tool integration.

## 🚀 Project Overview

This project showcases the evolution of AI chatbot capabilities through three progressive levels:

- **Level 1**: Basic CLI chatbot with structured responses
- **Level 2**: Tool-integrated chatbot with smart task routing  
- **Level 3**: Advanced agent with multi-step reasoning and memory

Each level builds upon the previous one, introducing new concepts and capabilities that demonstrate modern AI agent development patterns.

## 📁 Repository Structure

```
.
├── Level1/                 # Basic CLI Chatbot
│   ├── chatbot.py          # Main chatbot implementation
│   ├── logs_level1.txt     # Example interactions
│   └── README.md           # Level 1 instructions
├── Level2/                 # Tool-Integrated Chatbot
│   ├── chatbot_with_tool.py # Enhanced chatbot with tools
│   ├── calculator_tool.py   # Basic calculator tool
│   ├── logs_level2.txt     # Example interactions
│   └── README.md           # Level 2 instructions
├── Level3/                 # Multi-Step Reasoning Agent
│   ├── full_agent.py       # Advanced reasoning agent
│   ├── calculator_tool.py  # Calculator tool
│   ├── translator_tool.py  # Translation tool
│   ├── logs_level3.json    # Example interactions (JSON)
│   └── README.md           # Level 3 instructions
└── README.md               # This file
```

## 🎯 Learning Progression

### Level 1: Foundation
**Concepts Introduced:**
- CLI interface design
- LLM API integration (Gemini)
- Structured response formatting
- Basic error handling
- Input validation and filtering

**Key Learning Points:**
- How to integrate with modern LLM APIs
- Prompt engineering for structured outputs
- Graceful refusal of unsupported operations

### Level 2: Tool Integration
**Concepts Introduced:**
- Tool abstraction and integration
- Smart task routing
- Multiple task detection
- Modular architecture design

**Key Learning Points:**
- When and how to delegate tasks to specialized tools
- Balancing automation with user control
- Error propagation and handling across systems

### Level 3: Advanced Reasoning
**Concepts Introduced:**
- Multi-step task decomposition
- Short-term memory management
- Tool coordination and orchestration
- Complex query parsing and execution

**Key Learning Points:**
- Breaking down complex problems into manageable steps
- Maintaining context across multi-step operations
- Coordinating multiple tools to solve complex tasks

## 🛠️ Prerequisites

- **Python 3.7+**
- **Google Gemini API Key** (get from [Google AI Studio](https://makersuite.google.com/app/apikey))
- **requests library**: `pip install requests`

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd progressive-chatbot-project
```

### 2. Set Up API Key
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your_api_key_here"

# Linux/Mac
export GEMINI_API_KEY="your_api_key_here"
```

### 3. Install Dependencies
```bash
pip install requests
```

### 4. Run Any Level
```bash
# Level 1: Basic Chatbot
cd Level1
python chatbot.py

# Level 2: Tool-Integrated Chatbot
cd Level2
python chatbot_with_tool.py

# Level 3: Advanced Reasoning Agent
cd Level3
python full_agent.py
```

## 🔧 Tools & Capabilities

### Calculator Tool
- **Operations**: Addition, multiplication
- **Input Formats**: Natural language and symbolic
- **Examples**: `"15 + 23"`, `"multiply 5 by 6"`, `"add 10 and 20"`

### Translator Tool
- **Language Pair**: English → German
- **Vocabulary**: 80+ common words and phrases
- **Examples**: `"Translate 'Hello'"`, `"Good Morning → Guten Morgen"`

### LLM Integration
- **Provider**: Google Gemini
- **Capabilities**: General knowledge, explanations, structured responses
- **Format**: Step-by-step, numbered responses

## 📝 Example Capabilities by Level

### Level 1 Examples
```
✅ "How do I bake a cake?" → Structured step-by-step guide
❌ "What is 15 + 23?" → Graceful refusal with alternatives
```

### Level 2 Examples
```
✅ "What is 15 + 23?" → Calculator: 15 + 23 = 38
✅ "How do I learn Python?" → LLM: Structured learning guide
❌ "Add 5 + 5 and tell me about Python" → Graceful multi-task refusal
```

### Level 3 Examples
```
✅ "Translate 'Hello' to German and multiply 5 by 6"
    → Step 1: "Hello" → "Hallo"
    → Step 2: 5 * 6 = 30
    → Summary provided

✅ "Tell me about AI, then add 10 + 20"
    → Step 1: Comprehensive AI explanation
    → Step 2: 10 + 20 = 30
    → Complete task summary
```

## 🎓 Educational Value

This project demonstrates:

1. **Progressive Complexity**: Each level introduces new concepts while building on previous ones
2. **Real-World Patterns**: Industry-standard approaches to AI agent development
3. **Best Practices**: Error handling, modular design, user experience considerations
4. **Modern Integration**: Current LLM APIs and tool integration patterns

## 🚀 Extension Ideas

- **Level 4**: Persistent memory and learning
- **Level 5**: Multi-modal capabilities (images, files)
- **Level 6**: Advanced planning and execution
- **Level 7**: Multi-agent collaboration

## 📄 License

This project is provided for educational purposes. Feel free to use, modify, and extend for learning and development.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new tools and capabilities
- Improve error handling and user experience
- Extend to additional levels
- Add support for other LLM providers

## 📞 Support

If you encounter issues:
1. Check the level-specific README files
2. Verify your Gemini API key is set correctly
3. Ensure all dependencies are installed
4. Review the example logs for expected behavior

---

**Start your journey with Level 1 and progress through each level to master progressive AI agent development!** 🎯
