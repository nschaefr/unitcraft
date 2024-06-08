ZERO_SHOT_PROMPT = ("Write a Test class with unit tests for the following method: \n\n"
                    "Method: {}\n\n"
                    "Package: {}\n\n"
                    "Imports: {}\n\n"
                    "Class_Name: {}\n\n"
                    "Constructor: {}\n\n"
                    "Code_of_method: {}\n\n"
                    "Name_of_Test_Class: {}"
                    )
ONE_SHOT_PROMPT = "Java Class:\n\n###{}###\n\nUnit tests:\n"

prompt_templates = {
    "ZERO_SHOT": ZERO_SHOT_PROMPT,
    "ONE_SHOT": ONE_SHOT_PROMPT
}

system_text = (
    "You are an excellent Java programmer. Create a test class with unit tests using JUnit5 for the provided method. "
    "Use Reflection for private access and Mockito if it is necessary. Aim for high line-, "
    "branch- and method coverage. Return code only.")

system_text_repair = (
    "You are an excellent Java programmer who repairs compilation and build errors in Java code. Use Reflection for "
    "private access errors and check for missing imports or packages."
    "Fix the error and write the correct code. Always provide the entire class including package and imports. Return "
    "code only.")

system_text_delete = (
    "You are an excellent Java programmer. Delete all methods that causing errors. Return code only.")

PROMPT_REPAIR = ("Please fix the following error: \n\n {} \n\n"
                 "The error occurs when executing this class: \n\n ```java{}``` \n\n")

PROMPT_DEL = (
    "Delete the full test that causes the following error: \n\n {} \n\n"
    "The error occurs when executing this class: \n\n ```java{}``` \n\n")
