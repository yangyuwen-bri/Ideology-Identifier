# 🔧 详细安装指南

## 📋 系统要求

- **Python**: 3.9+ (推荐 3.11+)
- **操作系统**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **内存**: 至少 4GB RAM (推荐 8GB+)
- **存储**: 至少 2GB 可用空间 (用于模型缓存)
- **网络**: 首次运行需要下载 ~545MB 模型文件

## 🌍 不同地区安装指南

### 🇨🇳 中国用户 (推荐方式)

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd Ideology-Identifier-main

# 2. 创建虚拟环境
python3 -m venv ideology_env

# 3. 激活虚拟环境
# macOS/Linux:
source ideology_env/bin/activate
# Windows:
ideology_env\Scripts\activate

# 4. 一键配置 (自动处理镜像源、依赖等)
python setup_china.py

# 5. 启动应用
python app_china.py
```

### 🌍 国际用户

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd Ideology-Identifier-main

# 2. 创建虚拟环境
python3 -m venv ideology_env
source ideology_env/bin/activate  # Linux/Mac
# 或 ideology_env\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动应用
python app.py
```

## 🔧 手动安装步骤

### 步骤1: Python环境检查

```bash
# 检查Python版本
python --version
# 或
python3 --version

# 如果版本低于3.9，请升级Python
```

### 步骤2: 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv ideology_env

# 激活虚拟环境
# Windows:
ideology_env\Scripts\activate
# macOS/Linux:
source ideology_env/bin/activate

# 确认虚拟环境已激活 (命令行前应该有 (ideology_env) 前缀)
```

### 步骤3: 安装依赖

#### 选项A: 标准安装
```bash
pip install -r requirements.txt
```

#### 选项B: 中国镜像安装
```bash
pip install -r requirements-china.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 选项C: 分步安装 (如果遇到问题)
```bash
# 基础依赖
pip install flask beautifulsoup4 requests

# AI依赖 (如果网络有问题可以单独安装)
pip install transformers torch numpy
```

### 步骤4: 启动应用

```bash
# 标准版本
python app.py

# 中国优化版本
python app_china.py

# 自定义端口
python -c "import app_china; app_china.app.run(port=5001)"
```

## 🚨 常见问题解决

### 问题1: 模型下载失败

**症状**: `SSLError`, `ConnectionError`, `TimeoutError`

**解决方案**:
```bash
# 方案1: 使用中国优化版本
python app_china.py

# 方案2: 设置环境变量
export HF_ENDPOINT=https://hf-mirror.com
python app.py

# 方案3: 手动配置代理
export https_proxy=http://your-proxy:port
python app.py
```

### 问题2: 依赖安装失败

**症状**: `pip install` 出错

**解决方案**:
```bash
# 方案1: 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 方案2: 升级pip
pip install --upgrade pip

# 方案3: 单独安装问题包
pip install transformers --no-cache-dir
```

### 问题3: 端口被占用

**症状**: `Address already in use`

**解决方案**:
```bash
# 方案1: 使用其他端口
python -c "import app_china; app_china.app.run(port=5001)"

# 方案2: 关闭占用端口的程序
# macOS: 关闭 AirPlay Receiver
# Windows: 检查任务管理器
# Linux: lsof -i :5000
```

### 问题4: 内存不足

**症状**: 程序崩溃或运行缓慢

**解决方案**:
```bash
# 使用CPU模式 (已在代码中默认启用)
# 减少并发请求
# 关闭其他占用内存的程序
```

## 🧪 安装验证

### 验证步骤

1. **检查应用启动**:
   ```bash
   curl http://localhost:5000/status
   ```

2. **测试分析功能**:
   ```bash
   curl -X POST http://localhost:5000/analyze \
     -H "Content-Type: application/json" \
     -d '{"text": "测试文本"}'
   ```

3. **检查Web界面**:
   - 浏览器访问 `http://localhost:5000`
   - 输入测试文本进行分析

### 预期结果

- ✅ 状态检查返回JSON响应
- ✅ 分析接口返回评分结果
- ✅ Web界面正常显示和交互

## 🔄 更新和维护

### 更新模型

```bash
# 清除模型缓存
rm -rf models_cache/
rm -rf ~/.cache/huggingface/

# 重新启动应用下载最新模型
python app_china.py
```

### 更新依赖

```bash
# 更新到最新版本
pip install --upgrade -r requirements.txt
```

### 备份和恢复

```bash
# 备份配置
cp .env_china .env_china.backup

# 恢复配置
cp .env_china.backup .env_china
```

## 🐳 Docker安装 (可选)

如果你熟悉Docker，可以使用容器化部署：

```dockerfile
# Dockerfile示例
FROM python:3.11-slim

WORKDIR /app
COPY requirements-china.txt .
RUN pip install -r requirements-china.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .
EXPOSE 5000

ENV HF_ENDPOINT=https://hf-mirror.com
CMD ["python", "app_china.py"]
```

```bash
# 构建和运行
docker build -t ideology-identifier .
docker run -p 5000:5000 ideology-identifier
```

## 📞 获取帮助

如果遇到其他问题：

1. 📋 查看 [常见问题](README.md#故障排除)
2. 🐛 提交 [Issue](../../issues)
3. 💬 参与 [讨论](../../discussions)
4. 📧 联系维护者

---

**💡 提示**: 建议首次安装时选择 `python setup_china.py` 自动配置，这会自动处理大部分网络和环境问题。 