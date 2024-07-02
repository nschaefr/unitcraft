import re


class JavaClassExtractor:

    def __init__(self, java_class_content):
        self.java_class_content = java_class_content
        self.class_info = self.extract_class_info()

    def extract_class_info(self):
        package_pattern = r"package\s+([a-zA-Z0-9_.]+);"
        imports_pattern = r"import\s+([a-zA-Z0-9_.]+);"
        class_name_pattern = r"\b(class|interface)\s+([a-zA-Z_$][a-zA-Z\d_$]*)"
        method_pattern = (
            r"(public|private|protected|static|final|synchronized|abstract|native|strictfp|transient|volatile|\w+)"
            r"\s+[\w<>,\s]+\s+"
            r"[a-zA-Z_]\w*"
            r"\s*\([^)]*\)"
            r"\s*(?:throws\s+[a-zA-Z0-9_,\s]+)?"
            r"\s*\{"
        )

        package_match = re.search(package_pattern, self.java_class_content)
        package = package_match.group(1) if package_match else None

        imports_matches = re.findall(imports_pattern, self.java_class_content)
        imports = imports_matches if imports_matches else []

        class_name_match = re.search(class_name_pattern, self.java_class_content)
        class_name = class_name_match.group(2) if class_name_match else None

        constructor_pattern = (
            r"public\s+" + re.escape(class_name) + r"\s*\(([^)]*)\)\s*\{" r"(.*?)}"
        )
        constructor_match = re.search(
            constructor_pattern, self.java_class_content, re.DOTALL
        )
        constructor = constructor_match.group(0).strip() if constructor_match else None

        methods = self.extract_methods_with_content(method_pattern)

        return {
            "package": package,
            "imports": imports,
            "class_name": class_name,
            "constructor": constructor,
            "methods": methods,
        }

    def extract_methods_with_content(self, method_pattern):
        method_starts = [
            m.start() for m in re.finditer(method_pattern, self.java_class_content)
        ]
        methods = []
        for start in method_starts:
            method_content = self.extract_full_method(start)
            methods.append(method_content)
        return methods

    def extract_full_method(self, start_index):
        stack = []
        index = start_index
        while index < len(self.java_class_content):
            if self.java_class_content[index] == "{":
                stack.append("{")
            elif self.java_class_content[index] == "}":
                stack.pop()
                if not stack:
                    return self.java_class_content[start_index : index + 1]
            index += 1
        return None

    def get_package(self):
        return self.class_info["package"]

    def get_imports(self):
        return self.class_info["imports"]

    def get_class_name(self):
        return self.class_info["class_name"]

    def get_constructor(self):
        return self.class_info["constructor"]

    def get_methods(self):
        return self.class_info["methods"]
