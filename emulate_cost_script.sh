#!/bin/zsh

zsh -c "source ~/.zshrc; conda activate torch; python emulate_cost.py 500 data1.csv big_cost" &
zsh -c "source ~/.zshrc; conda activate torch; python emulate_cost.py 500 data2.csv small_cost" &

