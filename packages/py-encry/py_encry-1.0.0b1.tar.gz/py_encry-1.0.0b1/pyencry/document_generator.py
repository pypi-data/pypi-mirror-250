import ast, sys, json

class DocumentGenerator:
    """A class used to parse docstrings from a Python file
    
    Attributes
    ----------
    filename : string - The path to the file to parse
    docstrings : list - A list of docstrings from the file

    Methods
    -------
    extract_docstrings(): Extracts the docstrings from the file
    count_starting_characters(input_string, target_character): Counts the number of starting characters in a string
    parse_docstring(): Parses the docstrings into a JSON object
    """
    def __init__(self, filename):
        self.filename = filename
        self.docstrings = self.extract_docstrings()

    def extract_docstrings(self):
        """Extracts the docstrings from the file

        returns:
        - list - A list of docstrings from the file
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read())
        
        docstrings = []
        inside_class = None

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                if node.body and isinstance(node.body[0], ast.Expr):
                    if str(node.name).startswith("__"):
                        continue
                    docstrings.append((node.name, node.body[0].value.s, type(node).__name__, inside_class))
            if isinstance(node, ast.ClassDef):
                inside_class = node.name
        return docstrings
    
    def count_starting_characters(self, input_string, target_character):
        """Counts the number of starting characters in a string

        arguments:
        - input_string - string - The string to count the characters in
        - target_character - string - The character to count

        returns:
        - int - The number of starting characters in the string
        """
        count = 0
        for char in input_string:
            if char == target_character:
                count += 1
            else:
                break
        return count

    def parse_docstring(self):
        """Parses the docstrings into a JSON object

        returns:
        - list - A list of docstrings from the file
        """

        info = []

        for name, docstring, type, inside_class in self.docstrings:
            content = docstring.split('\n')
            info.append({"type": type, "name": name, "inside_class": inside_class, "type_method" : None, "info": []})
            last_content = {"line": None, "content": None}

            for (idx, line) in enumerate(content):
                line = line.strip()
                if not line.startswith('- ') and (last_content["content"] == "arguments" or last_content["content"] == "returns"):
                    last_content = {"line": None, "content": None}
                if line.startswith('- ') and last_content["content"] == "arguments":
                    if line[2:] == "no-arguments":
                        continue
                    (name, type, text) = line[2:].split(' - ')
                    info[-1]["info"][-1]["data"].append({"name": name, "type": type, "info": text})
                elif line.startswith('- ') and last_content["content"] == "returns":
                    if line[2:] == "no-return":
                        info[-1]["type_method"] = "method"
                        continue
                    (type, text) = line[2:].split(' - ')
                    info[-1]["info"][-1]["data"].append({"type": type, "info": text})
                    if type == info[0]["name"]:
                        info[-1]["type_method"] = "constructor"
                    else:
                        info[-1]["type_method"] = "method"
                elif line.startswith('arguments:'):
                    info[-1]["info"].append({"info": "arguments", "data": []})
                    last_content = {"line": idx, "content": "arguments"}
                elif line.startswith('returns:'):
                    info[-1]["info"].append({"info": "returns", "data": []})
                    last_content = {"line": idx, "content": "returns"}
                elif line.startswith('```') and last_content["content"] == "example":
                    code = content[last_content["line"] + 1 :idx]
                    base_indent = self.count_starting_characters(code[0], ' ')
                    code = [line[base_indent:] for line in code]
                    info[-1]["info"][-1]["data"]["code"] = "\n".join(code)
                    last_content = {"line": None, "content": None}
                elif line.startswith('```'):
                    lang = line[3:]
                    if lang.isspace() or not lang:
                        lang = "python"
                    info[-1]["info"].append({"info": "example", "data": {"lang": lang, "code": None}})
                    last_content = {"line": idx, "content": "example"}
                elif last_content["content"] == "text":
                    info[-1]["info"][-1]["data"]["text"] += "\n" + line
                elif last_content["content"] is None:
                    info[-1]["info"].append({"info": "text", "data": {"text": line}})
                    last_content = {"line": idx, "content": "text"}

        return info

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python document_generator.py <filename>")
        exit(1)
    filename = sys.argv[1]  # Replace with your Python file's path
    docstrings = DocumentGenerator(filename)

    info = docstrings.parse_docstring()
    json_info = json.dumps(info)
    with open('docstrings.json', 'w') as file:
        file.write(json_info)
