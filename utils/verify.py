import os
import re
import subprocess

from utils.data_handler import update_test_file, delete_test, read_java_file, delete_java_file

SUCCESS = '\033[92m'
FAIL = '\033[91m'
BLUE = '\033[94m'
UNDERLINE = '\033[1;4m'
BOLD = '\033[1m'
RESET = '\033[0m'

PROMPT_WITH_ERROR = (
    "Please fix {}."
    "\n\nJava"
    "Class:\n\n###{"
    "}###\n\nUnit test:\n\n###{"
    "}###\n\nError:\n\n###{}###")


def extract_tests(test_class):
    test_pattern = re.compile(r'@Test\s*[\w\s]*\s*(test\w*)\s*\(')
    tests = test_pattern.findall(test_class)
    return tests


def check_test_annotation(test_class, file_path):
    pattern = re.compile(r'@Test')
    match = pattern.search(test_class)
    if match:
        return True
    else:
        print(f"\n{RESET}{FAIL}{os.path.basename(file_path)} will be deleted due to missing compile tests.{RESET}")
        delete_java_file(file_path)
        return False


def verify_tests(java_class, test_class, file_path):
    succ, succ_rev, fail = 0, 0, 0
    tests = extract_tests(test_class)
    print(f"{RESET}{BOLD}\n\n\nGenerated {os.path.basename(file_path)} with {len(tests)} Tests\n{RESET}")
    print(f"{RESET}{UNDERLINE}Check test compilation:\n{RESET}")

    for i in range(len(tests)):
        success, success_rev, failed = verify_test(i, tests, read_java_file(file_path), java_class, file_path,
                                                   attempt=1)
        succ += success
        succ_rev += success_rev
        fail += failed

        if i == len(tests) - 1:
            print(read_java_file(file_path))
            check_test_annotation(read_java_file(file_path), file_path)

    return succ, succ_rev, fail


def verify_test(i, tests, test_class, java_class, file_path, attempt):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    success, err, succ, succ_rev, fail = run_maven_test(i, tests, file_name, attempt)

    if not success:
        if attempt > 1:
            print(f"    {FAIL}FAILED{RESET}")
        else:
            print(f"{RESET}{FAIL}{tests[i]}\t\t\t{i + 1}/{len(tests)} FAILED{RESET}")
        succ, succ_rev, fail = handle_error(err, tests, test_class, i, java_class, file_path, attempt,
                                            succ,
                                            succ_rev)

    return succ, succ_rev, fail


def run_maven_test(i, tests, file_name, attempt):
    try:
        print("mvn", "-Dtest=" + file_name + "#" + tests[i], "test-compile")
        result = subprocess.run(
            ["mvn", "-Dtest=" + file_name + "#" + tests[i], "test-compile"],
            capture_output=True, text=True)
        if result.returncode == 0:
            if attempt == 1:
                print(f"{RESET}{SUCCESS}{tests[i]}\t\t\t{i + 1}/{len(tests)}{RESET}")
                return True, None, 1, 0, 0
            else:
                print(f"{RESET}{SUCCESS}{tests[i]}\t\t\t{i + 1}/{len(tests)}{RESET}")
                return True, None, 0, 1, 0
        else:
            err = result.stdout.strip()
            return False, err, 0, 0, 0
    except Exception as e:
        print("Error in run_maven_test: ", e)


def handle_error(err, tests, test_class, i, java_class, file_path, attempt, succ, succ_rev):
    from utils.llm import prompt_openai_corr

    if attempt > 2:
        print(f"    {RESET}{FAIL}{tests[i]} not compilable and will be deleted.{RESET}")
        delete_test(file_path, tests[i])
        return 0, 0, 1

    print(f"    {RESET}{BLUE}TEST REVISION {attempt}/2{RESET}")
    prompt_with_error = PROMPT_WITH_ERROR.format(tests[i], tests[i], java_class, read_java_file(file_path), err)
    corrected_test_class = prompt_openai_corr(prompt_with_error)

    update_test_file(file_path, corrected_test_class)
    print(f"    {RESET}{BLUE}Generated new {tests[i]}{RESET}")
    return verify_test(i, tests, corrected_test_class, java_class, file_path, attempt + 1)
