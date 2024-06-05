import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

from utils.constants import prompt_templates, system_text, system_text_corr
from utils.data_handler import find_java_files, create_test_file, read_java_file
from utils.test_utils import verify_test

load_dotenv()
key = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key=key)

logger = logging.getLogger()


class TestStats:
    def __init__(self, total_tests=0, succ_tests=0, succ_classes=0, succ_rev_classes=0, fail_classes=0):
        self.total_tests = total_tests
        self.succ_tests = succ_tests
        self.succ_classes = succ_classes
        self.succ_rev_classes = succ_rev_classes
        self.fail_classes = fail_classes


def prompt_openai(prompt, model):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": [{"type": "text", "text": system_text}]},
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            temperature=0.1,
            max_tokens=2500
        )
        test_code = response.choices[0].message.content
        return remove_format(test_code)
    except Exception as e:
        logger.error(f"Error while generating test code: {e}")
        return None


def prompt_openai_corr(prompt_corr, model):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": [{"type": "text", "text": system_text_corr}]},
                {"role": "user", "content": [{"type": "text", "text": prompt_corr}]}
            ],
            temperature=0.1,
            max_tokens=2500
        )
        test_code = response.choices[0].message.content
        return remove_format(test_code)
    except Exception as e:
        logger.error(f"Error while correcting test code: {e}")
        return None


def generate_test_code(prompt, java_file, java_class, stats, model):
    test_code = prompt_openai(prompt, model)
    test_path = create_test_file(java_file, test_code)
    return verify_test(java_class, test_code, test_path, stats, model)


def remove_format(test_code):
    if test_code.startswith("```java") and test_code.endswith("```"):
        return "\n".join(test_code.split("\n")[1:-1])
    if test_code.startswith("###") and test_code.endswith("###"):
        return "\n".join(test_code.split("\n")[1:-1])
    return test_code


def generate_unit_tests(prompt_type, model):
    java_files = find_java_files()
    prompt_template = prompt_templates.get(prompt_type)
    stats = TestStats()

    if java_files:
        for java_file in java_files:
            java_class = read_java_file(java_file)
            prompt = prompt_template.format(java_class)
            stats = generate_test_code(prompt, java_file, java_class, stats, model)
    else:
        logger.warning("No java files found.")

    print(f"\n\nSTATISTICS:\n\n"
          f"TEST CLASSES GENERATED: {stats.succ_classes + stats.succ_rev_classes + stats.fail_classes}\n"
          f"SUCCESSFUL COMPILATIONS: {stats.succ_classes + stats.succ_rev_classes}\n"
          f"\t-- FIRST TIME: {stats.succ_classes}\n"
          f"\t-- AFTER REVISION: {stats.succ_rev_classes}\n"
          f"FAILED: {stats.fail_classes}\n\n"
          f"TESTS GENERATED: {stats.total_tests}\n"
          f"COMPILABLE TESTS: {stats.succ_tests}\n"
          f"DELETED TESTS: {stats.total_tests - stats.succ_tests}\n")
