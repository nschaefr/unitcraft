import logging
import time

import inquirer

from llm import generate_unit_tests
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def print_welcome_message():
    welcome_message = """
---------------------------------------------------
|                                                 |
|             Welcome to UnitCraft!               |
|             A Unit Test Generator               |
|                                                 |
---------------------------------------------------
|                                                 |
|               Version: 1.0.0                    |
|             Owner: Nils Schäfer                 |
|                                                 |
|         Generate JUnit 5 unit tests             |
|           for Java Maven projects.              |
|                                                 |
---------------------------------------------------
"""
    print(welcome_message)


def main():
    print_welcome_message()
    questions = [
        inquirer.List(
            "model",
            message="Select the model to use",
            choices=["gpt-3.5-turbo-0125", "gpt-4-turbo"],
        ),
        inquirer.List(
            "prompt",
            message="Select the type of prompt to use",
            choices=["ZERO_SHOT", "ONE_SHOT"],
        ),
    ]

    answers = inquirer.prompt(questions)
    prompt_type = answers["prompt"]
    model = answers["model"]

    try:
        start = time.time()
        generate_unit_tests(prompt_type, model)
        end = time.time()

        total_time_seconds = end - start
        total_minutes = int(total_time_seconds // 60)
        total_seconds = int(total_time_seconds % 60)

        print(f"\nTotal Generation-Time: {total_minutes:01d}m {total_seconds:01d}s")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        logger.error(
            "Generation process failed. Please check the logs for more details."
        )


if __name__ == "__main__":
    main()
