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


class TestConfiguration:
    def __init__(self, temperature=0, prompt_type="default"):
        self.temperature = temperature
        self.prompt_type = prompt_type


def prompt_openai(prompt, temperature, system):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": [{"type": "text", "text": system}]},
                {"role": "user", "content": [{"type": "text", "text": prompt}]},
            ],
            temperature=temperature,
            max_tokens=4096,
        )
        test_code = response.choices[0].message.content
        return remove_format(test_code)
    except Exception as e:
        logger.error(f"Error while generating test code: {e}")
        return None


def generate_test_code(java_file, java_class, config):
    extractor = JavaClassExtractor(java_class)

    package = extractor.get_package()
    imports = extractor.get_imports()
    class_name = extractor.get_class_name()
    constructor = extractor.get_constructor()
    methods = extractor.get_methods()

    for method in methods:
        method_name = re.search(r"([a-zA-Z0-9_]+)\s*\(", method).group(1)
        capitalized_method_name = method_name[0].upper() + method_name[1:]
        test_file_name = f"{class_name}{capitalized_method_name}Test.java"
        test_class_name = f"{class_name}{capitalized_method_name}Test"

        prompt = prompt_templates[config.prompt_type].format(
            method_name,
            package,
            ", ".join(imports),
            class_name,
            constructor,
            method,
            test_class_name,
        )

        test_code = prompt_openai(prompt, config.temperature, system_text)

        test_path = create_test_file(java_file, test_file_name, test_code)

        validate_test(test_code, test_path, config.temperature)


def remove_format(test_code):
    pattern = r"```java(.*?)```"
    match = re.search(pattern, test_code, re.DOTALL)
    if match:
        return match.group(1).strip()
    return test_code.strip()


def generate_unit_tests(prompt_type, temperature):
    java_files = find_java_files()
    config = TestConfiguration()
    config.temperature = temperature
    config.prompt_type = prompt_type

    if java_files:
        for java_file in java_files:
            java_class = read_java_file(java_file)
            generate_test_code(java_file, java_class, config)
    else:
        logger.warning("No java files found.")
