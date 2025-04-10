import ast
import traceback
import io
import contextlib
# Custom Hints DB
HINTS = {
    "IndexError": [
        "Consider revisiting how elements are being accessed within your sequence.",
        "Check if the index used exceeds the bounds of the list or array.",
        "You're trying to access a position that doesn’t exist in the sequence — list indices must be within range."
    ],
    "NameError": [
        "It appears a reference may not correspond to a defined identifier.",
        "Ensure all variables or functions are declared before being used.",
        "A variable or function is being used before it has been defined — please check for typos or omissions."
    ],
    "SyntaxError": [
        "There might be an inconsistency in the structure or formatting of the code.",
        "Review your use of colons, parentheses, or quotation marks for completeness.",
        "The code contains a syntax error — likely due to missing punctuation or incorrect indentation."
    ],
    "ZeroDivisionError": [
        "Reevaluate the operands involved in arithmetic expressions.",
        "Ensure that no division operations involve a zero denominator.",
        "You're dividing by zero, which is mathematically undefined and not allowed in Python."
    ],
    "TypeError": [
        "The operation might be applied to elements of incompatible types.",
        "Verify that operands belong to compatible data types before combining them.",
        "You're attempting an operation with mismatched types — such as adding a string to an integer."
    ],
    "AttributeError": [
        "An object may not support the requested operation or characteristic.",
        "Check whether the attribute or method actually exists for the object's type.",
        "You're accessing an attribute or method that does not exist for this object."
    ],
    "KeyError": [
        "A dictionary lookup might be referencing an unavailable key.",
        "Consider verifying the presence of the key before accessing its value.",
        "You're attempting to access a key that doesn't exist in the dictionary."
    ],
    "ValueError": [
        "The function may be receiving input that is semantically inappropriate.",
        "Confirm that values passed into functions meet their expected format or constraints.",
        "You're passing an invalid value — for example, trying to convert a non-numeric string to an integer."
    ],
    "ImportError": [
        "There may be an issue resolving external references or modules.",
        "Verify that the module or object you're importing is correctly named and available.",
        "The import failed — the specified module or component doesn't exist or isn't installed."
    ],
    "IndentationError": [
        "The layout of your code blocks may not conform to expected alignment.",
        "Ensure consistent indentation throughout your script using either spaces or tabs (not both).",
        "Your code's indentation is incorrect — Python requires properly aligned blocks."
    ],
    "UnboundLocalError": [
        "A variable might be interpreted locally without prior assignment.",
        "Check if you're referencing a variable before defining it within the function.",
        "You're using a local variable before assigning it — use the global keyword if needed."
    ],
    "RecursionError": [
        "There could be an excessively deep call chain in your function.",
        "Ensure that the recursive function includes a termination condition.",
        "Your recursive function is calling itself endlessly — this has exceeded Python's recursion limit."
    ],
    "FileNotFoundError": [
        "The resource being accessed may not be available in the expected location.",
        "Double-check the filename and its path for any errors.",
        "The file you're trying to open does not exist — verify the path and filename."
    ],
    "ModuleNotFoundError": [
        "The system may be unable to locate the specified external module.",
        "Make sure the module name is spelled correctly and that it's installed.",
        "Python can't find the module — it’s either missing or not installed. Try using pip install."
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
        stdout_buffer = io.StringIO()
        with contextlib.redirect_stdout(stdout_buffer):
            exec(code, {})
        output = stdout_buffer.getvalue()
        return [], None, output.strip()
    except Exception as e:
        tb = traceback.format_exc()
        error_type = e.__class__.__name__
        hints = HINTS.get(error_type, ["An error occurred, but no hints found."])
        return hints,tb,None
