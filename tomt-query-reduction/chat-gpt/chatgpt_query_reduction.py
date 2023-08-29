import json

def normalize_query(query):
    query = query.strip().lower()
    from jnius import autoclass
    
    tokeniser = autoclass("org.terrier.indexing.tokenisation.Tokeniser").getTokeniser()
    
    return " ".join(tokeniser.getTokens(query))

class ChatGPTQueryReduction():
    def __init__(self, directory_with_predictions, prompt):
        predictions = json.load(open(f'{directory_with_predictions}/query-expansions-from-chatgpt-raw-prompt-0{prompt}.json', 'r'))
        self.predictions = {}
        for k, v in predictions.items():
            self.predictions[normalize_query(k)] = v

    def reduce_query(self, query):
        query = normalize_query(query if type(query) == str else query['query'])
        query = self.predictions[query]['gpt-3.5-turbo-response']['choices'][0]['message']['content']

        return normalize_query(query)

    def as_transformer(self):
        import pyterrier
        return pyterrier.apply.query(lambda i: self.reduce_query(i))