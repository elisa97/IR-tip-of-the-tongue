from subprocess import check_output
import sys
from tempfile import TemporaryDirectory
from pathlib import Path
import os
from spacy.lang.en import English
import json

# append directory to path so that we can easily execute the deepct script
sys.path.append('/deepct')

def partition_sentences(text, length_target=800):
    global nlp
    if not nlp:
        nlp = English()
        nlp.add_pipe("sentencizer")

    sentences = nlp(text).sents
    ret = ''
    for sentence in sentences:
        ret = (ret + str(sentence)).strip()
        if len(ret) >= length_target:
            yield ret
            ret = ''
    
    if len(ret) > 0:
        yield ret.strip()


def partition_input_data(input_file):
    ret = []
    with open(input_file, 'r') as f:
        for i in f:
            i = json.loads(i)
            qid = str(i['qid'])
            partitions = partition_sentences(i['query'])
            for partition in partitions:
                ret += [(str(int(qid)), ' '.join(partition.split()).strip())]
        return ret


def run_deepct_prediction(model_checkpoint, input_file):
    with TemporaryDirectory() as tmp_dir:
        input_data_partitioned = partition_input_data(input_file)
        output_dir = str((Path(tmp_dir) / 'output').absolute())
        deepct_input_file = str((Path(tmp_dir) / 'input').absolute())
        with open(deepct_input_file, 'w') as f:
            for qid, partition in input_data_partitioned:
                f.write(qid + '\t' + partition + '\n')

        bert_base_dir = os.environ['BERT_BASE_DIR']
        vocab_file = os.path.join(bert_base_dir, 'vocab.txt')
        bert_config_file = os.path.join(bert_base_dir, 'bert_config.json')

        cmd = f'python3 /deepct/run_deepct.py --task_name=marcotsvdoc --do_train=false --do_eval=false --do_predict=true --data_dir={deepct_input_file} ' + \
              f'--max_seq_length=128 --output_dir={output_dir} --vocab_file={vocab_file} --bert_config_file={bert_config_file} ' + \
              f'--init_checkpoint={model_checkpoint}'

        print(check_output(cmd, shell=True).decode('utf-8'))
        ret_raw = parse_deepct_output(open(output_dir + '/test_results.tsv').read().strip())
        ret = {}

        for i in range(len(input_data_partitioned)):
            qid = input_data_partitioned[i][0]
            if qid not in ret:
                ret[qid] = []
            ret[qid] = ret[qid] + ret_raw[i]

        return ret


def determine_per_query_threshold(predictions_for_query, threshold):
    ret = -1000000
    matching_tokens = 0
    scores = sorted([s for t, s in predictions_for_query if len(t) > 1], reverse=True)

    for score in scores:
        print(score)
        if threshold is not None and matching_tokens/len(scores) < threshold:
            print('-->' + str(matching_tokens/len(scores)))
            matching_tokens += 1
            ret = score

    return ret


class DeepCTQueryReduction():
    def __init__(self, deep_ct_predictions, configuration):
        self.model = configuration.split(';')[0]
        self.threshold = float(configuration.split(';')[1]) if configuration.split(';')[1].lower() != 'none' else None
        self.predictions = json.load(open(deep_ct_predictions, 'r'))
    
    def reduce_query(self, query):
        query_id = query if type(query) == str else query['qid']
        predictions_for_query = self.predictions[self.model][query_id]
        threshold_for_query = determine_per_query_threshold(predictions_for_query, self.threshold)
        ret = []

        for token, score in predictions_for_query:
            if len(token) > 1 and (threshold_for_query == None or score >= threshold_for_query):
                ret += [token]

        return ' '.join(ret)



def main(model_checkpoints, input_file, output_file):
    ret = {}

    for model_checkpoint in model_checkpoints:
        ret[model_checkpoint] = run_deepct_prediction(model_checkpoint, input_file)

    with open(output_file, 'w') as f:
        f.write(json.dumps(ret))


def parse_deepct_output_line(line):
    if not line:
        print('asddsaads')
        return []

    ret = []
    line = line.split()
    current_index = 0
    print(line)
    while current_index < len(line):
        token = line[current_index]
        score = float(line[current_index + 1])
        current_index += 2
        if token == '[PAD]' or token == '[SEP]':
            continue        
        
        if token.startswith('##'):
            ret[-1] = (ret[-1][0] + token[2:], max(ret[-1][1], score))
        else:
            ret += [(token, score)]
    return ret


def parse_deepct_output(lines):
    ret = []
    for line in lines.split('\n'):
        
        ret += [parse_deepct_output_line(line)]
    return ret


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Run DeepCT on a set of queries')
    parser.add_argument('--model_checkpoints', type=str, help='The checkpoint of the model to use', nargs='+', default=['/deepct-models/deepct-main-01/output/model.ckpt-0', '/deepct-models/deepct-main-01/output/model.ckpt-20000', '/deepct-models/deepct-main-01/output/model.ckpt-22503', '/deepct-models/deepct-main-02/output/model.ckpt-0', '/deepct-models/deepct-title-01/output/model.ckpt-0', '/deepct-models/deepct-title-01/output/model.ckpt-20000', '/deepct-models/deepct-title-01/output/model.ckpt-21166'])
    parser.add_argument('--input_file', type=str, help='The input file containing the queries')
    parser.add_argument('--output_file', type=str, help='The output file containing the results')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args.model_checkpoints, args.input_file, args.output_file)