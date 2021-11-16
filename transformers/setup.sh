#!/bin/bash

# installing fairseq
git clone https://github.com/pytorch/fairseq
cd fairseq
pip install --editable ./
pip install sentencepiece sacrebleu tensorboardX
