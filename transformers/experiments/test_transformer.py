import os
import subprocess
import json
import argparse

def execute_command(command):
    output = subprocess.run(command, shell=True)

def test(config):
    config = json.load(open(args.config))
    c = 'fairseq-generate \
         {} \
        --source-lang {} --target-lang {} \
        --path {} \
        --beam 5 --lenpen 1.2 \
        --gen-subset test \
        --remove-bpe=sentencepiece > {} 2>&1'
    print(config['preprocess']['destdir'])
    command = (c.format(
        config['preprocess']['destdir'],
        config['source_lang'], config['target_lang'],
        config['test']['best_model_path'],
        config['test']['save_path_output'].format("flores")
    ))
    execute_command(command)

    c = 'fairseq-generate \
         {} \
        --source-lang {} --target-lang {} \
        --path {} \
        --beam 5 --lenpen 1.2 \
        --gen-subset test1 \
        --remove-bpe=sentencepiece > {} 2>&1'
    print(config['preprocess']['destdir'])
    command = (c.format(
        config['preprocess']['destdir'],
        config['source_lang'], config['target_lang'],
        config['test']['best_model_path'],
        config['test']['save_path_output'].format("domain")
    ))
    execute_command(command)

    c = 'cat {} | grep -P "^H" |sort -V |cut -f 3- > {}'
    command = (c.format(
        config['test']['save_path_output'].format("flores"),
        config['test']['save_path_hypothesis'].format("flores")
    ))
    execute_command(command)

    c = 'cat {} | grep -P "^H" |sort -V |cut -f 3- > {}'
    command = (c.format(
        config['test']['save_path_output'].format("domain"),
        config['test']['save_path_hypothesis'].format("domain")
    ))
    execute_command(command)

    c= "sacrebleu -tok 'none' -s 'none' {} < {} > {} 2>&1"
    command = (c.format(
        config['test']['test_file_flores'],
        config['test']['save_path_hypothesis'].format('flores'),
        config['test']['sacrebleu_output'].format('flores')
    ))
    execute_command(command)

    c= "sacrebleu -tok 'none' -s 'none' {} < {} > {} 2>&1"
    command = (c.format(
        config['test']['test_file_domain'],
        config['test']['save_path_hypothesis'].format('domain'),
        config['test']['sacrebleu_output'].format('domain')
    ))
    execute_command(command)

    c= "perl ./multi-bleu.perl {} < {} > {}"
    command = (c.format(
        config['test']['test_file_flores'],
        config['test']['save_path_hypothesis'].format('flores'),
        config['test']['bleu_output'].format('flores')
    ))
    execute_command(command)

    c= "perl ./multi-bleu.perl {} < {} > {}"
    command = (c.format(
        config['test']['test_file_domain'],
        config['test']['save_path_hypothesis'].format('domain'),
        config['test']['bleu_output'].format('domain')
    ))
    execute_command(command)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True, help="Path to config file")
    args = parser.parse_args()

    test(args.config)
