#!/bin/bash

nohup python3 ./news_auto.py > ./logs/qq_auto.log 2>&1 &
nohup python3 ./news_cul.py > ./logs/qq_cul.log 2>&1 &
nohup python3 ./news_ent.py > ./logs/qq_ent.log 2>&1 &
nohup python3 ./news_finance.py > ./logs/qq_finance.log 2>&1 &
nohup python3 ./news_sports.py > ./logs/qq_sports.log 2>&1 &
nohup python3 ./news_tech.py > ./logs/qq_tech.log 2>&1 &
