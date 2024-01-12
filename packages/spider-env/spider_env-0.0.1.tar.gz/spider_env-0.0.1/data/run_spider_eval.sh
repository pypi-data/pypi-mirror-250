#/bin/bash

# Runs under spider repo:
python evaluation.py \
    --gold evaluation_examples/gold_example.txt \
    --pred evaluation_examples/pred_example.txt \
    --etype exec \
    --db data/spider/database/ \
    --table data/spider/tables.json
