# 环境变量配置说明

## ChatGPT功能配置

为了使用ChatGPT分析功能，需要设置以下环境变量：

### 方法1: 在终端中设置
```bash
export CHATGPT_API_BASE="https://apidekey.xyz"
export CHATGPT_API_KEY="你的API密钥"
export CHATGPT_MODEL="gpt-4o"
```

### 方法2: 创建.env文件（推荐）
在项目根目录创建 `.env` 文件：
```
CHATGPT_API_BASE=https://apidekey.xyz
CHATGPT_API_KEY=你的API密钥
CHATGPT_MODEL=gpt-4o
```

然后在启动应用前加载环境变量：
```bash
# 安装python-dotenv（如果需要）
pip install python-dotenv

# 启动应用
python app.py
```

### 方法3: 直接在启动命令中设置
```bash
CHATGPT_API_KEY="你的API密钥" python app.py
```

## 安全提醒

⚠️ **重要**: 
- 绝不要将API密钥提交到Git仓库
- 将 `.env` 文件添加到 `.gitignore`
- 在生产环境中使用更安全的密钥管理方案

## 中国用户优化

🇨🇳 **自动配置** - 系统已自动为中国用户配置优化：
- Hugging Face 镜像源：`https://hf-mirror.com`
- 模型缓存路径：`./models_cache`
- 网络超时优化：60秒
- 进度条禁用：减少输出干扰

无需额外配置，应用启动时自动生效。

## 降级策略

如果没有配置ChatGPT API密钥，系统会自动降级到：
1. 本地AI模型（mDeBERTa）
2. 规则分析

这确保了系统在任何情况下都能正常工作。 