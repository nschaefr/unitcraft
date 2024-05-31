import logging
import os
import re
import subprocess

from utils.constants import PROMPT_ERROR, PROMPT_DEL
from utils.data_handler import update_test_file, delete_java_file

logger = logging.getLogger()


def extract_tests(test_class):
    test_pattern = re.compile(r'@Test')
    tests = test_pattern.findall(test_class)
    return tests


def run_maven_test(file_name, attempt, stats, tests):
    try:
        result = subprocess.run(["mvn", "--quiet", "-Dtest=" + file_name, "test-compile"], capture_output=True,
                                text=True)
        if result.returncode == 0:
            if attempt == 1:
                stats.succ_classes += 1
                stats.total_tests += len(tests)
            else:
                stats.succ_rev_classes += 1
            logger.info("TEST COMPILATION SUCCESSFUL")
            stats.succ_tests += len(tests)
            return True, None
        else:
            err = result.stdout.strip()
            return False, err
    except subprocess.SubprocessError as e:
        logger.error(f"Error in run_maven_test: {e}")
        return False, str(e)


def handle_error(err, test_class, java_class, test_path, attempt, stats, model):
    from utils.llm import prompt_openai_corr

    if attempt == 1:
        stats.total_tests += len(extract_tests(test_class))

    if attempt > 2:
        if attempt > 3:
            stats.fail_classes += 1
            logger.error("Test class still not compilable and will be deleted.")
            delete_java_file(test_path)
            return stats
        prompt_del = PROMPT_DEL.format(java_class, test_class, err)
        logger.error("Deleted tests that causing compilation error.")
        corr_class = prompt_openai_corr(prompt_del, model)
        update_test_file(test_path, corr_class)
        return verify_test(java_class, corr_class, test_path, stats, attempt + 1)

    logger.info(f"TEST REVISION {attempt}/3")
    prompt_error = PROMPT_ERROR.format(java_class, test_class, err)
    corr_class = prompt_openai_corr(prompt_error, model)

    update_test_file(test_path, corr_class)
    return verify_test(java_class, corr_class, test_path, stats, attempt + 1)


def verify_test(java_class, test_class, test_path, stats, model, attempt=1):
    tests = extract_tests(test_class)
    file_name = os.path.basename(test_path)
    logger.info(f"Generated {file_name} with {len(tests)} tests.")
    success, err = run_maven_test(file_name, attempt, stats, tests)
    if not success:
        logger.error("TEST COMPILATION FAILED")
        stats = handle_error(err, test_class, java_class, test_path, attempt, stats, model)
    return stats
