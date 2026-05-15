#!/bin/bash
# https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/

if command -v brew >/dev/null 2>&1; then
    echo "Homebrew is installed"
    
    brew install google-chrome
    brew install --cask chromedriver

else
    echo "Homebrew is NOT installed"

    temp=$TMPDIR$(uuidgen)
    mkdir -p $temp/mount
    curl https://dl.google.com/chrome/mac/stable/GGRO/googlechrome.dmg > $temp/1.dmg
    yes | hdiutil attach -noverify -nobrowse -mountpoint $temp/mount $temp/1.dmg
    cp -r $temp/mount/*.app /Applications
    hdiutil detach $temp/mount
    rm -r $temp

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
fi

chromedriver --version
