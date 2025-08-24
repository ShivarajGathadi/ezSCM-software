"""
Level 2 Chatbot - CLI Interface with Tool Integration
===================================================

An enhanced chatbot that integrates with Google's Gemini API and uses a calculator tool
for mathematical operations. Provides structured responses and handles tool delegation.
"""

import os
import re
import json
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from calculator_tool import CalculatorTool


class Level2Chatbot:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Level 2 Chatbot with Gemini API and tool integration.
        
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
        
        # Initialize calculator tool
        self.calculator = CalculatorTool()
        
        # System prompt for structured responses
        self.system_prompt = """You are a helpful assistant that provides structured, step-by-step answers. 

IMPORTANT RULES:
1. Always structure your responses with clear steps using numbered lists or bullet points
2. Break down complex topics into digestible parts
3. Be conversational but informative
4. Keep responses concise but thorough
5. Do NOT perform mathematical calculations - those are handled by external tools

Note: Mathematical calculations are handled by specialized tools, not by you directly.
"""

    def detect_multiple_tasks(self, user_input: str) -> bool:
        """
        Detect if the user input contains multiple different types of tasks.
        
        Args:
            user_input: The user's input string
            
        Returns:
            bool: True if multiple tasks detected, False otherwise
        """
        user_input_lower = user_input.lower()
        
        # Check for math operations
        has_math = self.calculator.is_supported_math_query(user_input)
        
        # Check for non-math questions/requests
        non_math_indicators = [
            r'what\s+is\s+(?![\d\s+\-\*/]+[\d\s]*$)',  # "what is" not followed by just math
            r'how\s+(?:do|to)',  # "how do", "how to"
            r'tell\s+me',  # "tell me"
            r'explain',  # "explain"
            r'capital\s+of',  # "capital of"
            r'who\s+is',  # "who is"
            r'where\s+is',  # "where is"
            r'when\s+(?:did|was)',  # "when did", "when was"
            r'why\s+(?:is|do)',  # "why is", "why do"
            r'help\s+me',  # "help me"
            r'can\s+you',  # "can you"
        ]
        
        has_non_math = False
        for pattern in non_math_indicators:
            if re.search(pattern, user_input_lower):
                has_non_math = True
                break
        
        # Check for connecting words that might indicate multiple tasks
        connecting_words = [
            r'\s+and\s+(?:also\s+)?(?:tell|explain|what|how|who|where|when|why)',
            r'\s+also\s+',
            r'\s+plus\s+(?:tell|explain|what|how|who|where|when|why)',
            r'\s+then\s+',
            r',\s*(?:and\s+)?(?:tell|explain|what|how|who|where|when|why)',
        ]
        
        has_connecting_words = False
        for pattern in connecting_words:
            if re.search(pattern, user_input_lower):
                has_connecting_words = True
                break
        
        # Multiple tasks if we have both math and non-math, or connecting words
        return (has_math and has_non_math) or (has_connecting_words and (has_math or has_non_math))

    def get_multiple_tasks_response(self) -> str:
        """
        Return a standardized response for multiple task requests.
        
        Returns:
            str: Response explaining inability to handle multiple tasks
        """
        return """I cannot yet handle multiple tasks at once. Please ask me one thing at a time.

For example:
✅ Good: "What is 15 + 23?"
✅ Good: "What is the capital of Japan?"
❌ Too complex: "Multiply 9 and 8, and also tell me the capital of Japan"

Please separate your questions and I'll be happy to help with each one individually!"""

    def query_llm(self, user_message: str) -> str:
        """
        Send a query to the Gemini API and get a structured response.
        
        Args:
            user_message: The user's input message
            
        Returns:
            str: The LLM's response
        """
        try:
            # Construct the prompt with system instructions
            full_prompt = f"{self.system_prompt}\n\nUser: {user_message}\nAssistant:"
            
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
                    "maxOutputTokens": 500,
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
                    return candidate['content']['parts'][0]['text'].strip()
            
            return "Sorry, I couldn't generate a response. Please try again."
            
        except requests.exceptions.RequestException as e:
            return f"Sorry, I encountered a network error: {str(e)}"
        except Exception as e:
            return f"Sorry, I encountered an error while processing your request: {str(e)}"

    def process_user_input(self, user_input: str) -> str:
        """
        Process user input and determine whether to use tools or LLM.
        
        Args:
            user_input: The user's input string
            
        Returns:
            str: The appropriate response
        """
        # Check for multiple tasks first
        if self.detect_multiple_tasks(user_input):
            return self.get_multiple_tasks_response()
        
        # Check if it's a supported math query
        if self.calculator.is_supported_math_query(user_input):
            # Use calculator tool
            calc_result = self.calculator.process_math_query(user_input)
            
            if calc_result['success']:
                return f"🧮 Calculator Result: {calc_result['formatted_calculation']}"
            else:
                return f"🧮 Calculator Error: {calc_result['error']}\n\nSupported examples:\n" + \
                       "\n".join([f"• {ex}" for ex in calc_result.get('supported_examples', [])])
        
        # For non-math queries, use the LLM
        return self.query_llm(user_input)

    def chat_loop(self):
        """
        Main chat loop for the CLI interface.
        """
        print("🤖 Level 2 Chatbot - CLI Interface with Tool Integration")
        print("=" * 60)
        print("Welcome! I can help with:")
        print("• General questions (structured, step-by-step answers)")
        print("• Basic math calculations (addition and multiplication)")
        print("• Note: I cannot handle multiple tasks in one request")
        print("Type 'quit', 'exit', or 'bye' to end the conversation.\n")
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("\n🤖 Chatbot: Goodbye! Thanks for chatting with me!")
                    break
                
                # Skip empty inputs
                if not user_input:
                    continue
                
                # Process the input and get response
                print("\n🤖 Chatbot: ", end="")
                response = self.process_user_input(user_input)
                print(f"{response}\n")
                
            except KeyboardInterrupt:
                print("\n\n🤖 Chatbot: Goodbye! Thanks for chatting with me!")
                break
            except Exception as e:
                print(f"\n🤖 Chatbot: Sorry, an error occurred: {str(e)}\n")


def main():
    """
    Main function to run the Level 2 Chatbot.
    """
    load_dotenv()
    try:
        # Initialize chatbot
        chatbot = Level2Chatbot()
        
        # Start chat loop
        chatbot.chat_loop()
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nTo fix this:")
        print("1. Get a Gemini API key from: https://makersuite.google.com/app/apikey")
        print("2. Set it as an environment variable: set GEMINI_API_KEY=your_api_key_here")
        print("3. Or pass it directly when creating the chatbot instance")
        
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
