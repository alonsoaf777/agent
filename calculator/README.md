# Calculator Project

## Description
This is a simple command-line calculator application written in Python. It can evaluate arithmetic expressions involving addition, subtraction, multiplication, and division.

## How it Works
The calculator project is structured into three main components:

### `main.py`
This is the entry point of the application. It handles command-line arguments, initializes the `Calculator` class from `pkg.calculator`, evaluates the expression, and prints the result in a formatted JSON output using `pkg.render`.

Key functionalities:
- Parses the expression provided as command-line arguments.
- Creates an instance of `Calculator`.
- Calls the `evaluate` method to compute the result.
- Formats the output as JSON using `format_json_output`.
- Handles potential errors during evaluation.

### `pkg/calculator.py`
This file contains the `Calculator` class, which is responsible for parsing and evaluating arithmetic expressions. It uses the Shunting-yard algorithm to convert infix expressions to postfix and then evaluates them.

Key functionalities:
- Defines supported operators (`+`, `-`, `*`, `/`) and their precedence.
- The `evaluate` method takes an infix expression string, tokenizes it, and then calls `_evaluate_infix`.
- The `_evaluate_infix` method uses two stacks: one for values (numbers) and one for operators. It processes tokens, applies operator precedence rules, and performs calculations.
- The `_apply_operator` method pops two operands and an operator from their respective stacks, performs the operation, and pushes the result back onto the values stack.
- Includes error handling for invalid tokens, insufficient operands, and malformed expressions.

### `pkg/render.py`
This file provides a utility function to format the expression and its result into a JSON string.

Key functionalities:
- The `format_json_output` function takes the original expression and the calculated result.
- It converts float results to integers if they are whole numbers for cleaner output.
- It returns a JSON string containing the expression and its result.

## How to Run
To run the calculator, navigate to the project's root directory and execute the `main.py` script with the desired arithmetic expression enclosed in quotes.

## Example Usage

```bash
python main.py "3 + 5"
# Expected output: {"expression": "3 + 5", "result": 8}

python main.py "10 / 2 - 1"
# Expected output: {"expression": "10 / 2 - 1", "result": 4}

python main.py "2 * (3 + 4)"
# Expected output: {"expression": "2 * (3 + 4)", "result": 14} (Note: Parentheses are not yet supported in this version, so this example will likely throw an error.)

python main.py "7 * 3 + 6 / 2"
# Expected output: {"expression": "7 * 3 + 6 / 2", "result": 24}
```