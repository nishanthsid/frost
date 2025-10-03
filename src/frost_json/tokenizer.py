from typing import List
from ftoken import Token, TokenType
from token_stream import TokenStream

class Tokenizer:
    
    __OPENING_CHARS = set(
        ["[","{"]
    )
    
    __CLOSING_CHARS = set(
        ["]","}","\"",","]
    )

    __OPEN_CLOSE_CHAR_MAPPING = {
        "]" : "[",
        "}" : "{",
        "\"" : "\""
    }

    def __init__(self, json_string : str):
        self.json_string = json_string
        self.token_stream = TokenStream()
    
    def build_token_stream(self):
        current_opening_char = []

        current_aggregated_string = ''

        for char in self.json_string:

            if current_opening_char != [] and current_opening_char[-1] != "\"" and current_aggregated_string == '' and char == "\"":
                if current_opening_char and current_opening_char[-1] == ",":
                    current_opening_char.pop()
                current_opening_char.append(char)
            elif char in self.__OPENING_CHARS:
                if current_aggregated_string != '':
                    raise SyntaxError("Invalid Literal " + char + ", not allowed here")
                if current_opening_char and current_opening_char[-1] == ",":
                    current_opening_char.pop()
                current_opening_char.append(char)
                self.token_stream.push_token(Token(TokenType(char),char))
            elif char in self.__CLOSING_CHARS or char == ",":
                if not current_opening_char:
                    raise SyntaxError("Invalid Literal " + char + ", not allowed here")
                elif char != ',':
                    if current_opening_char[-1] != self.__OPEN_CLOSE_CHAR_MAPPING[char]:
                        raise SyntaxError("Invalid closing char : " + char + "")
                elif char == ',':
                    if current_opening_char and current_opening_char[-1] == "\"":
                        current_aggregated_string += char
                        continue
                if current_aggregated_string == "true" or current_aggregated_string == "false" or current_aggregated_string == "null":
                    self.token_stream.push_token(Token(TokenType(current_aggregated_string.upper()),current_aggregated_string))
                else:
                    is_num = None
                    try:
                        float(current_aggregated_string)
                        is_num = True
                    except ValueError:
                        is_num = False

                    if is_num:
                        self.token_stream.push_token(Token(TokenType.NUMBER,current_aggregated_string))
                    else:
                        if current_aggregated_string != "":
                            self.token_stream.push_token(Token(TokenType.STRING,current_aggregated_string))
                current_aggregated_string = ""
                if char != "\"":
                    self.token_stream.push_token(Token(TokenType(char),char))
                if char != ",":
                    current_opening_char.pop()
                else:
                    if current_opening_char and current_opening_char[-1] == ",":
                        current_opening_char.pop()
                    current_opening_char.append(",")
            elif char == ":" and current_opening_char[-1] != "\"":
                if current_aggregated_string != '':
                    raise SyntaxError("Invalid Literal " + char + ", not allowed here")
                else:
                    self.token_stream.push_token(Token(TokenType.COLON,char))
            elif char.isspace() and current_aggregated_string == '':
                continue
            else:
                current_aggregated_string += char
        
if __name__ == "__main__":
    my_json = '''
    {
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}

    '''

    tkniz = Tokenizer(my_json)
    tkniz.build_token_stream()
    print("Done Tokenizing")

    