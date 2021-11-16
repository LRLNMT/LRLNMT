#!/bin/bash

DIR=$1

if [ -d "$DIR" ]; then
  echo "Directory already present"
  exit 1
fi

mkdir $DIR
cd $DIR
mkdir encoded
mkdir preprocess
mkdir data
mkdir models
mkdir outputs
cd models
mkdir sentencepiece
mkdir checkpoints

echo "Finished creating directories"
