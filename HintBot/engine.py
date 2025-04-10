import ast
import traceback
import sys

# Custom Hints DB
HINTS = {
    "IndexError": [
        "Check how you're indexing lists.",
        "Are you accessing an index that doesn't exist?",
        "Review zero-based indexing in Python."
    ],
    "NameError": [
        "You're using a variable that hasn't been defined yet.",
        "Check for typos or variable scope issues.",
        "Review Python variable declaration rules."
    ],
    "SyntaxError": [
        "There's a syntax mistake. Look for missing colons, brackets, or wrong indentation.",
        "Check if you're using keywords properly.",
        "Try running your code line-by-line to isolate the error."
    ],
    "ZeroDivisionError": [
        "You're dividing by zero.",
        "Make sure the denominator isn't zero before dividing.",
        "Review Python division rules."
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
    except SyntaxError as e:
        warnings.append("Could not parse code due to syntax error.")
    return warnings

def execute_code(code):
    try:
        exec(code, {})
        return [], None  # no errors
    except Exception as e:
        tb = traceback.format_exc()
        error_type = e.__class__.__name__
        hints = HINTS.get(error_type, ["An error occurred, but no hints found."])
        return hints, tb
