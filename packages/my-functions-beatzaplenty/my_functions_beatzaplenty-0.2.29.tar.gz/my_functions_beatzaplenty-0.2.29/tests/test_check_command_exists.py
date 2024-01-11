import pytest
import my_functions_beatzaplenty.general_purpose as general_purpose

def test_check_command_exists():
    # Test for an existing command (you can replace 'ls' with any valid command on your system)
    assert general_purpose.check_command_exists('ls') is True

    # Test for a non-existing command
    assert general_purpose.check_command_exists('nonexistentcommand123') is False

    # Test for a command that raises FileNotFoundError
    assert general_purpose.check_command_exists('this_command_does_not_exist') is False

    # Test for a command that raises subprocess.CalledProcessError
    assert general_purpose.check_command_exists('ls /nonexistentdirectory') is False

    # You can add more test cases as needed

if __name__ == '__main__':
    pytest.main()
