import openai
import json
from dotenv import load_dotenv
import os
from db_helper import get_marks, get_fees

#Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key= os.getenv("OPENAI_API_KEY")

def ask_openai(question):
    """Ask a question to OpenAI and handle function calls."""
    # Define available functions for OpenAI
    functions = [
        {
            "name": "get_marks",
            "description": """Get the GPA for a college student or aggregate GPA (such as average, min, max) 
            for a given semester. Returns -1 if no record is found.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "student_name": {
                        "type": "string",
                        "description": "First and last name of the student, e.g., Peter Pandey"
                    },
                    "semester": {
                        "type": "integer",
                        "description": "A number between 1 to 4 indicating the semester"
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["max", "min", "avg"],
                        "description": """If student_name is blank, specifies aggregate operation (max, min, avg) 
                        for the semester."""
                    }
                },
                "required": ["semester"]
            }
        },
        {
            "name": "get_fees",
            "description": """Get the fees for an individual student or total fees for a semester. 
            Returns -1 if no record is found.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "student_name": {
                        "type": "string",
                        "description": "First and last name of the student, e.g., Peter Pandey"
                    },
                    "semester": {
                        "type": "integer",
                        "description": "A number between 1 to 4 indicating the semester"
                    },
                    "fees_type": {
                        "type": "string",
                        "enum": ["paid", "pending", "total"],
                        "description": "Type of fees: paid, pending, or total"
                    }
                },
                "required": ["semester"]
            }
        }
    ]

    # Make the initial OpenAI API call
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            functions=functions,
            function_call="auto"
        )
        response_message = response.choices[0].message

        # Check if a function call was triggered
        if response_message.function_call:
            function_name = response_message.function_call.name
            function_args = json.loads(response_message.function_call.arguments)

            # Map function names to actual functions
            available_functions = {
                "get_marks": get_marks,
                "get_fees": get_fees
            }
            function_to_call = available_functions[function_name]
            function_response = function_to_call(function_args)

            # Make a second OpenAI call to get a human-readable response
            messages = [
                {"role": "user", "content": question},
                response_message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": str(function_response)
                }
            ]
            second_response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return second_response.choices[0].message.content
        else:
            # Return direct response for general questions
            return response_message.content

    except Exception as e:
        return f"Error processing question: {str(e)}"
