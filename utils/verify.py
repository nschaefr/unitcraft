import os
import subprocess

from utils.data_handler import update_test_file, delete_java_file

SUCCESS = '\033[92m'
FAIL = '\033[91m'
BOLD = '\033[1m'
BLUE = '\033[94m'
RESET = '\033[0m'

PROMPT_WITH_ERROR = (
    "\n\nJava Class:\n\n###{"
    "}###\n\nUnit test:\n\n###{"
    "}###\n\nError:\n\n###{}###")

PROMPT_WITH_DEL = (
    "Delete the tests that causing the error."
    "a\n\nJava Class:\n\n###{"
    "}###\n\nUnit test:\n\n###{"
    "}###\n\nError:\n\n###{}###"
)


def verify_test(java_class, test_code, test_path, attempt=1, succ=0,
                succ_rev=0, fail=0):
    file_name = os.path.basename(test_path)
    success, err, succ, succ_rev = run_maven_test(file_name, attempt,
                                                  succ,
                                                  succ_rev)
    if not success:
        print(f"{FAIL}{BOLD}TEST COMPILATION FAILED")
        succ, succ_rev, fail = handle_error(err, test_code, java_class, test_path, attempt, succ, succ_rev, fail)

    return succ, succ_rev, fail


def run_maven_test(file_name, attempt, succ, succ_rev):
    try:
        result = subprocess.run(["mvn", "-Dtest=" + file_name, "test-compile"], capture_output=True, text=True)
        if result.returncode == 0:
            if attempt == 1:
                succ += 1
            else:
                succ_rev += 1
            print(f"{SUCCESS}{BOLD}TEST COMPILATION SUCCESSFUL\n{RESET}")
            return True, None, succ, succ_rev
        else:
            err = result.stdout.strip()
            return False, err, succ, succ_rev
    except Exception as e:
        print("Error in run_maven_test: ", e)


def handle_error(err, test_code, java_class, test_path, attempt, succ,
                 succ_rev, fail):
    from utils.llm import prompt_openai_corr

    if attempt > 2:
        if attempt > 3:
            fail += 1
            print(f"{BOLD}Test class not compilable and will be deleted.\n{RESET}")
            delete_java_file(test_path)
            return succ, succ_rev, fail
        prompt_with_del = PROMPT_WITH_DEL.format(java_class, test_code, err)
        corrected_test_code = prompt_openai_corr(prompt_with_del)
        update_test_file(test_path, corrected_test_code)
        return verify_test(java_class, corrected_test_code, test_path, attempt + 1)

    print(f"{RESET}{BLUE}TEST REVISION {attempt}/3")
    prompt_with_error = PROMPT_WITH_ERROR.format(java_class, test_code, err)
    corrected_test_code = prompt_openai_corr(prompt_with_error)

    update_test_file(test_path, corrected_test_code)
    return verify_test(java_class, corrected_test_code, test_path, attempt + 1)
