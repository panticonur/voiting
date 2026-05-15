#!/bin/bash

cd -- "$(dirname "$0")"

python3 vbot.py --interval=1 --page_name="https://tafel-oesterreich.at/voting-2026/" --item_name="Integrationstreffen 50+ (Neki)"

