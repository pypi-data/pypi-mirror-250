# About LexBuilder:
LexBuilder is a library for automatically building a lexer in Python. In the future, the library will be able to build lexers in major programming languages such as C++, Golang, Java/Kotlin, etc.

## About Syntax:
In order for the library to generate the Lexer.py file, you need to pass a list of tokens to the PyBuilder class.
To declare a token, you need to import the Token() class from the PyLexer() class. You need to pass the token name and its value to the Token() class. After that, add all the tokens we created to the list and pass it as an argument to the PyBuilder() class:
```python
from LexBuilder.PyLexer import Token

DIVIDE = Token("DIVIDE", "/")
PRINT = Token("PRINT", "print")
INPUT = Token("INPUT", "input")

tokens = [DIVIDE, PRINT, INPUT]
```
## Example:
```python
from LexBuilder.PyLexer import PyBuilder, Token


DIVIDE = Token("DIVIDE", "/")
PRINT = Token("PRINT", "print")
INPUT = Token("INPUT", "input")

tokens = [DIVIDE, PRINT, INPUT]

lexer = PyBuilder(tokens)
lexer.build_lexer()
```
