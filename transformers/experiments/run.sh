#!/bin/bash

lang=$1
dataset=$2
size=$3
r=$4

if [ "$r" -eq "1" ]; then
  DIR="${lang}_en_${dataset}_${size}"
else
  DIR="en_${lang}_${dataset}_${size}"
fi

sh ./create_folders.sh $DIR
sh ./clean_folders.sh $DIR

echo "Creating config"
python create_config.py --lang $lang --size $size --dataset $dataset --r $r
echo "Config creation finished"

echo "Started training"
python train_transformer.py --config "./configs/config_$DIR.json"
echo "finished training"

echo "started testing"
python test_transformer.py --config "./configs/config_$DIR.json"
echo "finished testing"
