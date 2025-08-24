"""
Calculator Tool - Level 2 Component
==================================

A simple calculator tool that performs basic mathematical operations.
This tool is designed to be called by the Level 2 chatbot for math queries.
"""

import re
from typing import Dict, Any, Optional, Tuple


class CalculatorTool:
    """
    A basic calculator tool that can perform addition and multiplication operations.
    """
    
    def __init__(self):
        """Initialize the calculator tool."""
        self.supported_operations = ['add', 'multiply', 'addition', 'multiplication', '+', '*']
    
    def parse_math_expression(self, expression: str) -> Optional[Dict[str, Any]]:
        """
        Parse a mathematical expression to extract operation and numbers.
        
        Args:
            expression: The mathematical expression as a string
            
        Returns:
            Dict containing operation type and numbers, or None if cannot parse
        """
        expression = expression.lower().strip()
        
        # Pattern for addition
        add_patterns = [
            r'(\d+(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)?)',  # "15 + 23"
            r'add\s+(\d+(?:\.\d+)?)\s+(?:and\s+|to\s+)?(\d+(?:\.\d+)?)',  # "add 15 and 23"
            r'(\d+(?:\.\d+)?)\s+plus\s+(\d+(?:\.\d+)?)',  # "15 plus 23"
            r'what\s+is\s+(\d+(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)?)',  # "what is 15 + 23"
        ]
        
        # Pattern for multiplication
        multiply_patterns = [
            r'(\d+(?:\.\d+)?)\s*\*\s*(\d+(?:\.\d+)?)',  # "5 * 6"
            r'multiply\s+(\d+(?:\.\d+)?)\s+(?:by\s+|and\s+)?(\d+(?:\.\d+)?)',  # "multiply 5 by 6"
            r'(\d+(?:\.\d+)?)\s+times\s+(\d+(?:\.\d+)?)',  # "5 times 6"
            r'what\s+is\s+(\d+(?:\.\d+)?)\s*\*\s*(\d+(?:\.\d+)?)',  # "what is 5 * 6"
        ]
        
        # Check addition patterns
        for pattern in add_patterns:
            match = re.search(pattern, expression)
            if match:
                try:
                    num1 = float(match.group(1))
                    num2 = float(match.group(2))
                    return {
                        'operation': 'addition',
                        'numbers': [num1, num2],
                        'expression': expression
                    }
                except (ValueError, IndexError):
                    continue
        
        # Check multiplication patterns
        for pattern in multiply_patterns:
            match = re.search(pattern, expression)
            if match:
                try:
                    num1 = float(match.group(1))
                    num2 = float(match.group(2))
                    return {
                        'operation': 'multiplication',
                        'numbers': [num1, num2],
                        'expression': expression
                    }
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def calculate(self, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform the calculation based on the parsed operation data.
        
        Args:
            operation_data: Dictionary containing operation type and numbers
            
        Returns:
            Dictionary containing the result and calculation details
        """
        try:
            operation = operation_data['operation']
            numbers = operation_data['numbers']
            expression = operation_data['expression']
            
            if operation == 'addition':
                result = numbers[0] + numbers[1]
                operation_symbol = '+'
            elif operation == 'multiplication':
                result = numbers[0] * numbers[1]
                operation_symbol = '*'
            else:
                return {
                    'success': False,
                    'error': f"Unsupported operation: {operation}",
                    'expression': expression
                }
            
            # Format result (remove .0 if it's a whole number)
            if result == int(result):
                result = int(result)
            
            return {
                'success': True,
                'result': result,
                'operation': operation,
                'numbers': numbers,
                'expression': expression,
                'formatted_calculation': f"{numbers[0]} {operation_symbol} {numbers[1]} = {result}"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Calculation error: {str(e)}",
                'expression': operation_data.get('expression', 'Unknown')
            }
    
    def process_math_query(self, user_input: str) -> Dict[str, Any]:
        """
        Process a user's math query and return the calculation result.
        
        Args:
            user_input: The user's input containing a math question
            
        Returns:
            Dictionary containing the calculation result or error information
        """
        # Parse the mathematical expression
        operation_data = self.parse_math_expression(user_input)
        
        if operation_data is None:
            return {
                'success': False,
                'error': "Could not parse mathematical expression. I only support basic addition and multiplication.",
                'supported_examples': [
                    "15 + 23",
                    "add 10 and 5",
                    "5 * 6",
                    "multiply 4 by 7",
                    "what is 12 + 8"
                ]
            }
        
        # Perform the calculation
        return self.calculate(operation_data)
    
    def is_supported_math_query(self, user_input: str) -> bool:
        """
        Check if the user input contains a supported mathematical operation.
        
        Args:
            user_input: The user's input string
            
        Returns:
            bool: True if the query contains supported math operations
        """
        operation_data = self.parse_math_expression(user_input)
        return operation_data is not None


def main():
    """
    Interactive calculator tool for direct user input.
    """
    calculator = CalculatorTool()
    
    print("🧮 Calculator Tool - Interactive Mode")
    print("=" * 40)
    print("Welcome! I can help with basic math operations:")
    print("• Addition: 15 + 23, add 10 and 5, 12 plus 8")
    print("• Multiplication: 5 * 6, multiply 4 by 7, 5 times 6")
    print("Type 'quit', 'exit', or 'bye' to end.\n")
    
    while True:
        try:
            # Get user input
            user_input = input("Math Query: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n🧮 Calculator: Goodbye! Thanks for using the calculator!")
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Process the math query
            result = calculator.process_math_query(user_input)
            
            if result['success']:
                print(f"✅ Result: {result['formatted_calculation']}\n")
            else:
                print(f"❌ Error: {result['error']}")
                if 'supported_examples' in result:
                    print("\nSupported examples:")
                    for example in result['supported_examples']:
                        print(f"  • {example}")
                print()
                
        except KeyboardInterrupt:
            print("\n\n🧮 Calculator: Goodbye! Thanks for using the calculator!")
            break
        except Exception as e:
            print(f"\n🧮 Calculator: Sorry, an error occurred: {str(e)}\n")


if __name__ == "__main__":
    main()
