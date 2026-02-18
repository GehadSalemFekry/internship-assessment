from flask import Flask, request, jsonify
from collections import deque
import re
from typing import Tuple, Optional

app = Flask(__name__)

# Global state for history (queue)
MAX_HISTORY = 5
HISTORY = deque(maxlen=MAX_HISTORY)
SUPPORTED_OPERATORS = {"+", "-", "*", "/"}


def validate_expression(expression: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that expression contains only supported operators and digits/spaces.

    Returns:
        (is_valid, error_message)
    """
    invalid_chars = set(re.findall(r"[^\d\s\+\-\*/]", expression))
    if invalid_chars:
        unsupported_str = " ".join(sorted(invalid_chars))
        supported_str = " ".join(sorted(SUPPORTED_OPERATORS))
        return (
            False,
            f"Unsupported operators: {unsupported_str}\nSupported operators: {supported_str}",
        )

    return True, None


def evaluate_expression(expression: str) -> Tuple[Optional[float], Optional[str]]:
    """
    Safely evaluate an arithmetic expression.

    Returns:
        (result, error_message)
    """
    try:
        result = eval(expression)

        # Return as int if it's a whole number, otherwise float
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return result, None

    except ZeroDivisionError:
        return None, "Error: Division by zero"
    except Exception as e:
        return None, f"Error: Invalid expression - {str(e)}"


@app.route("/calculate", methods=["POST"])
def calculate():
    """
    Calculate arithmetic expression endpoint.

    Request: {"expression": "10 + 10 + 3 - 5"}
    Response: {"result": "18"}
    """
    try:
        data = request.get_json()

        if not data or "expression" not in data:
            return jsonify({"error": "Missing 'expression' field"}), 400

        expression = str(data["expression"])

        # Validate operators
        is_valid, error_msg = validate_expression(expression)
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Evaluate expression
        result, error_msg = evaluate_expression(expression)
        if error_msg:
            return jsonify({"error": error_msg}), 400

        # Add to history
        history_entry = f"{expression} = {result}"
        HISTORY.append(history_entry)

        return jsonify({"result": str(result)}), 200

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/history", methods=["GET"])
def get_history():
    """Get calculation history."""
    return jsonify({"history": list(HISTORY)}), 200


@app.route("/clear-history", methods=["POST"])
def clear_history():
    """Clear calculation history."""
    HISTORY.clear()
    return jsonify({"message": "History cleared"}), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "OK"}), 200


if __name__ == "__main__":
    print("Starting Flask calculator API...")
    print("Available endpoints:")
    print("  POST   /calculate           - Evaluate expression")
    print("  GET    /history             - Get calculation history")
    print("  POST   /clear-history       - Clear history")
    print("  GET    /health              - Health check")
    app.run(debug=True, port=5000)
