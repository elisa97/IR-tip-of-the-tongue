# From https://github.com/grill-lab/trec-cast-tools/blob/master/src/main/python/passage_chunker.py
from tqdm import tqdm
import json
import argparse
import re
import spacy
nlp = spacy.load("en_core_web_sm", exclude=["parser", "tagger", "ner", "attribute_ruler", "lemmatizer", "tok2vec"]) #->senter
nlp.enable_pipe("senter")
print(nlp.pipe_names)


class SpacyPassageChunker:
    def __init__(self):
        self.document = None
        self.sentences = None

    
    def sentence_tokenization(self, document):
        self.document = parse_doc(document)
        self.sentences = list(self.document.sents)

    
    def create_passages(self, passage_size = 250):

        passages = []
        content_length = len(self.sentences)
        sentences_word_count = [len([token for token in sentence]) for sentence in self.sentences]
        
        current_idx = 0
        current_passage_word_count = 0
        current_passage = ''
        sub_id = 0
        
        for i in range(content_length):
            if current_passage_word_count >= (passage_size * 0.67):
                passages.append({
                    "body": current_passage,
                    "id": sub_id
                })
                current_passage = ''
                current_passage_word_count = 0
                
                current_idx = i
                sub_id += 1
            
            current_passage += self.sentences[i].text + ' '
            current_passage_word_count += sentences_word_count[i]

        
        current_passage = ' '.join(sentence.text for sentence in self.sentences[current_idx:])
        passages.append({
            "body": current_passage,
            "id": sub_id
        })
        
        return passages
        
        
def parse_doc(document):
    return nlp(sanitize_document(document))

def sanitize_document(doc):
    sanitized = re.compile('<.*?>')
    return re.sub(sanitized, '', doc)[:999999]

def tokens(doc):
    return set([i for i in parse_doc(doc) if not i.is_punct])


def passages(document_text,passage_len=300):
    tmp = SpacyPassageChunker()
    tmp.sentence_tokenization(document_text)

    ret = [i['body'] for i in tmp.create_passages(passage_len)]

    return [(i[0] +1, i[1]) for i in enumerate(ret)]

def passage_calculate_doc_term_recall(lines, args):
    import json
    from get_training_query_term_recall import calculate_doc_term_recall

    for line in lines:
        json_dict = json.loads(line)
        for passage in passages(json_dict['doc']['title']):
            i = {k:v for k,v in json_dict.items()}
            i['doc'] = {'title': passage[1]}
            for k in calculate_doc_term_recall([json.dumps(i)], args):
                yield k

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_in_file", help="Each line: {\"queries\": [\"what kind of animals are in grasslands\", \"tropical grasslands animals\", ...], \"doc\":{\"title\": Tropical grassland animals (which do not all occur in the same area) include giraffes, zebras, buffaloes, ka...}}")
    parser.add_argument("json_out_file", help="just the outfile")
    parser.add_argument("--stem", action="store_true", help="recommend: true")
    parser.add_argument("--stop", action="store_true", help="recommend: true")
    args = parser.parse_args()
    with open(args.json_in_file,'r') as infile, open(args.json_out_file,'w') as outfile:
        for passage in tqdm(passage_calculate_doc_term_recall(infile,args)):
            outfile.write(json.dumps(passage) + "\n")
