from ..frost_json import tokenizer

my_json = '''
{
    "name" : "Nishanth S D",
    "male" : true
}
'''

tkniz = tokenizer.Tokenizer(my_json)
tkniz.build_token_stream()


