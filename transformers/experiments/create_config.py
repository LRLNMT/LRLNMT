import os
import json
import argparse
def create(args):
    s = {"1k":1000, "10k": 10000, "25k": 25000, "50k":50000, "100k": 100000, "200k": 200000}
    if args.size == "1k":
        config = json.load(open('./config_1k.json'))
    else:
        config = json.load(open('./config_cc.json'))

    if args.r == "1":
        src = args.lang
        trg = "en"
    else:
        src = "en"
        trg = args.lang

    folder_name = "_".join([src, trg, args.dataset, args.size])

    config['source_lang'] = src
    config['target_lang'] = trg

    train_path = "./dataset/{}/train/{}/{}/train_{}.txt"
    dev_path = "./dataset/{}/dev/{}/dev_{}.txt"
    test_path = "./dataset/{}/test/{}/test_{}.txt"

    # sentencepiece
    config['sentencepiece']['input'] = train_path.format(args.lang, args.dataset, args.size, src ) + ',' +\
                            train_path.format(args.lang, args.dataset, args.size, trg )
    config['sentencepiece']['model_save_path'] = folder_name+"/models/sentencepiece/sentencepiece.bpe"
    if s[args.size] == 1000:
        config['sentencepiece']['vocab_size'] = 5000
    else:
        config['sentencepiece']['vocab_size'] = str(min(s[args.size]//2, 10000))

    config['encoder']['train']['inputs'] = train_path.format(args.lang, args.dataset, args.size, src ) + ' ' +\
                            train_path.format(args.lang, args.dataset, args.size, trg )
    config['encoder']['train']['outputs'] = "{}/encoded/train.bpe.{} {}/encoded/train.bpe.{}".format(folder_name, src, folder_name, trg)

    if args.dataset == "cc_aligned":
        config['encoder']['valid']['inputs'] = dev_path.format(args.lang, 'flores', src ) + ' ' +\
                                dev_path.format(args.lang, 'flores', trg )
    else:
        config['encoder']['valid']['inputs'] = dev_path.format(args.lang, args.dataset, src ) + ' ' +\
                                dev_path.format(args.lang, args.dataset, trg )
    config['encoder']['valid']['outputs'] = "{}/encoded/valid.bpe.{} {}/encoded/valid.bpe.{}".format(folder_name, src, folder_name, trg)

    config['encoder']['test']['inputs'] = test_path.format(args.lang, 'flores', src ) + ' ' +\
                            test_path.format(args.lang, 'flores', trg )
    config['encoder']['test']['outputs'] = "{}/encoded/test.bpe.{} {}/encoded/test.bpe.{}".format(folder_name, src, folder_name, trg)

    if args.dataset == "cc_aligned":
        config['encoder']['test_domain']['inputs'] = test_path.format(args.lang, 'flores', src ) + ' ' +\
                                test_path.format(args.lang, 'flores', trg )
    else:
        config['encoder']['test_domain']['inputs'] = test_path.format(args.lang, args.dataset, src ) + ' ' +\
                                test_path.format(args.lang, args.dataset, trg )
    config['encoder']['test_domain']['outputs'] = "{}/encoded/test_domain.bpe.{} {}/encoded/test_domain.bpe.{}".format(folder_name, src, folder_name, trg)

    config['preprocess']['trainpref'] = folder_name+'/encoded/train.bpe'
    config['preprocess']['validpref'] = folder_name+'/encoded/valid.bpe'
    config['preprocess']['testpref'] = folder_name+'/encoded/test.bpe'+','+folder_name+'/encoded/test_domain.bpe'
    config['preprocess']['destdir'] = folder_name+'/preprocess'

    config['train']['tensorboard-logdir'] = folder_name+'/logs'
    config['train']['save-dir'] = folder_name+'/models/checkpoints'

    config['test']['best_model_path'] = folder_name+'/models/checkpoints/checkpoint_best.pt'
    config['test']['save_path_output'] = folder_name+'/outputs/output_{}.txt'
    config['test']['save_path_hypothesis'] = folder_name+ '/outputs/output_{}.hyp'
    config['test']['test_file_flores'] = test_path.format(args.lang, 'flores', trg )
    if args.dataset == "cc_aligned":
        config['test']['test_file_domain'] = test_path.format(args.lang, 'flores', trg )
    else:
        config['test']['test_file_domain'] = test_path.format(args.lang, args.dataset, trg )
    config['test']['sacrebleu_output'] = folder_name+'/outputs/sacrebleu_{}.txt'
    config['test']['bleu_output'] = folder_name+'/outputs/bleu_{}.txt'

    filename = './configs/config_'+folder_name+'.json'
    print(config)
    with open(filename, 'w') as f:
        json.dump(config, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', type=str, required=True, help="Path to config file")
    parser.add_argument('--size', type=str, required=True, help="Path to config file")
    parser.add_argument('--dataset', type=str, required=True, help="Path to config file")
    parser.add_argument('--r', type=str, required=True, help="Path to config file")
    args = parser.parse_args()

    create(args)
