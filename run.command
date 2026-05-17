#!/bin/bash
cd -- "$(dirname "$0")"
python3 vbot.py --interval=2 --move_window=1900
