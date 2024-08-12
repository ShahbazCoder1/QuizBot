'''
Title: Quiz Dictionary Parser with Data Validation
Code Written by: 𝗠𝗱 𝗦𝗵𝗮𝗵𝗯𝗮𝘇 𝗛𝗮𝘀𝗵𝗺𝗶 𝗔𝗻𝘀𝗮𝗿𝗶
programing languages: Python
Description: This code defines functions to parse a quiz definition string into a dictionary format, 
handling different data types like strings and options.
Copyright ©: Open-source
'''

import re
import ast

def convert_dict(dictionary_input):
    return ast.literal_eval(dictionary_input)

def escape_reserved_characters(text):
    reserved_chars = r'([._*(){}#+\-=|><!~])'
    return re.sub(reserved_chars, r'\\\1', text)

def parse_quiz_dict(quiz_str):
    quiz_dict = {}
    current_question = None
    current_field = None
    
    # Remove extra curly braces at the start and end
    quiz_str = quiz_str.strip().strip('{}')

    lines = quiz_str.split('\n')
    for line in lines:
        line = line.strip().rstrip(',')
        if not line:
            continue

        if line.startswith("'Q"):
            match = re.match(r"'(Q\d+)'\s*:\s*{", line)
            if match:
                current_question = match.group(1)
                quiz_dict[current_question] = {}
        elif line.startswith("'"):
            match = re.match(r"'(\w+)'\s*:\s*(.+)", line)
            if match:
                current_field = match.group(1)
                value = match.group(2)
                
                if value.startswith("'") and value.endswith("'"):
                    # String value
                    value = value.strip("'")
                elif value.startswith("{") and value.endswith("}"):
                    # Options dictionary
                    options = {}
                    value = value.strip("{}")
                    for option in value.split(','):
                        key, val = option.split(':')
                        key = key.strip().strip("'")
                        val = val.strip().strip("'")
                        options[key] = val
                    value = options
                
                quiz_dict[current_question][current_field] = value
        elif line.startswith("}"):
            current_question = None
            current_field = None

    return quiz_dict

def get_validated_dict(dictionary_input):
    if isinstance(dictionary_input, dict):
        return dictionary_input

    try:
        return parse_quiz_dict(dictionary_input)
    except Exception as e:
        print(f"\n{dictionary_input}\n")
        print(f"Failed to parse the quiz dictionary: {e}")
        raise ValueError(f"Failed to parse the quiz dictionary: {e}")
