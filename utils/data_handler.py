import os
import re

working_dir = os.getcwd()

RESET = '\033[0m'
BLUE = '\033[94m'


def find_java_files():
    java_files = []
    main_java_dir = os.path.join(working_dir, "src", "main")
    for root, dirs, files in os.walk(main_java_dir):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    return java_files


def read_java_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def create_test_file(file_path, response):
    os.makedirs(os.path.join(working_dir, "src", "test"), exist_ok=True)
    test_file_dir = os.path.join(working_dir, "src", "test")
    relative_path = os.path.relpath(os.path.dirname(file_path), os.path.join(working_dir, "src", "main"))
    relative_path = relative_path.replace("..", "").lstrip(os.sep)
    target_dir = os.path.join(test_file_dir, relative_path)
    os.makedirs(target_dir, exist_ok=True)
    test_file = os.path.splitext(os.path.basename(file_path))[0] + "Test.java"
    test_file_path = os.path.join(target_dir, test_file)
    with open(test_file_path, 'w') as file:
        file.write(response)
    return test_file_path


def update_test_file(file_path, corrected_test_code):
    with open(file_path, 'w') as file:
        file.write(corrected_test_code)


def delete_test(file_path, test):
    with open(file_path, 'r') as file:
        code = file.read()
    pattern = re.compile(r'@Test\s*.*?(\b' + re.escape(test) + r'\b.*?){.*?}(?=\s*@|$)', re.DOTALL)
    modified_code = pattern.sub('', code)

    with open(file_path, 'w') as file:
        file.write(modified_code)


def delete_java_file(file_path):
    os.remove(file_path)
