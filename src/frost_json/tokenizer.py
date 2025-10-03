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
                if current_opening_char and current_opening_char[-1] == "," and current_aggregated_string != '':
                    current_opening_char.pop()
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
  "company": {
    "name": "TechNova Solutions",
    "founded": 2005,
    "employees": [
      {
        "id": 101,
        "name": "Alice Johnson",
        "department": "Engineering",
        "skills": ["Python", "C++", "Machine Learning"],
        "full_time": true,
        "manager_id": null
      },
      {
        "id": 102,
        "name": "Bob Smith",
        "department": "Product",
        "skills": ["UX Design", "Prototyping", "Figma"],
        "full_time": true,
        "manager_id": 101
      },
      {
        "id": 103,
        "name": "Charlie Lee",
        "department": "Marketing",
        "skills": ["SEO", "Content Writing"],
        "full_time": false,
        "manager_id": 102
      }
    ],
    "locations": {
      "headquarters": {
        "city": "San Francisco",
        "state": "CA",
        "country": "USA",
        "address": {
          "street": "123 Market St",
          "zip": "94103"
        }
      },
      "branch_offices": [
        {
          "city": "New York",
          "state": "NY",
          "country": "USA"
        },
        {
          "city": "London",
          "state": null,
          "country": "UK"
        },
        {
          "city": "Bangalore",
          "state": "KA",
          "country": "India"
        }
      ]
    },
    "products": [
      {
        "name": "NovaAI",
        "category": "Software",
        "versions": [1.0, 1.1, 2.0],
        "release_dates": ["2020-01-15", "2020-06-30", "2021-02-10"]
      },
      {
        "name": "NovaCloud",
        "category": "Cloud Services",
        "versions": [1, 2],
        "release_dates": ["2019-05-20", "2020-11-11"]
      }
    ],
    "is_public": false,
    "revenue_million_usd": 125.75
  },
  "partners": [
    {
      "name": "Globex Corp",
      "industry": "Tech",
      "contract_signed": true,
      "contract_value_million_usd": 20.5
    },
    {
      "name": "Innotech",
      "industry": "Consulting",
      "contract_signed": false,
      "contract_value_million_usd": null
    }
  ],
  "misc": {
    "notes": "This is a large sample JSON for testing purposes.",
    "tags": ["test", "json", "tokenizer", "parser"]
  }
}

    '''

    tkniz = Tokenizer(my_json)
    tkniz.build_token_stream()
    for i in tkniz.token_stream.tokens:
        print(i)

    