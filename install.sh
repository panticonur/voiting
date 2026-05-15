#!/bin/bash



if [[ $(uname -m) == 'arm64' ]]; then
    echo "Running natively on Apple Silicon (arm64)"
    wget https://storage.googleapis.com/chrome-for-testing-public/148.0.7778.167/mac-arm64/chromedriver-mac-arm64.zip
    unzip chromedriver-mac-arm64.zip
else
    echo "Running on Intel or via Rosetta (x86_64)"
    wget https://storage.googleapis.com/chrome-for-testing-public/148.0.7778.167/mac-x64/chromedriver-mac-x64.zip
    unzip chromedriver-mac-x64.zip
fi


sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
chromedriver --version

