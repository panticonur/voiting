#!/bin/bash
cd -- "$(dirname "$0")"
python3 vbot.py \
    --interval=3 \
    --move_window=1900
