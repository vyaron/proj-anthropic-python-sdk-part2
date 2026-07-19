"""
Module to calculate pi to the 5th digit using the Leibniz formula.
"""

def calculate_pi(precision=5):
    """
    Calculate pi to the specified number of decimal digits.
    
    Uses the Leibniz formula: pi = 4 * (1 - 1/3 + 1/5 - 1/7 + 1/9 - ...)
    This is a simple but slow-converging series.
    
    Args:
        precision (int): Number of decimal digits of accuracy desired (default: 5)
    
    Returns:
        float: Approximation of pi
    """
    pi_estimate = 0.0
    sign = 1
    denominator = 1
    iterations = 1000000  # More iterations for better precision
    
    for i in range(iterations):
        pi_estimate += sign * (4.0 / denominator)
        sign *= -1
        denominator += 2
        
        # Early exit if we have enough precision
        if i > 100 and i % 1000 == 0:
            # Check if we've reached desired precision
            if abs(pi_estimate - 3.141592653589793) < 10 ** (-(precision + 1)):
                break
    
    return pi_estimate


def calculate_pi_machin(precision=5):
    """
    Calculate pi using Machin's formula for faster convergence.
    
    Machin's formula: pi/4 = 4*arctan(1/5) - arctan(1/239)
    This converges much faster than the Leibniz formula.
    
    Args:
        precision (int): Number of decimal digits of accuracy desired (default: 5)
    
    Returns:
        float: Approximation of pi
    """
    def arctan(x, num_terms=50):
        """Calculate arctan using Taylor series."""
        result = 0.0
        x_squared = x * x
        x_power = x
        
        for n in range(num_terms):
            term = x_power / (2 * n + 1)
            if n % 2 == 0:
                result += term
            else:
                result -= term
            x_power *= x_squared
            
            # Early exit if term is very small
            if abs(term) < 1e-15:
                break
        
        return result
    
    # Machin's formula
    pi_estimate = 4 * (4 * arctan(1/5) - arctan(1/239))
    
    return pi_estimate


def get_pi_to_5th_digit():
    """
    Get pi calculated to the 5th decimal digit.
    
    Returns:
        float: Pi approximated to at least 5 decimal digits (3.14159)
    """
    return calculate_pi_machin(precision=5)


if __name__ == "__main__":
    # Demonstrate the calculation
    pi_value = get_pi_to_5th_digit()
    print(f"Pi calculated to 5th digit: {pi_value}")
    print(f"Pi rounded to 5 decimals: {round(pi_value, 5)}")
    print(f"Actual pi value:          3.14159...")
