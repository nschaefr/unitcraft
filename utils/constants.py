test_class_example = """
package com.example.calculator;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class CalculatorTest {{
    private Calculator calculator;

    @BeforeEach
    public void setUp() {{
        calculator = new Calculator("Model X");
    }}

    @Test
    public void testAdd() {{
        assertEquals(5, calculator.add(2, 3), "2 + 3 should equal 5");
        assertEquals(1, calculator.add(-2, 3), "-2 + 3 should equal 1");
        assertEquals(0, calculator.add(0, 0), "0 + 0 should equal 0");
    }}
}}
"""

ZERO_SHOT_PROMPT = (
    "Write a Test class with unit tests for the following method: \n\n"
    "Method: {}\n\n"
    "Package: {}\n\n"
    "Imports: {}\n\n"
    "Class_Name: {}\n\n"
    "Constructor: {}\n\n"
    "Code_of_method: {}\n\n"
    "Name_of_Test_Class: {}\n\n"
    "Test_Class:"
)

ONE_SHOT_PROMPT = (
    "Write a Test class with unit tests for the following method: \n\n"
    "Method: add\n\n"
    "Package: com.example.calculator\n\n"
    "Imports: ['java.util.ArrayList']\n\n"
    "Class_Name: Calculator\n\n"
    "Constructor: public Calculator(String model) {{this.model = model;}}\n\n"
    "Code_of_method: public int add(int a, int b) {{return a + b;}}\n\n"
    "Name_of_Test_Class: CalculatorAddTest\n\n"
    f"Test_Class: {test_class_example}\n\n"
    "Method: {}\n\n"
    "Package: {}\n\n"
    "Imports: {}\n\n"
    "Class_Name: {}\n\n"
    "Constructor: {}\n\n"
    "Code_of_method: {}\n\n"
    "Name_of_Test_Class: {}\n\n"
    "Test_Class:"
)

prompt_templates = {"ZERO_SHOT": ZERO_SHOT_PROMPT, "ONE_SHOT": ONE_SHOT_PROMPT}

system_text = (
    "You are an excellent Java programmer. Create a test class with unit tests using JUnit5 for the provided method. "
    "Use Reflection for private access and Mockito if it is necessary. Aim for high line-, "
    "branch- and method coverage. Return code only without any instructions."
)

system_text_repair = (
    "You are an excellent Java programmer who repairs compilation and build errors in Java code. Use Reflection for "
    "private access errors and check for missing imports or packages."
    "Fix the error and write the correct code. Always provide the entire class including package and imports. Return "
    "code only without any instructions."
)

system_text_delete = (
    "You are an excellent Java programmer. Delete all methods that causing errors. Return code only without any "
    "instructions."
)

PROMPT_REPAIR = (
    "Please fix the following error: \n\n {} \n\n"
    "The error occurs when executing this class: \n\n {} \n\n"
)

PROMPT_DEL = (
    "Delete the full test that causes the following error: \n\n {} \n\n"
    "The error occurs when executing this class: \n\n {} \n\n"
)
