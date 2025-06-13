# Calculator app with style issues
import math


class calculator:  # Class name should be capitalized
    def __init__(self):
        self.result = 0  # Missing spaces around operator

    def add(self, a, b):  # Missing spaces in parameters
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        return a / b  # No zero division check

    def power(self, base, exp):
        return math.pow(base, exp)


def main():
    calc = calculator()
    print("Calculator ready!")

    # Long line that exceeds 80 characters and should be split for better readability
    result = (
        calc.add(10, 5)
        + calc.multiply(3, 4)
        + calc.power(2, 3)
        + calc.subtract(100, 25)
    )
    print(f"Complex calculation result: {result}")


if __name__ == "__main__":
    main()
