# Level 2: Tool-Integrated Chatbot

An enhanced chatbot that builds upon Level 1 by adding calculator tool integration and smart task routing, while maintaining graceful handling of complex multi-task requests.

## 🎯 Learning Objectives

By completing Level 2, you will learn:
- Tool abstraction and integration patterns
- Smart task routing and delegation
- Multiple task detection and graceful failure
- Modular architecture design
- Error propagation across systems

## 🚀 Features

- **Tool Integration**: Calculator tool for basic math operations
- **Smart Task Routing**: Automatically detects math vs general questions
- **Multiple Task Detection**: Gracefully handles complex multi-task requests
- **Enhanced Error Handling**: Specific error messages for different scenarios
- **Structured Responses**: Maintains step-by-step format for general questions

## 📋 Prerequisites

- Python 3.7+
- Google Gemini API key
- `requests` library
- Completion of Level 1 (recommended)

## ⚡ Quick Start

### 1. Set Up API Key
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your_api_key_here"

# Windows Command Prompt
set GEMINI_API_KEY=your_api_key_here

# Linux/Mac
export GEMINI_API_KEY="your_api_key_here"
```

### 2. Install Dependencies
```bash
pip install requests
```

### 3. Run the Enhanced Chatbot
```bash
python chatbot_with_tool.py
```

### 4. Test Calculator Tool Independently
```bash
python calculator_tool.py
```

## 🔧 How It Works

1. **Input Analysis**: Checks for multiple tasks and math operations
2. **Task Routing**: Routes math queries to calculator tool, others to LLM
3. **Tool Integration**: Uses calculator tool for supported math operations
4. **Multiple Task Detection**: Identifies and refuses complex multi-task requests
5. **Unified Response**: Provides consistent interface regardless of processing method

## 🧮 Calculator Tool Capabilities

### Supported Operations
- **Addition**: `15 + 23`, `add 10 and 5`, `what is 12 + 8`
- **Multiplication**: `5 * 6`, `multiply 4 by 7`, `5 times 6`
- **Decimal Support**: `2.5 + 3.7`, `1.5 * 4.2`

### Supported Input Formats
- Symbolic: `15 + 23`, `5 * 6`
- Natural language: `add 10 and 5`, `multiply 4 by 7`
- Conversational: `what is 15 + 23`, `tell me 5 times 6`

## 📝 Example Interactions

### ✅ Math Operations (Calculator Tool)
```
You: What is 15 + 23?

🤖 Chatbot: 🧮 Calculator Result: 15 + 23 = 38
```

```
You: Multiply 9 by 8

🤖 Chatbot: 🧮 Calculator Result: 9 * 8 = 72
```

### ✅ General Questions (LLM)
```
You: How do I improve my public speaking skills?

🤖 Chatbot: Here's a step-by-step guide to improving your public speaking skills:

Step 1: Start with preparation and practice
- Know your material inside and out
- Practice your speech multiple times in front of a mirror
- Record yourself to identify areas for improvement

[Response continues with structured steps...]

Summary: Improving public speaking requires consistent practice, preparation, and gradual exposure to speaking opportunities.
```

### ❌ Multiple Tasks (Graceful Failure)
```
You: Multiply 9 and 8, and also tell me the capital of Japan

🤖 Chatbot: I cannot yet handle multiple tasks at once. Please ask me one thing at a time.

For example:
✅ Good: "What is 15 + 23?"
✅ Good: "What is the capital of Japan?"
❌ Too complex: "Multiply 9 and 8, and also tell me the capital of Japan"

Please separate your questions and I'll be happy to help with each one individually!
```

### ❌ Unsupported Math Operations
```
You: What is 50 divided by 5?

🤖 Chatbot: 🧮 Calculator Error: Could not parse mathematical expression. I only support basic addition and multiplication.

Supported examples:
• 15 + 23
• add 10 and 5
• 5 * 6
• multiply 4 by 7
• what is 12 + 8
```

## 💡 Key Components

### Level2Chatbot Class
- **`__init__()`**: Initializes API key and calculator tool
- **`detect_multiple_tasks()`**: Identifies multi-task requests using regex patterns
- **`process_user_input()`**: Routes requests to appropriate handler
- **`query_llm()`**: Handles Gemini API communication
- **`chat_loop()`**: Enhanced interaction loop

### CalculatorTool Class
- **`parse_math_expression()`**: Extracts numbers and operations from text
- **`calculate()`**: Performs mathematical calculations
- **`process_math_query()`**: Complete math query processing pipeline
- **`is_supported_math_query()`**: Checks if math operation is supported

## 🔍 Task Detection Logic

### Math Detection
The system recognizes various mathematical expressions:
- Direct operations: `15 + 23`, `5 * 6`
- Natural language: `add 10 and 5`, `multiply 4 by 7`
- Question format: `what is 15 + 23`

### Multiple Task Detection
The system identifies complex requests with multiple components:
- Connecting words: `and then`, `also`, `and also`
- Mixed task types: math + general questions
- Sequential requests with commas

## 🛠️ Testing

### Interactive Calculator Testing
```bash
python calculator_tool.py
```

This opens an interactive mode where you can test math operations directly:
```
🧮 Calculator Tool - Interactive Mode
========================================
Math Query: 15 + 23
✅ Result: 15 + 23 = 38

Math Query: multiply 5 by 6
✅ Result: 5 * 6 = 30
```

## 🔧 Architecture

### File Structure
- `chatbot_with_tool.py` - Enhanced chatbot with tool integration
- `calculator_tool.py` - Basic calculator tool with interactive mode
- `logs_level2.txt` - Example interaction logs

### Design Patterns
- **Tool Abstraction**: Clean separation between chatbot and tools
- **Task Routing**: Intelligent delegation based on query analysis
- **Error Handling**: Graceful degradation and informative error messages

## 🛠️ Troubleshooting

### Common Issues

**Import errors with calculator_tool**
- Ensure `calculator_tool.py` is in the same directory
- Check Python path includes current directory

**Calculator not recognizing math operations**
- Verify input format matches supported patterns
- Check example logs for proper syntax

**Multiple task detection too aggressive**
- Review the detection patterns in `detect_multiple_tasks()`
- Consider adjusting regex patterns for edge cases

## 🎓 What's Next?

After mastering Level 2, proceed to:
- **Level 3**: Multi-step reasoning, translator tool, and advanced agent capabilities

## 📊 Files in This Level

- `chatbot_with_tool.py` - Enhanced chatbot implementation
- `calculator_tool.py` - Calculator tool with interactive mode
- `logs_level2.txt` - Example interaction logs
- `README.md` - This file

---

**Congratulations on completing Level 2!** 🎉 
You've learned tool integration and smart task routing. Ready for Level 3's advanced reasoning capabilities?
