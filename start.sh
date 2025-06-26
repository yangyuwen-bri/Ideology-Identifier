#!/bin/bash
# start.sh - 意识形态分析器启动脚本

echo "🚀 启动意识形态分析器..."

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python版本检查通过: $python_version"
else
    echo "⚠️ Python版本过低: $python_version (建议 >= 3.9)"
    echo "   macOS用户可运行: brew install python@3.11"
fi

# 检查依赖
echo "🔍 检查依赖..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "❌ Flask未安装，请运行: pip install -r requirements.txt"
    exit 1
fi

if ! python3 -c "import transformers" 2>/dev/null; then
    echo "⚠️ Transformers未安装，将使用规则分析模式"
fi

# 加载环境变量（如果存在）
if [ -f .env_china ]; then
    echo "🇨🇳 加载中国镜像源配置..."
    source .env_china
fi

# 启动应用
echo "🌐 启动服务器..."
echo "   程序会自动选择可用端口"
echo "   按 Ctrl+C 停止服务"
echo ""

python3 app.py 