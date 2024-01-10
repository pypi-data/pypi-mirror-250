class Calculator:

    def __init__(self):
        # Initialize memory to zero
        self._memory = 0

    @property
    def memory(self):
        """Get the value stored in memory."""
        return self._memory

    def reset_memory(self):
        """Reset the memory to zero."""
        self._memory = 0

    def add(self, first_number: float = 0, second_number: float = 0) -> float:
        """Add two numbers."""
        result = first_number + second_number
        self._memory = result
        return result

    def subtract(self, first_number: float = 0, second_number: float = 0) -> float:
        """Subtract Function."""
        result = first_number - second_number
        self._memory = result
        return result

    def multiply(self, first_number: float = 0, second_number: float = 0) -> float:
        """Multiply Function."""
        result = first_number * second_number
        self._memory = result
        return result

    def divide(self, first_number: float = 0, second_number: float = 0) -> float:
        """Divide Function."""
        if second_number == 0:
            raise ValueError('Not divisible by zero!')
        result = first_number / second_number
        self._memory = result
        return result

    def nth_root(self, first_number: float, n: int) -> float:
        """Calculate the nth root of a number."""
        if first_number < 0 and n % 2 == 0:
            raise ValueError('Cannot calculate the even root of a negative number')
        result = first_number ** (1/n)
        self._memory = result
        return result
