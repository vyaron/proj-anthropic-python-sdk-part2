"""
Test module for pie.py - tests pi calculation functions.
"""

import math
import outputs.pie as pie


def test_calculate_pi():
    """Test the basic Leibniz formula implementation."""
    print("Testing calculate_pi()...")
    result = pie.calculate_pi(precision=5)
    print(f"  Result: {result}")
    print(f"  Rounded to 5 decimals: {round(result, 5)}")
    
    # Check that it's close to the actual value of pi
    expected = math.pi
    difference = abs(result - expected)
    print(f"  Difference from math.pi: {difference}")
    
    # Should be accurate to at least 3 decimal places (being lenient with Leibniz)
    assert abs(result - expected) < 0.01, f"Result {result} too far from pi {expected}"
    print("  ✓ Test passed!")
    return True


def test_calculate_pi_machin():
    """Test the Machin formula implementation (more accurate)."""
    print("\nTesting calculate_pi_machin()...")
    result = pie.calculate_pi_machin(precision=5)
    print(f"  Result: {result}")
    print(f"  Rounded to 5 decimals: {round(result, 5)}")
    
    # Check that it's close to the actual value of pi
    expected = math.pi
    difference = abs(result - expected)
    print(f"  Difference from math.pi: {difference}")
    
    # Should be accurate to at least 5 decimal places
    assert abs(result - expected) < 0.000001, f"Result {result} too far from pi {expected}"
    print("  ✓ Test passed!")
    return True


def test_get_pi_to_5th_digit():
    """Test the main function that gets pi to 5th digit."""
    print("\nTesting get_pi_to_5th_digit()...")
    result = pie.get_pi_to_5th_digit()
    print(f"  Result: {result}")
    
    # Round to 5 decimal places
    rounded_result = round(result, 5)
    expected_rounded = 3.14159
    
    print(f"  Rounded to 5 decimals: {rounded_result}")
    print(f"  Expected:              {expected_rounded}")
    
    # Check that when rounded to 5 decimal places, it matches
    assert rounded_result == expected_rounded, \
        f"Result {rounded_result} doesn't match expected {expected_rounded}"
    print("  ✓ Test passed!")
    return True


def test_accuracy_comparison():
    """Compare the accuracy of different methods."""
    print("\nComparing accuracy of methods...")
    
    leibniz_result = pie.calculate_pi(precision=5)
    machin_result = pie.calculate_pi_machin(precision=5)
    actual_pi = math.pi
    
    print(f"  Leibniz formula:  {leibniz_result}")
    print(f"  Machin formula:   {machin_result}")
    print(f"  Python math.pi:   {actual_pi}")
    print(f"  Leibniz error:    {abs(leibniz_result - actual_pi)}")
    print(f"  Machin error:     {abs(machin_result - actual_pi)}")
    
    # Machin should be more accurate
    assert abs(machin_result - actual_pi) < abs(leibniz_result - actual_pi), \
        "Machin formula should be more accurate than Leibniz"
    print("  ✓ Machin formula is more accurate!")
    return True


def test_first_five_digits():
    """Test that the first 5 decimal digits are correct."""
    print("\nTesting first 5 decimal digits...")
    result = pie.get_pi_to_5th_digit()
    
    # Extract first 5 decimal digits
    result_str = f"{result:.10f}"
    print(f"  Full result: {result_str}")
    
    # Get the digits after decimal point
    decimal_part = result_str.split('.')[1][:5]
    expected_digits = "14159"
    
    print(f"  First 5 decimal digits: {decimal_part}")
    print(f"  Expected:               {expected_digits}")
    
    assert decimal_part == expected_digits, \
        f"First 5 digits {decimal_part} don't match expected {expected_digits}"
    print("  ✓ Test passed!")
    return True


def run_all_tests():
    """Run all test functions."""
    print("=" * 60)
    print("Running all tests for pie.py")
    print("=" * 60)
    
    tests = [
        test_calculate_pi,
        test_calculate_pi_machin,
        test_get_pi_to_5th_digit,
        test_accuracy_comparison,
        test_first_five_digits
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ Test error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
