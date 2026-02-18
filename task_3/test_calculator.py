import requests
import json
from time import sleep

BASE_URL = "http://127.0.0.1:5000"


def test_calculator():
    """Test the calculator API with various inputs."""

    print("\n" + "=" * 60)
    print("CALCULATOR API TEST SUITE")
    print("=" * 60)

    test_cases = [
        ("10 + 10 + 3 - 5", "18", "Basic arithmetic"),
        ("5 * 2", "10", "Multiplication"),
        ("20 / 4", "5", "Division"),
        ("10 + 5 * 2 + 10 / 2", "25", "Order of operations"),
        ("10 / 4", "2.5", "Division with float result"),
        ("100 - 50 + 25", "75", "Multiple operations"),
        ("(10 + 5) * 2", "30", "Parentheses (should fail)"),
        ("10 / 0", None, "Division by zero (should fail)"),
        ("10 ^ 2", None, "Unsupported operator (should fail)"),
        ("10 + ", None, "Invalid expression (should fail)"),
    ]

    for i, (expression, expected, description) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {description}")
        print(f"  Expression: {expression}")

        try:
            response = requests.post(
                f"{BASE_URL}/calculate", json={"expression": expression}, timeout=5
            )

            if response.status_code == 200:
                result = response.json()["result"]
                print(f"  ✓ Result: {result}")
                if expected:
                    print(
                        f"    Expected: {expected}, Got: {result}, Match: {result == expected}"
                    )
            else:
                error = response.json()["error"]
                print(f"  ✗ {error}")

        except requests.exceptions.ConnectionError:
            print("  ✗ Connection error - is the server running?")
            return
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")

    # Check history
    print("\n" + "-" * 60)
    print("HISTORY")
    print("-" * 60)
    try:
        response = requests.get(f"{BASE_URL}/history", timeout=5)
        history = response.json()["history"]
        print(f"Last {len(history)} successful calculations:")
        for entry in history:
            print(f"  • {entry}")
    except Exception as e:
        print(f"Error fetching history: {e}")


if __name__ == "__main__":
    print("To run this test:")
    print("1. Start the calculator server: python task_3/calculator.py")
    print("2. In another terminal: python task_3/test_calculator.py")
    print()
    input("Press Enter when the server is running...")

    test_calculator()
