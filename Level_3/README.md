# Level 3: Multi-Step Reasoning Agent

An advanced full agent that demonstrates multi-step reasoning capabilities, coordinating multiple tools while maintaining short-term memory to complete complex, multi-step queries.

## 🎯 Learning Objectives

By completing Level 3, you will learn:
- Multi-step task decomposition and sequencing
- Short-term memory management for context preservation
- Tool coordination and orchestration
- Complex query parsing and execution
- Advanced error handling and recovery strategies

## 🚀 Features

- **Multi-Step Reasoning**: Breaks down complex queries into manageable steps
- **Multiple Tool Integration**: Calculator and translator tools working together
- **Short-Term Memory**: Maintains context across steps within a single query
- **Task Decomposition**: Automatically identifies and sequences sub-tasks
- **Comprehensive Error Handling**: Graceful failure with detailed feedback
- **Execution Reporting**: Step-by-step results with comprehensive summaries

## 📋 Prerequisites

- Python 3.7+
- Google Gemini API key
- `requests` library
- Completion of Level 1 & 2 (recommended)

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

### 3. Run the Full Agent
```bash
python full_agent.py
```

### 4. Test Tools Independently
```bash
# Test calculator tool
python calculator_tool.py

# Test translator tool
python translator_tool.py
```

## 🔧 How It Works

1. **Query Decomposition**: Breaks complex queries into sequential steps
2. **Multi-Tool Coordination**: Coordinates calculator, translator, and LLM tools
3. **Short-Term Memory**: Maintains context and results across steps
4. **Sequential Execution**: Executes steps in order with dependency handling
5. **Comprehensive Reporting**: Provides detailed step-by-step results with summary

## 🛠️ Available Tools

### 🧮 Calculator Tool
- **Operations**: Addition, multiplication
- **Examples**: `15 + 23`, `multiply 5 by 6`, `add 10 and 20`
- **Decimal Support**: `2.5 + 3.7 = 6.2`

### 🌐 Translator Tool
- **Language Pair**: English → German
- **Vocabulary**: 80+ common words and phrases
- **Examples**: `"Hello" → "Hallo"`, `"Good Morning" → "Guten Morgen"`

### 🧠 LLM Integration
- **Provider**: Google Gemini
- **Capabilities**: General knowledge, explanations, structured responses
- **Format**: Step-by-step, numbered responses

## 📝 Example Interactions

### ✅ Multi-Step: Translation + Math
```
You: Translate 'Good Morning' into German and then multiply 5 and 6.

🤖 Full Agent: 🔍 Multi-step task detected! Breaking down your request:

**Step 1**: Translate 'Good Morning' into German
✅ Result: "Good Morning" → "Guten Morgen"

**Step 2**: multiply 5 and 6
✅ Result: 5 * 6 = 30

📋 **Task Summary**:
• Translation: Translate 'Good Morning' into German → Guten Morgen
• Math calculation: multiply 5 and 6 → 30
```

### ✅ Multi-Step: Math + Translation
```
You: Add 10 and 20, then translate 'Have a nice day' into German.

🤖 Full Agent: 🔍 Multi-step task detected! Breaking down your request:

**Step 1**: Add 10 and 20
✅ Result: 10 + 20 = 30

**Step 2**: translate 'Have a nice day' into German
✅ Result: "Have a nice day" → "Hab Einen Schönen Tag"

📋 **Task Summary**:
• Math calculation: Add 10 and 20 → 30
• Translation: translate 'Have a nice day' into German → Hab Einen Schönen Tag
```

### ✅ Multi-Step: LLM + Math
```
You: Tell me the capital of Italy, then multiply 12 and 12.

🤖 Full Agent: 🔍 Multi-step task detected! Breaking down your request:

**Step 1**: Tell me the capital of Italy
✅ Result: The capital of Italy is Rome (Roma in Italian). It's a historic city that has been the center of the Roman Empire and is now the political, cultural, and economic heart of modern Italy.

**Step 2**: multiply 12 and 12
✅ Result: 12 * 12 = 144

📋 **Task Summary**:
• General query: Tell me the capital of Italy → Rome (Roma in Italian)...
• Math calculation: multiply 12 and 12 → 144
```

### ✅ Single-Step Operations
```
You: Translate 'Sunshine' into German.

🤖 Full Agent: "Sunshine" → "Sonnenschein"
```

```
You: What is the distance between Earth and Mars?

🤖 Full Agent: The distance between Earth and Mars varies significantly due to their elliptical orbits around the Sun:

Step 1: Understanding orbital mechanics
- Both planets follow elliptical paths around the Sun
- The distance changes constantly as they orbit at different speeds

[Detailed explanation continues...]

Summary: The distance ranges from 35 million to 250 million miles, depending on orbital positions.
```

## 💡 Key Components

### FullAgent Class
- **`__init__()`**: Initializes API key, tools, and memory system
- **`parse_multi_step_query()`**: Decomposes queries into sequential steps
- **`execute_math_step()`**: Handles math operations via calculator tool
- **`execute_translation_step()`**: Handles translations via translator tool
- **`execute_llm_step()`**: Handles general queries via LLM
- **`process_multi_step_query()`**: Orchestrates multi-step execution
- **`add_to_memory()`**: Manages short-term memory for task context

### Memory System
```python
self.memory = {
    'previous_results': [],      # Completed step outcomes
    'current_task_steps': [],    # Planned steps for current task
    'completed_steps': []        # List of completed step descriptions
}
```

### Step Decomposition Logic
The agent identifies task boundaries using:
- Connecting words: `and then`, `then`, `and also`, `also`
- Task type analysis: math, translation, general queries
- Sequential parsing with comma separation

## 🌐 Translator Tool Details

### Supported Vocabulary (80+ words)
- **Greetings**: Hello → Hallo, Good Morning → Guten Morgen
- **Common Phrases**: Thank you → Danke, Please → Bitte
- **Everyday Words**: Water → Wasser, House → Haus, Friend → Freund
- **Colors**: Red → Rot, Blue → Blau, Green → Grün

### Translation Formats
- Direct: `Translate "Hello"`
- Question: `How do you say "Hello" in German?`
- Contextual: `What is "Hello" in German?`

## 🔍 Advanced Features

### Error Recovery
If a step fails, the agent:
1. Reports the specific error
2. Stops execution to prevent cascading failures
3. Provides helpful error messages
4. Suggests alternatives when possible

### Memory Management
- **Context Preservation**: Results from previous steps are available to subsequent steps
- **Task Isolation**: Memory is cleared between different user queries
- **Summary Generation**: Comprehensive task summaries with all results

## 🛠️ Testing Individual Tools

### Interactive Calculator
```bash
python calculator_tool.py
```

### Interactive Translator
```bash
python translator_tool.py
```

Both tools provide interactive modes for testing and exploration.

## 🔧 Architecture

### File Structure
- `full_agent.py` - Advanced reasoning agent
- `calculator_tool.py` - Calculator with interactive mode
- `translator_tool.py` - Translator with interactive mode
- `logs_level3.json` - Example interactions in JSON format

### Design Patterns
- **Agent Architecture**: Central coordinator managing multiple tools
- **Memory Management**: Short-term context preservation
- **Pipeline Processing**: Sequential step execution with error handling
- **Tool Abstraction**: Unified interface for different tool types

## 🛠️ Troubleshooting

### Common Issues

**Tool import errors**
- Ensure both `calculator_tool.py` and `translator_tool.py` are present
- Check Python path includes current directory

**Memory not persisting between steps**
- Verify `add_to_memory()` is called after successful step execution
- Check memory clearing only happens between different queries

**Step decomposition too aggressive/conservative**
- Review parsing logic in `parse_multi_step_query()`
- Adjust connector word patterns as needed

**Translation failures**
- Check if word exists in translation dictionary
- Consider adding new words to the vocabulary

## 📊 JSON Logs Structure

Level 3 uses JSON format for interaction logs:
```json
{
  "interaction_id": 1,
  "description": "Multi-step: Translation + Math",
  "user": "Translate 'Good Morning' into German and then multiply 5 and 6.",
  "assistant": "🔍 Multi-step task detected! Breaking down your request:\n\n..."
}
```

## 🎓 What's Next?

Level 3 represents advanced agent capabilities. Future extensions could include:
- **Level 4**: Persistent memory and learning
- **Level 5**: Multi-modal capabilities (images, files)
- **Level 6**: Advanced planning and execution
- **Level 7**: Multi-agent collaboration

## 📊 Files in This Level

- `full_agent.py` - Advanced reasoning agent implementation
- `calculator_tool.py` - Calculator tool with interactive mode
- `translator_tool.py` - Translation tool with interactive mode
- `logs_level3.json` - Example interactions in JSON format
- `README.md` - This file

---

**Congratulations on completing Level 3!** 🎉 
You've mastered multi-step reasoning, tool coordination, and advanced agent development patterns. You're now ready to build sophisticated AI agents!
