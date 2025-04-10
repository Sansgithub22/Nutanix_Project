import ast
import traceback

# Custom Hints DB
HINTS = {
    "IndexError": [
        "Are you trying to access an index that’s out of range?",
        "Check the length of your list or array.",
        "Remember: indexing starts at 0 in Python."
    ],
    "NameError": [
        "Are you using a variable before defining it?",
        "Check for typos in variable or function names.",
        "Ensure you’ve declared all your variables."
    ],
    "SyntaxError": [
        "Is there a missing colon, parenthesis, or quote?",
        "Check indentation and line endings.",
        "Syntax errors often show up one line after the actual mistake."
    ],
    "ZeroDivisionError": [
        "You're dividing a number by zero.",
        "Add a check before the division operation.",
        "Use try-except to handle divide-by-zero gracefully."
    ],
    "TypeError": [
        "Are you mixing incompatible data types?",
        "You might be adding a string and an integer.",
        "Try converting types explicitly using int(), str(), etc."
    ],
    "AttributeError": [
        "Does the object really have that attribute or method?",
        "Check the object's type before calling the attribute.",
        "Use dir(object) to inspect available attributes."
    ],
    "KeyError": [
        "The key you’re accessing doesn’t exist in the dictionary.",
        "Check if the key exists using key in dict.",
        "Use .get(key) to safely access values."
    ],
    "ValueError": [
        "You're passing an inappropriate value to a function.",
        "Ensure the value fits the expected format or range.",
        "Wrap risky conversions (like int('abc')) in try-except blocks."
    ],
    "ImportError": [
        "The module you're trying to import doesn’t exist or isn’t installed.",
        "Check the module name for typos.",
        "Try installing it with pip install."
    ],
    "IndentationError": [
        "Python relies on indentation for block structure.",
        "Ensure consistent use of tabs or spaces (not both).",
        "Each block (if, for, def, etc.) must be properly indented."
    ],
    "UnboundLocalError": [
        "You’re using a local variable before assigning it.",
        "Declare the variable before using it.",
        "Use the global keyword if you’re modifying a global variable."
    ],
    "RecursionError": [
        "You’ve exceeded the maximum recursion depth.",
        "Make sure your recursive function has a base case.",
        "Check that each recursive call gets closer to the base case."
    ],
    "FileNotFoundError": [
        "The file path might be incorrect or the file doesn’t exist.",
        "Check if the file name and location are correct.",
        "Use os.path.exists() to confirm the file’s presence."
    ],
    "ModuleNotFoundError": [
        "The module you're trying to import isn't installed.",
        "Check for typos in the module name.",
        "Install it using pip install module_name."
    ]
}

def get_ast_warnings(code):
    warnings = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'id') and node.func.id == 'eval':
                    warnings.append("Try to avoid using `eval()` unless necessary.")
            if isinstance(node, ast.FunctionDef) and len(node.body) > 20:
                warnings.append(f"Function `{node.name}` might be doing too much. Consider splitting it.")
    except SyntaxError:
        warnings.append("Could not parse code due to syntax error.")
    return warnings

def execute_code(code):
    try:
        exec(code, {})
        return [], None
    except Exception as e:
        tb = traceback.format_exc()
        error_type = e.__class__.__name__
        hints = HINTS.get(error_type, ["An error occurred, but no hints found."])
        return hints, tb
