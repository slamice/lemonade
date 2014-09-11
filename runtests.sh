#!/bin/bash -eux

export NLTK_DATA=$PWD/nltk_data
export PYTHONPATH=$PWD
python ./tests/tests.py