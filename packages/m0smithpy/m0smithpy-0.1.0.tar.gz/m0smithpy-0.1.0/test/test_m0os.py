import json
import os

import pytest

import m0smithpy.m0os as m0os
from m0smithpy.m0os import makedirsto, spit_json


# Test 1: Opening a file in an existing path
def test_open_existing_path():
    # Ensure the path exists
    os.makedirs('test_dir', exist_ok=True)
    with m0os.m0open('test_dir/test_file.txt', 'w') as f:
        f.write("Hello World")
    assert os.path.exists('test_dir/test_file.txt')

# Test 2: Opening a file where the path needs to be created
def test_open_non_existing_path():
    if os.path.exists('new_test_dir'):
        os.rmdir('new_test_dir')
    with m0os.m0open('new_test_dir/test_file.txt', 'w') as f:
        f.write("Hello World")
    assert os.path.exists('new_test_dir/test_file.txt')

# Test 3: Handling errors (e.g., invalid mode)
def test_open_with_invalid_mode():
    with pytest.raises(ValueError):
        with m0os.m0open('test_dir/test_file.txt', 'invalid_mode') as f:
            f.write("Hello World")

# Clean up test files and directories after tests
def teardown_module(module):
    os.path.isfile('test_dir/test_file.txt') and os.remove('test_dir/test_file.txt')
    os.rmdir('test_dir')
    os.path.isfile('new_test_dir/test_file.txt') and os.remove('new_test_dir/test_file.txt')
    os.rmdir('new_test_dir')

# Fixture to create and clean up a directory
@pytest.fixture
def test_directory():
    test_dir = 'test_dir'
    yield test_dir  # This is where the test runs
    # Teardown code after yield
    if os.path.exists(test_dir):
        os.rmdir(test_dir)

# Test 1: Successfully creating a new directory
def test_create_new_directory(test_directory):
    test_file_path = f'{test_directory}/test_file.txt'
    makedirsto(test_file_path)
    assert os.path.exists(test_directory)

# Test 2: Directory already exists, exist_ok=True
def test_existing_directory_exist_ok_true(test_directory):
    test_file_path = f'{test_directory}/test_file.txt'
    os.makedirs(test_directory, exist_ok=True)
    makedirsto(test_file_path, exist_ok=True)
    assert os.path.exists(test_directory)

# Test 3: Directory already exists, exist_ok=False
def test_existing_directory_exist_ok_false(test_directory):
    test_file_path = f'{test_directory}/test_file.txt'
    os.makedirs(test_directory, exist_ok=True)
    with pytest.raises(FileExistsError):
        makedirsto(test_file_path, exist_ok=False)

def test_spit_json_new_file(tmp_path):
    """ Test writing JSON data to a new file. """
    file_path = tmp_path / "test.json"
    data = {"key": "value"}

    spit_json(data, str(file_path))
    with open(file_path, "r") as file:
        content = json.load(file)
    assert content == data



def test_spit_json_non_serializable(tmp_path):
    """ Test handling of non-serializable data. """
    file_path = tmp_path / "test.json"
    data = {"key": set([1, 2, 3])}  # Sets are not JSON serializable

    with pytest.raises(TypeError):
        spit_json(data, str(file_path))