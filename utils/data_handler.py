import logging
import os

logger = logging.getLogger(__name__)

working_dir = os.getcwd()


def find_java_files():
    java_files = []
    main_java_dir = os.path.join(working_dir, "src", "main")
    for root, dirs, files in os.walk(main_java_dir):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    return java_files


def read_java_file(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error while reading file: {e}")
        return None


def create_test_file(file_path, file_name, response):
    try:
        os.makedirs(os.path.join(working_dir, "src", "test"), exist_ok=True)
        test_file_dir = os.path.join(working_dir, "src", "test")
        relative_path = os.path.relpath(
            os.path.dirname(file_path), os.path.join(working_dir, "src", "main")
        )
        relative_path = relative_path.replace("..", "").lstrip(os.sep)
        target_dir = os.path.join(test_file_dir, relative_path)
        os.makedirs(target_dir, exist_ok=True)
        test_file_path = os.path.join(target_dir, file_name)
        with open(test_file_path, "w") as file:
            file.write(response)
        return test_file_path
    except Exception as e:
        logger.error(f"Error while creating test file: {e}")
        return None


def update_test_file(file_path, corrected_test_code):
    try:
        with open(file_path, "w") as file:
            file.write(corrected_test_code)
    except Exception as e:
        logger.error(f"Error while updating test file: {e}")


def delete_java_file(file_path):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except Exception as e:
        logger.error(f"Error while deleting file: {e}")
