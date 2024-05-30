import os

from dotenv import load_dotenv
from openai import OpenAI

from utils.data_handler import find_java_files, create_test_file, read_java_file
from utils.verify import verify_tests

load_dotenv()
key = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key=key)

SUCCESS = '\033[92m'
FAIL = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
UNDERLINE = '\033[1;4m'

ZERO_SHOT_PROMPT = "Java Class:\n\n###{}###\n\nUnit tests:\n"
ONE_SHOT_PROMPT = "Java Class:\n\n###{}###\n\nUnit tests:\n"

prompt_templates = {
    "zero": ZERO_SHOT_PROMPT,
    "one": ONE_SHOT_PROMPT
}


def generate_test_code(prompt, java_file, java_class):
    test_class = prompt_openai(prompt)
    test_path = create_test_file(java_file, test_class)
    return verify_tests(java_class, test_class, test_path)


def remove_format_code_block(code):
    if code.startswith("```java") and code.endswith("```"):
        return "\n".join(code.split("\n")[1:-1])
    if code.startswith("###") and code.endswith("###"):
        return "\n".join(code.split("\n")[1:-1])
    return code


def prompt_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You will be provided with a java class and your task is to create a test class with "
                                "unit tests that are testing the functionality using JUnit5. Your goal is maximum "
                                "test coverage. You are not allowed to write comments. Return the full code only."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        temperature=0,
        max_tokens=2000
    )
    test_code = response.choices[0].message.content
    return remove_format_code_block(test_code)


def prompt_openai_corr(prompt_corr):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You will be provided with a java class, a test class and an error and your task is "
                                "to repair a given unit test using JUnit5. Your goal is to fix the error caused by "
                                "the test. You are not allowed to write comments."
                                "You are not allowed to add or delete other tests than the given one. Return the full "
                                "code only. Use Reflection for private access errors and check for missing imports or "
                                "packages."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_corr
                    }
                ]
            }
        ],
        temperature=0.3,
        max_tokens=2000
    )
    test_code = response.choices[0].message.content
    return remove_format_code_block(test_code)


def generate_unit_tests(prompt_type):
    java_files = find_java_files()
    prompt_template = prompt_templates.get(prompt_type)
    succ, succ_rev, fail, = 0, 0, 0

    if java_files:
        for java_file in java_files:
            java_class = read_java_file(java_file)
            prompt = prompt_template.format(java_class)
            success, successful_rev, failed = generate_test_code(prompt, java_file,
                                                                 java_class)
            succ += success
            succ_rev += successful_rev
            fail += failed
    else:
        print("No java files found.")

    print(f"\n\n{RESET}{UNDERLINE}STATISTICS:\n{RESET}")
    print(f"{RESET}TOTAL TESTS GENERATED: {succ + succ_rev + fail}{RESET}")
    print(
        f"{RESET}{SUCCESS}SUCCESSFUL COMPILATIONS: {succ + succ_rev}\n\t-- FIRST TIME: "
        f"{succ}\n{RESET}\t-- AFTER "
        f"REVISION: {succ_rev}\n{RESET}{FAIL}FAILED: {fail}{RESET}")
