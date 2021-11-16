import os
import subprocess
import json
import argparse

def execute_command(command):
    output = subprocess.run(command, shell=True)

def create_sentencepiece(config):
    c = "python {}  \
        --input={} \
        --model_prefix={} \
        --vocab_size={} \
        --character_coverage=1.0 \
        --model_type=bpe"
    command = (c.format(
        config['sentencepiece']['script_path'],
        config['sentencepiece']['input'],
        config['sentencepiece']['model_save_path'],
        config['sentencepiece']['vocab_size']
    ))
    execute_command(command)

def encode(config, mode='train'):
    c = "python {} --model {}.model --output_format=piece --inputs {} --outputs {} --min-len 0"
    command = (c.format(config['encoder']['encoder_script_path'], config['sentencepiece']['model_save_path'],
                config['encoder'][mode]['inputs'], config['encoder'][mode]['outputs']))
    execute_command(command)

def preprocess(config):
    c = "fairseq-preprocess --source-lang {} --target-lang {} \
        --trainpref {} --validpref {} --testpref {} --destdir {} \
        --joined-dictionary"
    command = (c.format(config['source_lang'], config['target_lang'], config['preprocess']['trainpref'],
            config['preprocess']['validpref'], config['preprocess']['testpref'],
            config['preprocess']['destdir']))
    execute_command(command)

def train(config):
    c = "fairseq-train \
        {}\
        --source-lang {} --target-lang {} \
        --arch transformer --share-all-embeddings \
        --encoder-layers {} --decoder-layers {} \
        --encoder-embed-dim {} --decoder-embed-dim {} \
        --encoder-ffn-embed-dim {} --decoder-ffn-embed-dim {} \
        --encoder-attention-heads {} --decoder-attention-heads {} \
        --encoder-normalize-before --decoder-normalize-before \
        --dropout {} --attention-dropout {} --relu-dropout {} \
        --weight-decay {} \
        --label-smoothing {} --criterion label_smoothed_cross_entropy \
        --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm {} \
        --lr-scheduler inverse_sqrt --warmup-updates {} --warmup-init-lr 1e-7 \
        --lr {} --stop-min-lr 1e-9 \
        --batch-size {} \
        --update-freq {} \
        --max-epoch {} --keep-best-checkpoints {} \
        --tensorboard-logdir {} \
        --save-dir {} \
        --no-epoch-checkpoints \
        --patience 6"
    command = (c.format(
            config['preprocess']['destdir'],
            config['source_lang'], config['target_lang'],
            config['train']['encoder-layers'], config['train']['decoder-layers'],
            config['train']['encoder-embed-dim'], config['train']['decoder-embed-dim'],
            config['train']['encoder-ffn-embed-dim'], config['train']['decoder-ffn-embed-dim'],
            config['train']['encoder-attention-heads'], config['train']['decoder-attention-heads'],
            config['train']['dropout'], config['train']['attention-dropout'],
            config['train']['relu-dropout'], config['train']['weight-decay'],
            config['train']['label-smoothing'], config['train']['clip-norm'],
            config['train']['warmup-updates'], config['train']['lr'],
            config['train']['batch-size'], config['train']['update-freq'], config['train']['max-epoch'],
            config['train']['keep-best-checkpoints'], config['train']['tensorboard-logdir'],
            config['train']['save-dir']
    ))

    execute_command(command)

def main(args):
    config = json.load(open(args.config))
    try:
        create_sentencepiece(config)
        #assert os.path.exists(config['sentencepiece']['model_save_path']), "Sentence piece model not created."
        print("Sentence piece model creation successful")
    except Exception as e:
        print("Sentence piece creation failed with error \n", str(e))

    try:
        encode(config, 'train')
        encode(config, 'valid')
        encode(config, 'test')
        encode(config, 'test_domain')
        print("Encoding dataset creation successful")
    except Exception as e:
        print("encoding dataset failed with error \n", str(e))

    try:
        preprocess(config)
        print("Preprocessing successful")
    except Exception as e:
        print("preprocessing dataset failed with error \n", str(e))

    try:
        train(config)
        print("Training successful")
    except Exception as e:
        print("training failed with error \n", str(e))

    print("Hurray!! Completed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True, help="Path to config file")
    args = parser.parse_args()

    main(args)
