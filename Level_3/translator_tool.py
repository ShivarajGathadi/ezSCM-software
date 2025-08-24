"""
Translator Tool - Level 3 Component
=================================

A simple translator tool that translates English text to German.
This tool is designed to be called by the Level 3 chatbot for translation queries.
"""

import re
from typing import Dict, Any, Optional


class TranslatorTool:
    """
    A basic translator tool that translates English phrases to German.
    """
    
    def __init__(self):
        """Initialize the translator tool with a basic dictionary."""
        # Basic English to German dictionary
        self.translations = {
            # Common greetings
            "hello": "hallo",
            "good morning": "guten morgen",
            "good afternoon": "guten tag",
            "good evening": "guten abend",
            "good night": "gute nacht",
            "goodbye": "auf wiedersehen",
            "bye": "tschüss",
            
            # Common phrases
            "thank you": "danke",
            "please": "bitte",
            "excuse me": "entschuldigung",
            "sorry": "es tut mir leid",
            "yes": "ja",
            "no": "nein",
            "how are you": "wie geht es dir",
            "have a nice day": "hab einen schönen tag",
            "see you later": "bis später",
            
            # Common words
            "water": "wasser",
            "food": "essen",
            "house": "haus",
            "car": "auto",
            "book": "buch",
            "dog": "hund",
            "cat": "katze",
            "friend": "freund",
            "family": "familie",
            "love": "liebe",
            "sunshine": "sonnenschein",
            "moon": "mond",
            "star": "stern",
            "flower": "blume",
            "tree": "baum",
            
            # Numbers (for reference)
            "one": "eins",
            "two": "zwei",
            "three": "drei",
            "four": "vier",
            "five": "fünf",
            "six": "sechs",
            "seven": "sieben",
            "eight": "acht",
            "nine": "neun",
            "ten": "zehn",
            
            # Time
            "today": "heute",
            "tomorrow": "morgen",
            "yesterday": "gestern",
            "time": "zeit",
            "hour": "stunde",
            "minute": "minute",
            
            # Colors
            "red": "rot",
            "blue": "blau",
            "green": "grün",
            "yellow": "gelb",
            "black": "schwarz",
            "white": "weiß"
        }
    
    def parse_translation_request(self, text: str) -> Optional[str]:
        """
        Extract the text to be translated from a translation request.
        
        Args:
            text: The input text containing a translation request
            
        Returns:
            The text to be translated, or None if not found
        """
        text_lower = text.lower().strip()
        
        # Patterns to extract text for translation
        patterns = [
            r"translate\s+['\"]([^'\"]+)['\"]",  # translate "text"
            r"translate\s+['\']([^'']+)['\']",  # translate 'text'
            r"translate\s+(.+?)\s+(?:into|to)\s+german",  # translate text into german
            r"how\s+do\s+you\s+say\s+['\"]([^'\"]+)['\"]",  # how do you say "text"
            r"what\s+is\s+['\"]([^'\"]+)['\"].+german",  # what is "text" in german
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1).strip()
        
        return None
    
    def translate_text(self, english_text: str) -> Dict[str, Any]:
        """
        Translate English text to German.
        
        Args:
            english_text: The English text to translate
            
        Returns:
            Dictionary containing translation result
        """
        try:
            english_lower = english_text.lower().strip()
            
            # Direct lookup in dictionary
            if english_lower in self.translations:
                german_text = self.translations[english_lower]
                return {
                    'success': True,
                    'english': english_text,
                    'german': german_text,
                    'formatted_translation': f'"{english_text}" → "{german_text.title()}"'
                }
            
            # Try word-by-word translation for unknown phrases
            words = english_lower.split()
            translated_words = []
            untranslated_words = []
            
            for word in words:
                # Remove punctuation for lookup
                clean_word = re.sub(r'[^\w\s]', '', word)
                if clean_word in self.translations:
                    translated_words.append(self.translations[clean_word])
                else:
                    translated_words.append(f"[{word}]")  # Mark untranslated
                    untranslated_words.append(word)
            
            if untranslated_words:
                return {
                    'success': False,
                    'error': f"Unknown words: {', '.join(untranslated_words)}",
                    'english': english_text,
                    'partial_translation': ' '.join(translated_words),
                    'available_words': list(self.translations.keys())[:10]  # Show some examples
                }
            else:
                german_text = ' '.join(translated_words)
                return {
                    'success': True,
                    'english': english_text,
                    'german': german_text,
                    'formatted_translation': f'"{english_text}" → "{german_text.title()}"'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Translation error: {str(e)}",
                'english': english_text
            }
    
    def process_translation_query(self, user_input: str) -> Dict[str, Any]:
        """
        Process a user's translation query and return the translation result.
        
        Args:
            user_input: The user's input containing a translation request
            
        Returns:
            Dictionary containing the translation result or error information
        """
        # Extract the text to translate
        text_to_translate = self.parse_translation_request(user_input)
        
        if text_to_translate is None:
            return {
                'success': False,
                'error': "Could not find text to translate. Please use format: 'Translate \"text\" into German'",
                'supported_examples': [
                    'Translate "Good Morning" into German',
                    'Translate "Thank you"',
                    'How do you say "Hello" in German?'
                ]
            }
        
        # Perform the translation
        return self.translate_text(text_to_translate)
    
    def is_translation_query(self, user_input: str) -> bool:
        """
        Check if the user input contains a translation request.
        
        Args:
            user_input: The user's input string
            
        Returns:
            bool: True if the query contains a translation request
        """
        text_to_translate = self.parse_translation_request(user_input)
        return text_to_translate is not None


def main():
    """
    Interactive translator tool for direct user input.
    """
    translator = TranslatorTool()
    
    print("🌐 Translator Tool - Interactive Mode (English → German)")
    print("=" * 60)
    print("Welcome! I can translate English text to German.")
    print("Examples:")
    print('• Translate "Good Morning" into German')
    print('• Translate "Thank you"')
    print('• How do you say "Hello" in German?')
    print("Type 'quit', 'exit', or 'bye' to end.\n")
    
    while True:
        try:
            # Get user input
            user_input = input("Translation Query: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n🌐 Translator: Goodbye! Thanks for using the translator!")
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Process the translation query
            result = translator.process_translation_query(user_input)
            
            if result['success']:
                print(f"✅ Translation: {result['formatted_translation']}\n")
            else:
                print(f"❌ Error: {result['error']}")
                if 'supported_examples' in result:
                    print("\nSupported examples:")
                    for example in result['supported_examples']:
                        print(f"  • {example}")
                elif 'available_words' in result:
                    print(f"\nPartial result: {result.get('partial_translation', 'N/A')}")
                    print("\nSome available words:")
                    for word in result['available_words']:
                        print(f"  • {word}")
                print()
                
        except KeyboardInterrupt:
            print("\n\n🌐 Translator: Goodbye! Thanks for using the translator!")
            break
        except Exception as e:
            print(f"\n🌐 Translator: Sorry, an error occurred: {str(e)}\n")


if __name__ == "__main__":
    main()
