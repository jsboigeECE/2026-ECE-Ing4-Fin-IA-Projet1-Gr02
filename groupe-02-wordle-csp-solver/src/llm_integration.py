"""
LLM Integration with Function Calling for Wordle Solver.
Uses OpenAI's function calling to leverage LLM reasoning with CSP solving.
"""

import os
import json
from typing import List, Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv


class WordleLLMAssistant:
    """
    LLM-powered assistant for Wordle solving using function calling.
    Combines linguistic reasoning with CSP-based constraint solving.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize LLM assistant.

        Args:
            api_key: OpenAI API key (reads from env if not provided)
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            print("Warning: No OpenAI API key found. LLM features will be disabled.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)

        self.conversation_history = []

    def get_function_definitions(self) -> List[Dict]:
        """
        Define functions available to the LLM for Wordle solving.

        Returns:
            List of function definitions
        """
        return [
            {
                "name": "apply_wordle_constraints",
                "description": "Apply constraints from a Wordle guess feedback to filter possible words",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "guess": {
                            "type": "string",
                            "description": "The word that was guessed (5 letters)"
                        },
                        "feedback": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["green", "yellow", "gray"]
                            },
                            "description": "Feedback for each letter: green (correct position), yellow (wrong position), gray (not in word)"
                        }
                    },
                    "required": ["guess", "feedback"]
                }
            },
            {
                "name": "get_possible_words",
                "description": "Get list of all words that satisfy current constraints",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of words to return (default: 20)",
                            "default": 20
                        }
                    }
                }
            },
            {
                "name": "suggest_best_guess",
                "description": "Get the optimal next guess based on information theory and constraint satisfaction",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "strategy": {
                            "type": "string",
                            "enum": ["max_info", "first", "random"],
                            "description": "Strategy for selecting guess: max_info (maximize information gain), first (alphabetically first), random",
                            "default": "max_info"
                        }
                    }
                }
            },
            {
                "name": "get_solver_stats",
                "description": "Get current statistics about the solving process",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "analyze_word_pattern",
                "description": "Analyze linguistic patterns in remaining words to find common features",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "aspect": {
                            "type": "string",
                            "enum": ["letter_frequency", "vowel_positions", "common_prefixes", "common_suffixes"],
                            "description": "Aspect of words to analyze"
                        }
                    },
                    "required": ["aspect"]
                }
            }
        ]

    def chat_with_context(
        self,
        user_message: str,
        available_functions: Dict,
        model: str = "gpt-4-turbo-preview"
    ) -> str:
        """
        Chat with LLM using function calling for Wordle assistance.

        Args:
            user_message: User's message
            available_functions: Dictionary mapping function names to callable functions
            model: OpenAI model to use

        Returns:
            LLM's response
        """
        if not self.client:
            return "LLM integration is disabled. Please set OPENAI_API_KEY."

        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Initial LLM call
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert Wordle solver assistant. You help users solve Wordle puzzles by:
1. Analyzing feedback from guesses (green/yellow/gray)
2. Using constraint satisfaction to filter possible words
3. Suggesting optimal next guesses based on information theory
4. Explaining your reasoning and strategy

When the user provides feedback from a guess, use the apply_wordle_constraints function.
To suggest the next guess, use suggest_best_guess function.
Always explain your reasoning and strategy to help the user learn."""
                }
            ] + self.conversation_history,
            functions=self.get_function_definitions(),
            function_call="auto"
        )

        assistant_message = response.choices[0].message

        # Handle function calls
        if assistant_message.function_call:
            function_name = assistant_message.function_call.name
            function_args = json.loads(assistant_message.function_call.arguments)

            # Execute the function
            if function_name in available_functions:
                function_response = available_functions[function_name](**function_args)

                # Add function call and response to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": None,
                    "function_call": {
                        "name": function_name,
                        "arguments": assistant_message.function_call.arguments
                    }
                })
                self.conversation_history.append({
                    "role": "function",
                    "name": function_name,
                    "content": json.dumps(function_response)
                })

                # Get final response from LLM
                second_response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are an expert Wordle solver assistant."}
                    ] + self.conversation_history
                )

                final_message = second_response.choices[0].message.content
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_message
                })

                return final_message
            else:
                return f"Function {function_name} not available."

        # No function call, return direct response
        response_content = assistant_message.content
        self.conversation_history.append({
            "role": "assistant",
            "content": response_content
        })

        return response_content

    def suggest_next_guess(
        self,
        possible_words: List[str],
        attempt_number: int,
        previous_guesses: List[str]
    ) -> Dict[str, str]:
        """
        Use LLM reasoning to suggest next guess with explanation.

        Args:
            possible_words: List of currently possible words
            attempt_number: Current attempt number
            previous_guesses: List of previous guesses

        Returns:
            Dictionary with 'guess' and 'reasoning'
        """
        if not self.client:
            return {
                "guess": possible_words[0] if possible_words else None,
                "reasoning": "LLM disabled, returning first possible word"
            }

        prompt = f"""Based on the Wordle solving process:
- Attempt number: {attempt_number}
- Previous guesses: {', '.join(previous_guesses) if previous_guesses else 'None'}
- Number of possible words remaining: {len(possible_words)}
- Sample possible words: {', '.join(possible_words[:10])}

Suggest the best next guess and explain your reasoning. Consider:
1. Information gain (eliminate maximum words)
2. Common letter patterns
3. Balancing exploration vs exploitation
"""

        return self.chat_with_context(prompt, {})

    def analyze_game_state(
        self,
        possible_words: List[str],
        constraints: Dict
    ) -> str:
        """
        Analyze current game state and provide insights.

        Args:
            possible_words: Currently possible words
            constraints: Current constraints

        Returns:
            Analysis text
        """
        if not self.client:
            return f"{len(possible_words)} words remaining"

        prompt = f"""Analyze this Wordle game state:
- Possible words remaining: {len(possible_words)}
- Sample words: {', '.join(possible_words[:15])}
- Known correct positions: {constraints.get('correct_positions', {})}
- Present letters: {constraints.get('present_letters', set())}
- Absent letters: {constraints.get('absent_letters', set())}

Provide strategic insights about:
1. How constrained the solution is
2. Patterns in remaining words
3. Best approach for next guess
"""

        return self.chat_with_context(prompt, {})

    def reset_conversation(self) -> None:
        """Reset conversation history."""
        self.conversation_history = []
