# Unitcraft  

Unitcraft is a Python command-line tool developed as part of my bachelor's thesis on:  

**Can language models take over the work of software testers?  
Automated JUnit test generation using Large Language Models**  

It is designed for the automatic generation of JUnit5 tests in Java-Maven projects. Since the focus is on measuring the quality of the *GPT-4o* language model, the generated test code is accepted as-is without manual intervention or additional refinement features.  

## Features  
* User prompts to initialize prompt and temperature variables  
* Automatic detection of all Java classes  
* Creation of a prompt  
* Test code generation via API request to communicate with the LLM  
* Verification of the test class's compilability  
* Repair rounds for error correction or removal of relevant code sections/test classes  
* Writing the test class to a Java file and placing it in the test directory with the correct path  

## Project Structure  
The project should follow this structure and include an empty *test* folder:  

```
project
└── src
    ├── main
    │   ├── java
    │   └── resources
    └── test
```
  
Additionally, a `.env` file must be created, where the OpenAI API key is stored as a string in a variable named `OPEN_API_KEY`.  

## Execution  
The tool is launched from the project's *root* directory using the following command:  

```bash
python3 path/to/main.py
```
