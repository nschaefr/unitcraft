import logging
import os
import re
import subprocess

from utils.constants import PROMPT_REPAIR, PROMPT_DEL
from utils.constants import system_text_repair
from utils.data_handler import update_test_file, delete_java_file

logger = logging.getLogger()


def extract_tests(test_code):
    test_pattern = re.compile(r"@Test")
    tests = test_pattern.findall(test_code)
    return tests


def run_maven_test(file_name, attempt, stats, tests):
    try:
        result = subprocess.run(
            [
                "mvn",
                "--quiet",
                "-Dtest=" + file_name,
                "-Dmaven.test.failure.ignore=true",
                "test",
            ],
            capture_output=True,
            text=True,
        )
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


def handle_error(err, test_code, test_path, attempt, stats, model):
    from llm import prompt_openai

    if attempt == 1:
        stats.total_tests += len(extract_tests(test_code))

    if attempt > 2:
        if attempt > 3:
            stats.fail_classes += 1
            logger.error("Test class still not compilable and will be deleted.")
            delete_java_file(test_path)
            return stats
        prompt_del = PROMPT_DEL.format(err, test_code)
        logger.error("Deleting tests that causing compilation error...")
        corr_class = prompt_openai(prompt_del, model, system_text_repair)

        if not extract_tests(corr_class):
            delete_java_file(test_path)
            stats.fail_classes += 1
            return stats

        update_test_file(test_path, corr_class)
        return validate_test(corr_class, test_path, stats, model, attempt + 1)

    logger.info(f"REPAIR ROUND {attempt}/3")
    prompt_error = PROMPT_REPAIR.format(err, test_code)
    corr_class = prompt_openai(prompt_error, model, system_text_repair)

    update_test_file(test_path, corr_class)
    return validate_test(corr_class, test_path, stats, model, attempt + 1)


def validate_test(test_code, test_path, stats, model, attempt=1):
    tests = extract_tests(test_code)
    file_name = os.path.basename(test_path)
    logger.info(f"Generated {file_name} with {len(tests)} tests.")
    success, err = run_maven_test(file_name, attempt, stats, tests)
    if not success:
        logger.error("TEST COMPILATION FAILED")
        stats = handle_error(err, test_code, test_path, attempt, stats, model)
    return stats
