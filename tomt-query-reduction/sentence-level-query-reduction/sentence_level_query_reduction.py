class SentenceLevelQueryReduction():
    def __init__(self, model):
        self.model = model
        from spacy.lang.en import English
        self.nlp = English()
        self.nlp.add_pipe("sentencizer")

    def reduce_query(self, query):
        query = query if type(query) == str else query['query']
        ret = []

        for sentence in self.sentences(query):
            if self.model.predict(sentence)[0][0]:
                ret += [sentence]

        return ' '.join(ret)
    
    def sentences(self, text):
        return [str(i) for i in self.nlp(text).sents]

    def as_transformer(self):
        import pyterrier
        return pyterrier.apply.query(lambda i: self.reduce_query(i))


def get_model_by_name(model_name):
    if model_name == 'PredictAlwaysFalse':
        class PredictAlwaysFalse():
            def predict(self, s):
                return [[0]]
        return PredictAlwaysFalse()
    if model_name == 'PredictAlwaysTrue':
        class PredictAlwaysTrue():
            def predict(self, s):
                return [[1]]
        return PredictAlwaysTrue()
    if model_name == 'PredictTrueIfSentenceContainsWorld':
        class PredictTrueIfSentenceContainsWorld():
            def predict(self, s):
                return [[1 if 'World' in s else 0]]
        return PredictTrueIfSentenceContainsWorld()
    
    from simpletransformers.classification import ClassificationModel
    import torch
    use_cuda = torch.cuda.is_available() and torch.cuda.device_count() > 0
    model_name = model_name.split(',')

    return ClassificationModel(
        model_name[0], model_name[1], use_cuda=use_cuda
    )
    
