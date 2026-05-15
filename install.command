#!/bin/bash
# https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/


# Check if Python 3 is already installed
if command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is already installed: $(python3 --version)"
else
    echo "Python 3 not found. Starting installation..."

    # Check if Homebrew is installed, install if not
    if ! command -v brew >/dev/null 2>&1; then
        echo "Homebrew not found. Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add Homebrew to PATH for the current session (for ARM Macs/Apple Silicon)
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi

    # Install Python 3 using Homebrew
    echo "Installing Python 3 via Homebrew..."
    brew install python
fi

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

pip install --upgrade selenium

if command -v brew >/dev/null 2>&1; then
    echo "Homebrew is installed"

    brew install --cask chromedriver

else
    echo "Homebrew is NOT installed"

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
