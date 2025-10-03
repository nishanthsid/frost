from tokenizer import Tokenizer

class FrostJsonParser:
    def __init__(self,json_text : str):
        self.json_text = json_text
        self.token_stream = Tokenizer(json_text)
        self.token_stream.build_token_stream()

