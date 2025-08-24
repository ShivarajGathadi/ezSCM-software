"""
Level 1 Chatbot - CLI Interface with Gemini API Integration
========================================================

A simple command-line chatbot that integrates with Google's Gemini API to provide
structured, step-by-step responses while refusing mathematical calculations.
"""

import os
import re
import json
import requests
from typing import Optional
from dotenv import load_dotenv


class Level1Chatbot:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Level 1 Chatbot with Gemini API integration.
        
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
        
        # System prompt for structured responses
        self.system_prompt = """You are a helpful assistant that provides structured, step-by-step answers. 

IMPORTANT RULES:
1. Always structure your responses with clear steps using numbered lists or bullet points
2. Break down complex topics into digestible parts
3. If the user asks ANY mathematical calculation (addition, subtraction, multiplication, division, percentages, etc.), you MUST refuse and suggest they use a calculator tool instead
4. Be conversational but informative
5. Keep responses concise but thorough

MATH REFUSAL TEMPLATE:
"I cannot perform mathematical calculations. Please use a calculator tool or app for accurate results. I'm here to help with explanations, advice, and general information instead!"
"""

    def is_math_question(self, user_input: str) -> bool:
        """
        Detect if the user input contains mathematical calculations.
        
        Args:
            user_input: The user's input string
            
        Returns:
            bool: True if math calculation detected, False otherwise
        """
        # Patterns that indicate math calculations
        math_patterns = [
            r'\d+\s*[\+\-\*\/\%]\s*\d+',  # Basic arithmetic: 15 + 23, 10 * 5, etc.
            r'what\s+is\s+\d+.*[\+\-\*\/\%]',  # "what is 15 + 23"
            r'calculate\s+\d+',  # "calculate 50 + 30"
            r'\d+\s+plus\s+\d+',  # "15 plus 23"
            r'\d+\s+minus\s+\d+',  # "30 minus 10"
            r'\d+\s+times\s+\d+',  # "5 times 6"
            r'\d+\s+divided\s+by\s+\d+',  # "20 divided by 4"
            r'add\s+\d+.*\d+',  # "add 5 and 7"
            r'subtract\s+\d+.*\d+',  # "subtract 3 from 10"
            r'multiply\s+\d+.*\d+',  # "multiply 4 by 6"
            r'percentage\s+of\s+\d+',  # "10 percentage of 100"
            r'\d+%\s+of\s+\d+',  # "10% of 100"
        ]
        
        user_input_lower = user_input.lower()
        
        for pattern in math_patterns:
            if re.search(pattern, user_input_lower):
                return True
        
        return False

    def get_math_refusal_response(self) -> str:
        """
        Return a standardized response for mathematical calculation requests.
        
        Returns:
            str: Refusal message with calculator suggestion
        """
        return """I cannot perform mathematical calculations. Please use a calculator tool or app for accurate results. I'm here to help with explanations, advice, and general information instead!

Some great calculator options:
• Built-in Windows Calculator
• Google Search (just type your calculation)
• Python calculator: python -c "print(15 + 23)"
• Online calculators like calculator.net

Is there something else I can help you with today?"""

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

    def chat_loop(self):
        """
        Main chat loop for the CLI interface.
        """
        print("🤖 Level 1 Chatbot - CLI Interface")
        print("=" * 40)
        print("Welcome! I provide structured, step-by-step answers.")
        print("Note: I cannot perform mathematical calculations - use a calculator for that!")
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
                
                # Check if it's a math question
                if self.is_math_question(user_input):
                    print(f"\n🤖 Chatbot: {self.get_math_refusal_response()}\n")
                    continue
                
                # Query the LLM for non-math questions
                print("\n🤖 Chatbot: ", end="")
                response = self.query_llm(user_input)
                print(f"{response}\n")
                
            except KeyboardInterrupt:
                print("\n\n🤖 Chatbot: Goodbye! Thanks for chatting with me!")
                break
            except Exception as e:
                print(f"\n🤖 Chatbot: Sorry, an error occurred: {str(e)}\n")

def main():
    """
    Main function to run the Level 1 Chatbot.
    """
    load_dotenv()
    try:
        # Initialize chatbot
        chatbot = Level1Chatbot()
        
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
