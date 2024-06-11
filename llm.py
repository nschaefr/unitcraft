import logging
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

from utils.constants import system_text, prompt_templates
from utils.data_handler import find_java_files, create_test_file, read_java_file
from utils.java_class_extractor import JavaClassExtractor
from utils.test_validator import validate_test

load_dotenv()
key = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key=key)

logger = logging.getLogger()


class TestStats:

    def __init__(
        self,
        total_tests=0,
        succ_tests=0,
        succ_classes=0,
        succ_rev_classes=0,
        fail_classes=0,
    ):
        self.total_tests = total_tests
        self.succ_tests = succ_tests
        self.succ_classes = succ_classes
        self.succ_rev_classes = succ_rev_classes
        self.fail_classes = fail_classes


def prompt_openai(prompt, model, system):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": [{"type": "text", "text": system}]},
                {"role": "user", "content": [{"type": "text", "text": prompt}]},
            ],
            temperature=0.1,
            max_tokens=4096,
        )
        test_code = response.choices[0].message.content
        return remove_format(test_code)
    except Exception as e:
        logger.error(f"Error while generating test code: {e}")
        return None


def generate_test_code(java_file, java_class, stats, model, prompt_type):
    extractor = JavaClassExtractor(java_class)

    package = extractor.get_package()
    imports = extractor.get_imports()
    class_name = extractor.get_class_name()
    constructor = extractor.get_constructor()
    methods = extractor.get_methods()

    for method in methods:
        method_name = re.search(r"([a-zA-Z0-9_]+)\s*\(", method).group(1)
        capitalized_method_name = method_name[0].upper() + method_name[1:]

        # Create the test file name
        test_file_name = f"{class_name}{capitalized_method_name}Test.java"
        test_class_name = f"{class_name}{capitalized_method_name}Test"

        print(class_name, method_name)

        prompt = prompt_templates[prompt_type].format(
            method_name,
            package,
            ", ".join(imports),
            class_name,
            constructor,
            method,
            test_class_name,
        )

        # Generate test code using the prompt
        test_code = prompt_openai(prompt, model, system_text)

        # Write the test code to the file
        test_path = create_test_file(java_file, test_file_name, test_code)

        # Verify the test
        stats = validate_test(test_code, test_path, stats, model)

    return stats


def remove_format(test_code):
    pattern = r"```java(.*?)```"
    match = re.search(pattern, test_code, re.DOTALL)
    if match:
        return match.group(1).strip()
    return test_code.strip()


def generate_unit_tests(prompt_type, model):
    java_files = find_java_files()
    stats = TestStats()

    if java_files:
        for java_file in java_files:
            java_class = read_java_file(java_file)
            stats = generate_test_code(java_file, java_class, stats, model, prompt_type)
    else:
        logger.warning("No java files found.")

    print(
        f"\n\nSTATISTICS:\n\n"
        f"TEST CLASSES GENERATED: {stats.succ_classes + stats.succ_rev_classes + stats.fail_classes}\n"
        f"SUCCESSFUL COMPILATIONS: {stats.succ_classes + stats.succ_rev_classes}\n"
        f"\t-- FIRST TIME: {stats.succ_classes}\n"
        f"\t-- AFTER REVISION: {stats.succ_rev_classes}\n"
        f"FAILED: {stats.fail_classes}\n\n"
        f"TESTS GENERATED: {stats.total_tests}\n"
        f"COMPILABLE TESTS: {stats.succ_tests}\n"
        f"DELETED TESTS: {stats.total_tests - stats.succ_tests}\n"
    )
