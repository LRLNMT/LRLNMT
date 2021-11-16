#!/bin/bash

DIR=$1

if [ -d "$DIR" ]; then
  echo "Cleaning .."
  cd $DIR
  rm -rf encoded/*
  rm -rf preprocess/*
  rm -rf models/checkpoints/*
  rm -rf models/sentencepiece/*
  rm -rf outputs/*
  echo "Finished cleaning"
else
  echo "No directory"
fi
