# Level 1: Basic CLI Chatbot

A simple command-line chatbot that integrates with Google's Gemini API to provide structured, step-by-step responses while gracefully refusing mathematical calculations.

## 🎯 Learning Objectives

By completing Level 1, you will learn:
- How to integrate with modern LLM APIs (Gemini)
- Prompt engineering for structured outputs
- Input validation and filtering techniques
- Graceful error handling and user feedback
- CLI interface design patterns

## 🚀 Features

- **CLI Interface**: Simple command-line interaction
- **Gemini API Integration**: Uses Google's Gemini Pro model
- **Structured Responses**: All answers formatted in step-by-step format
- **Math Calculation Refusal**: Automatically detects and refuses math questions
- **Error Handling**: Robust error handling for API failures

## 📋 Prerequisites

- Python 3.7+
- Google Gemini API key
- `requests` library

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

### 3. Run the Chatbot
```bash
python chatbot.py
```

## 🔧 How It Works

1. **Input Processing**: Takes user input through CLI
2. **Math Detection**: Uses regex patterns to detect mathematical calculations
3. **API Integration**: Sends non-math queries to Gemini API
4. **Response Formatting**: Returns structured, step-by-step answers
5. **Error Handling**: Gracefully handles API errors and network issues

## 📝 Example Interactions

### ✅ Supported Queries
```
You: How do I bake a cake?

🤖 Chatbot: Here's a step-by-step guide to baking a cake:

Step 1: Gather your ingredients
- 2 cups all-purpose flour
- 1½ cups sugar
- ½ cup butter
- 3 eggs
- 1 cup milk
- 2 teaspoons baking powder

Step 2: Prepare your workspace
- Preheat oven to 350°F (175°C)
- Grease and flour a 9-inch cake pan
- Set up mixing bowls and measuring tools

[Response continues with detailed steps...]

Summary: Baking a cake involves proper ingredient preparation, mixing technique, and careful temperature control for best results.
```

### ❌ Refused Operations
```
You: What is 15 + 23?

🤖 Chatbot: I cannot perform mathematical calculations. Please use a calculator tool or app for accurate results. I'm here to help with explanations, advice, and general information instead!

Some great calculator options:
• Built-in Windows Calculator
• Google Search (just type your calculation)
• Python calculator: python -c "print(15 + 23)"
• Online calculators like calculator.net

Is there something else I can help you with today?
```

## 💡 Key Components

### Level1Chatbot Class
- **`__init__()`**: Initializes API key and configuration
- **`is_math_question()`**: Detects mathematical calculations using regex patterns
- **`get_math_refusal_response()`**: Returns standard refusal message with alternatives
- **`query_llm()`**: Handles Gemini API communication with error handling
- **`chat_loop()`**: Main interaction loop with exit commands

### Math Detection Patterns
The chatbot recognizes various math formats:
- Basic arithmetic: `15 + 23`, `10 * 5`
- Natural language: `add 5 and 7`, `multiply 4 by 6`
- Question format: `what is 15 + 23`
- Percentages: `10% of 100`

## 🔍 Exit Commands
- `quit`
- `exit`
- `bye`
- `q`

## 🛠️ Troubleshooting

### Common Issues

**"Gemini API key not found"**
- Ensure GEMINI_API_KEY environment variable is set
- Check that the API key is valid and active

**Network errors**
- Check internet connection
- Verify API key has proper permissions

**Import errors**
- Install required packages: `pip install requests`

## 🎓 What's Next?

After mastering Level 1, proceed to:
- **Level 2**: Learn tool integration and smart task routing
- **Level 3**: Explore multi-step reasoning and advanced agent capabilities

## 📊 Files in This Level

- `chatbot.py` - Main chatbot implementation
- `logs_level1.txt` - Example interaction logs
- `README.md` - This file

---

**Congratulations on completing Level 1!** 🎉 
You've built a solid foundation for AI chatbot development. Ready for Level 2?
