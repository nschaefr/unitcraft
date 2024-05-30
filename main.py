import argparse
import time

from utils.llm import generate_unit_tests


def main():
    parser = argparse.ArgumentParser(description="Generate unit tests using LLM.")
    parser.add_argument("--prompt", default="zero", choices=["zero", "one"],
                        help="Type of prompt to use (zero_shot/one_shot)")
    args = parser.parse_args()
    prompt_type = args.prompt

    start = time.time()
    generate_unit_tests(prompt_type)
    end = time.time()

    total_time_seconds = end - start
    total_minutes = int(total_time_seconds // 60)
    total_seconds = int(total_time_seconds % 60)

    print(f"\nTotal Generation-Time: {total_minutes:02d}:{total_seconds:02d}")


if __name__ == "__main__":
    main()
