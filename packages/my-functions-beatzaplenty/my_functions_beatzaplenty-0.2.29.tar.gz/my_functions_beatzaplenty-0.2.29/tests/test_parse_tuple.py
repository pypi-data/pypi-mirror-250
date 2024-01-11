import pytest
import my_functions_beatzaplenty.general_purpose as general_purpose

# Write test cases using pytest
def test_parse_tuple():
    # Test case 1: Regular input
    input_1 = "(1, 2, 3)"
    expected_output_1 = ('1', '2', '3')
    assert general_purpose.parse_tuple(input_1) == expected_output_1

    # Test case 2: Input with spaces
    input_2 = "( 4 , 5 , 6 )"
    expected_output_2 = ('4', '5', '6')
    assert general_purpose.parse_tuple(input_2) == expected_output_2

    # Test case 3: Input with leading and trailing spaces
    input_3 = "  7,8,9  "
    expected_output_3 = ('7', '8', '9')
    assert general_purpose.parse_tuple(input_3) == expected_output_3

    # Test case 4: Input with different data types
    input_4 = '(10, hello, True)'
    expected_output_4 = ('10', 'hello', 'True')
    assert general_purpose.parse_tuple(input_4) == expected_output_4

    # Test case 5: Empty input
    input_5 = "()"
    expected_output_5 = ('',)
    assert general_purpose.parse_tuple(input_5) == expected_output_5

# You can add more tests based on the specific scenarios you want to cover.
if __name__ == '__main__':
    pytest.main()
