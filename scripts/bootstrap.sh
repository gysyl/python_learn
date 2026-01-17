#!/bin/bash
# 自动安装 uv 并初始化开发环境

set -e

# 1. 检测并安装 uv
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    else
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source $HOME/.local/bin/env
    fi
else
    echo "✅ uv is already installed"
fi

# 2. 同步依赖
echo "🔄 Syncing environment..."
uv sync

echo "🎉 Environment ready! Activate with:"
echo "   source .venv/bin/activate"
