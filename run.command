#!/bin/bash
cd -- "$(dirname "$0")"
python3 vbot.py \
    --interval=4 \
    --move_window=2100
