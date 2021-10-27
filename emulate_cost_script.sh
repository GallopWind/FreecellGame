#!/bin/zsh

zsh -c "source ~/.zshrc; conda activate torch; python emulate_cost.py 1000000 10-27_big_data1.csv big_cost" &
zsh -c "source ~/.zshrc; conda activate torch; python emulate_cost.py 1000000 10-27_big_data2.csv big_cost" &
zsh -c "source ~/.zshrc; conda activate torch; python emulate_cost.py 1000000 10-27_big_data3.csv big_cost" &
zsh -c "source ~/.zshrc; conda activate torch; python emulate_cost.py 1000000 10-27_big_data4.csv big_cost" &
zsh -c "source ~/.zshrc; conda activate torch; python emulate_cost.py 1000000 10-27_small_data5.csv small_cost" &

