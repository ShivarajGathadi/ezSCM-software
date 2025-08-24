"""
Level 3 Full Agent - Multi-Step Reasoning Chatbot
===============================================

An advanced chatbot with multi-step reasoning capabilities that can break down complex
queries, use multiple tools, and maintain short-term memory for task completion.
"""

import os
import re
import json
import requests
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
from calculator_tool import CalculatorTool
from translator_tool import TranslatorTool


class FullAgent:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Full Agent with Gemini API and tool integration.
        
        Args:
            api_key: Gemini API key. If None, will try to get from environment variable.
        """
        # Set up Gemini API key
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv('GEMINI_API_KEY')
            
        if not self.api_key:
            raise ValueError("Gemini API key not found. Please set GEMINI_API_KEY environment variable or pass it as parameter.")
        
        # Gemini API endpoint
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}"
        
        # Initialize tools
        self.calculator = CalculatorTool()
        self.translator = TranslatorTool()
        
        # Short-term memory for multi-step tasks
        self.memory = {
            'previous_results': [],
            'current_task_steps': [],
            'completed_steps': []
        }
        
        # System prompt for structured responses
        self.system_prompt = """You are a helpful assistant that provides structured, step-by-step answers. 

IMPORTANT RULES:
1. Always structure your responses with clear steps using numbered lists
2. Break down complex topics into digestible parts
3. Be conversational but informative
4. Keep responses concise but thorough
5. Do NOT perform mathematical calculations or translations - those are handled by external tools

Note: Mathematical calculations and translations are handled by specialized tools, not by you directly.
"""

    def clear_memory(self):
        """Clear the short-term memory."""
        self.memory = {
            'previous_results': [],
            'current_task_steps': [],
            'completed_steps': []
        }

    def add_to_memory(self, step_description: str, result: Any):
        """Add a completed step to memory."""
        self.memory['previous_results'].append({
            'step': step_description,
            'result': result
        })
        self.memory['completed_steps'].append(step_description)

    def parse_multi_step_query(self, user_input: str) -> List[Dict[str, Any]]:
        """
        Parse a user query to identify multiple steps/tasks.
        
        Args:
            user_input: The user's input string
            
        Returns:
            List of task dictionaries with type and content
        """
        steps = []
        user_input_lower = user_input.lower()
        
        # Split by common connectors
        connectors = [' and then ', ' then ', ' and also ', ' also ', ' and ']
        parts = [user_input]
        
        for connector in connectors:
            new_parts = []
            for part in parts:
                new_parts.extend(part.split(connector))
            parts = new_parts
        
        # Also split by commas with potential task indicators
        additional_parts = []
        for part in parts:
            if ',' in part:
                comma_parts = part.split(',')
                for i, comma_part in enumerate(comma_parts):
                    if i > 0:  # Skip first part, already included
                        comma_part = comma_part.strip()
                        # Check if it starts with task indicators
                        if any(comma_part.startswith(word) for word in ['translate', 'add', 'multiply', 'tell', 'what', 'how']):
                            additional_parts.append(comma_part)
                        elif len(comma_part) > 5:  # Avoid very short fragments
                            additional_parts.append(comma_part)
                additional_parts.append(comma_parts[0])  # Add the first part
            else:
                additional_parts.append(part)
        
        parts = additional_parts
        
        # Analyze each part
        for part in parts:
            part = part.strip()
            if not part or len(part) < 3:
                continue
                
            task = {
                'original_text': part,
                'type': 'unknown',
                'content': part
            }
            
            # Check for math operations
            if self.calculator.is_supported_math_query(part):
                task['type'] = 'math'
            # Check for translation requests
            elif self.translator.is_translation_query(part):
                task['type'] = 'translation'
            # Everything else goes to LLM
            else:
                task['type'] = 'llm'
            
            steps.append(task)
        
        return steps

    def execute_math_step(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a math calculation step."""
        result = self.calculator.process_math_query(task['content'])
        if result['success']:
            return {
                'success': True,
                'type': 'math',
                'description': f"Math calculation: {task['content']}",
                'result': result['formatted_calculation'],
                'raw_result': result['result']
            }
        else:
            return {
                'success': False,
                'type': 'math',
                'description': f"Math calculation: {task['content']}",
                'error': result['error']
            }

    def execute_translation_step(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a translation step."""
        result = self.translator.process_translation_query(task['content'])
        if result['success']:
            return {
                'success': True,
                'type': 'translation',
                'description': f"Translation: {task['content']}",
                'result': result['formatted_translation'],
                'raw_result': result['german']
            }
        else:
            return {
                'success': False,
                'type': 'translation',
                'description': f"Translation: {task['content']}",
                'error': result['error']
            }

    def execute_llm_step(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an LLM query step."""
        try:
            # Construct the prompt with system instructions
            full_prompt = f"{self.system_prompt}\n\nUser: {task['content']}\nAssistant:"
            
            # Prepare the request payload
            payload = {
                "contents": [{
                    "parts": [{
                        "text": full_prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 1,
                    "topP": 1,
                    "maxOutputTokens": 300,
                    "stopSequences": []
                },
                "safetySettings": [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    }
                ]
            }
            
            # Make the API request
            headers = {
                'Content-Type': 'application/json',
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    llm_response = candidate['content']['parts'][0]['text'].strip()
                    return {
                        'success': True,
                        'type': 'llm',
                        'description': f"General query: {task['content']}",
                        'result': llm_response,
                        'raw_result': llm_response
                    }
            
            return {
                'success': False,
                'type': 'llm',
                'description': f"General query: {task['content']}",
                'error': "Could not generate response from LLM"
            }
            
        except Exception as e:
            return {
                'success': False,
                'type': 'llm',
                'description': f"General query: {task['content']}",
                'error': f"LLM error: {str(e)}"
            }

    def process_multi_step_query(self, user_input: str) -> str:
        """
        Process a multi-step query by breaking it down and executing each step.
        
        Args:
            user_input: The user's input string
            
        Returns:
            str: The comprehensive response
        """
        # Clear previous memory
        self.clear_memory()
        
        # Parse the query into steps
        steps = self.parse_multi_step_query(user_input)
        
        if len(steps) <= 1:
            # Single step query - execute directly
            if len(steps) == 1:
                step = steps[0]
                if step['type'] == 'math':
                    result = self.execute_math_step(step)
                elif step['type'] == 'translation':
                    result = self.execute_translation_step(step)
                else:
                    result = self.execute_llm_step(step)
                
                if result['success']:
                    return result['result']
                else:
                    return f"❌ Error: {result['error']}"
            else:
                # No clear steps found, treat as general LLM query
                result = self.execute_llm_step({'content': user_input, 'type': 'llm'})
                if result['success']:
                    return result['result']
                else:
                    return f"❌ Error: {result['error']}"
        
        # Multi-step query
        response_parts = [f"🔍 Multi-step task detected! Breaking down your request:\n"]
        
        for i, step in enumerate(steps, 1):
            response_parts.append(f"**Step {i}**: {step['original_text']}")
            
            # Execute the step
            if step['type'] == 'math':
                result = self.execute_math_step(step)
            elif step['type'] == 'translation':
                result = self.execute_translation_step(step)
            else:
                result = self.execute_llm_step(step)
            
            # Add result to response and memory
            if result['success']:
                response_parts.append(f"✅ Result: {result['result']}")
                self.add_to_memory(result['description'], result['raw_result'])
            else:
                response_parts.append(f"❌ Error: {result['error']}")
                return "\n".join(response_parts)  # Stop on first error
            
            response_parts.append("")  # Add blank line
        
        # Add summary
        if len(self.memory['completed_steps']) > 1:
            response_parts.append("📋 **Task Summary**:")
            for step_result in self.memory['previous_results']:
                response_parts.append(f"• {step_result['step']} → {step_result['result']}")
        
        return "\n".join(response_parts)

    def chat_loop(self):
        """
        Main chat loop for the CLI interface.
        """
        print("🤖 Level 3 Full Agent - Multi-Step Reasoning Chatbot")
        print("=" * 60)
        print("Welcome! I can handle complex multi-step tasks including:")
        print("• Math calculations (addition, multiplication)")
        print("• English to German translations")
        print("• General questions and explanations")
        print("• Multi-step combinations of the above!")
        print("\nExamples:")
        print('• "Translate \'Good Morning\' into German and then multiply 5 and 6"')
        print('• "Add 10 and 20, then translate \'Have a nice day\' into German"')
        print('• "Tell me the capital of Italy, then multiply 12 and 12"')
        print("Type 'quit', 'exit', or 'bye' to end the conversation.\n")
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("\n🤖 Full Agent: Goodbye! Thanks for chatting with me!")
                    break
                
                # Skip empty inputs
                if not user_input:
                    continue
                
                # Process the input and get response
                print("\n🤖 Full Agent:")
                response = self.process_multi_step_query(user_input)
                print(f"{response}\n")
                
            except KeyboardInterrupt:
                print("\n\n🤖 Full Agent: Goodbye! Thanks for chatting with me!")
                break
            except Exception as e:
                print(f"\n🤖 Full Agent: Sorry, an error occurred: {str(e)}\n")


def main():
    """
    Main function to run the Level 3 Full Agent.
    """
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
    try:
        # Initialize agent
        agent = FullAgent()
        
        # Start chat loop
        agent.chat_loop()
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nTo fix this:")
        print("1. Get a Gemini API key from: https://makersuite.google.com/app/apikey")
        print("2. Set it as an environment variable: set GEMINI_API_KEY=your_api_key_here")
        print("3. Or pass it directly when creating the agent instance")
        
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
