ZERO_SHOT_PROMPT = "Java Class:\n\n###{}###\n\nUnit tests:\n"
ONE_SHOT_PROMPT = "Java Class:\n\n###{}###\n\nUnit tests:\n"

prompt_templates = {
    "ZERO_SHOT": ZERO_SHOT_PROMPT,
    "ONE_SHOT": ONE_SHOT_PROMPT
}

system_text = ("You will be provided with a java class and your task is to create a test class with unit tests that "
               "are testing the functionality using JUnit5. Your goal is maximum test "
               "coverage. You are not allowed to write comments in the code. Return the full code only.")

system_text_corr = ("You will be provided with a java class, a test class and an error and your task is to repair the "
                    "unit tests that are causing the error. You are not allowed to write comments. Return the full "
                    "code only. Use Reflection for private access errors and check for missing imports or packages.")

PROMPT_ERROR = (
    "\n\nJava Class:\n\n###{"
    "}###\n\nUnit test:\n\n###{"
    "}###\n\nError:\n\n###{}###")

PROMPT_DEL = (
    "Delete the tests that causing the error."
    "a\n\nJava Class:\n\n###{"
    "}###\n\nUnit test:\n\n###{"
    "}###\n\nError:\n\n###{}###")
