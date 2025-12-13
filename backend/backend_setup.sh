#!/bin/bash
# Backend setup script for Somen Spirits

set -e


# Check for uv and method of installation if not found
if ! command -v uv &> /dev/null; then
    if ! command -v curl &> /dev/null; then
        echo "going to try to use wget instead..."
        if ! command -v wget &> /dev/null; then
            echo "Neither curl nor wget is installed. Please install one of them to proceed (preferably curl)."
            exit 1
        fi
          wget -qO- https://astral.sh/uv/install.sh | sh
    fi
    echo "uv is not installed. Installing uv with curl..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

if ! command -v redis-cli &> /dev/null; then
    echo "Redis is not installed. Please install Redis."
    
fi


echo "Creating virtual environment with uv..."
uv venv
source .venv/bin/activate

echo "Installing dependencies with uv..."
uv pip install -r requirements.txt

mkdir -p data

#should seed db and start backend server after passes
