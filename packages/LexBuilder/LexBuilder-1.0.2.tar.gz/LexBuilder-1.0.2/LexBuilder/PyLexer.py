from .BaseLexer import types, lexer


class Token:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class PyBuilder:
    def __init__(self, tokens):
        self.tokens = tokens

    def generate_code_for_tokens(self):
        result1 = ""
        result2 = ""
        result3 = ""

        for token in self.tokens:
            name = token.name
            value = token.value
            result1 += f'{name} = "{name}"\n'
            if len(set(value)) == 1:
                result1 += f'{"_".join([name, name])} = "{"_".join([name, name])}"\n'
                result2 += f"             if self.current_char == '{list(set(value))[0]}':\n"
                result2 += '                 self.advance()\n'
                result2 += f"                 if self.current_char == '{list(set(value))[0]}':\n"
                result2 += f'                     self.advance()\n'
                result2 += f'                     return Token({"_".join([name, name])}, "{value*2}")\n'
                result2 += f'                 else:\n'
                result2 += f"                     return Token({name}, '{value}')\n\n"
            else:
                result3 += f'                     if token_value == "{value}":\n'
                result3 += f'                         return Token({name}, "{value}")\n\n'

        return result1, result2, result3


    def build_lexer(self):
        code1, code2, code3 = self.generate_code_for_tokens()
        with open("Lexer.py", "w", encoding="utf-8") as file:
            file.write("import sys\n\n\n")
            file.write(types.format(code1) + "\n\n\n")
            file.write(lexer.substitute(first=code2, second=code3) + "\n\n")

