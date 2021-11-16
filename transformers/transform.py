import json
import os
import argparse

def main(filename, src, trg, dest_src, dest_trg):
    source = []
    target = []
    with open(filename, 'r') as f:
        data = f.readlines()
        for d in data:
            d = d.strip()
            dict = json.loads(d)
            source.append(dict['translation'][src])
            target.append(dict['translation'][trg])

    if len(source) != len(target):
        print("incorrect length")
        return

    with open(dest_src, 'w') as f:
        for sent in source:
            f.write(sent+"\n")
    with open(dest_trg, 'w') as f:
        for sent in target:
            f.write(sent+"\n")

    print("successfullt finished")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str, default="")
    parser.add_argument("--src", type=str, default="", help='source language code')
    parser.add_argument("--trg", type=str, default="", help="target language code")
    parser.add_argument("--dest_src", type=str, default="")
    parser.add_argument("--dest_trg", type=str, default="")

    args = parser.parse_args()

    main(args.filename, args.src, args.trg, args.dest_src, args.dest_trg)
