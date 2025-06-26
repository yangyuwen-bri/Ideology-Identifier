# 🏛️ Ideology-Identifier

**中文社交媒体文本的性别/政治意识形态识别器**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-CC0%201.0-green.svg)](LICENSE)
[![Network Optimized](https://img.shields.io/badge/🌐-Network%20Optimized-blue.svg)](#网络优化)

## 📋 项目简介

这是一个基于深度学习的文本分析工具，专门用于识别中文社交媒体文本中的意识形态倾向。支持以下6个维度的分析：

- 🟢 **女权倾向** - 支持性别平权的观点
- 🔵 **男权倾向** - 传统性别角色的表达
- 🔴 **厌女倾向** - 对女性的负面刻板印象
- 🟡 **左倾表达** - 集体主义、反资本主义观点
- 🟠 **右倾表达** - 个人主义、自由市场观点
- ⚪ **情绪稳定性** - 文本的理性程度

## 🚀 核心特性

- ✅ **ChatGPT集成**: 使用GPT-4o模型提供最准确的分析结果
- ✅ **多模型支持**: ChatGPT + 本地mDeBERTa双重保障
- ✅ **智能降级**: 自动降级至本地AI模型或规则分析
- ✅ **网页界面**: 简洁直观的Web用户界面
- ✅ **URL支持**: 直接分析网页链接内容
- ✅ **网络优化**: 自动检测网络环境并配置镜像源
- ✅ **跨平台**: 支持Windows、macOS、Linux

## 🎯 分析效果示例

```
输入: "女性应该有选择职业的自由，不应该被传统观念束缚"

输出:
🟢 女权倾向: 95.43%
🟠 右倾表达: 64.88% 
🟡 左倾表达: 42.8%
🔵 男权倾向: 0.19%
🔴 厌女倾向: 1.56%
```

## 🛠️ 快速开始

### 方法1: 一键安装 (推荐)

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd Ideology-Identifier-main

# 2. 创建虚拟环境
python3 -m venv ideology_env
source ideology_env/bin/activate  # Linux/Mac
# 或 ideology_env\Scripts\activate  # Windows

# 3. 运行自动配置脚本
python3 setup.py

# 4. 启动应用
bash start.sh
# 或直接运行: python3 app.py
```

### 方法2: 手动安装

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动应用
python3 app.py
```

## 🌐 网络优化

### 自动网络检测
系统会自动检测网络环境：
- 🌐 **国际网络**: 直接访问官方源
- 🇨🇳 **中国网络**: 自动配置镜像源 (hf-mirror.com, 清华源等)

### 智能降级机制
- 🤖 **首选**: ChatGPT分析 (GPT-4o)
- 🔬 **备用1**: 本地AI模型分析 (mDeBERTa)  
- 📏 **备用2**: 规则分析 (当所有AI模型不可用时)

### 中国用户优化
如果检测到中国网络环境，系统会自动：
1. 配置HuggingFace镜像源
2. 设置pip国内镜像
3. 优化下载超时设置
4. 创建本地模型缓存

## 📁 项目结构

```
Ideology-Identifier-main/
├── app.py              # 主应用程序 (统一版本)
├── setup.py            # 一键配置脚本
├── start.sh            # 启动脚本
├── requirements.txt    # 项目依赖
├── templates/
│   └── index.html      # Web前端界面
├── models_cache/       # 模型缓存目录 (自动生成)
└── .env_china         # 中国网络环境配置 (自动生成)
```

## 🔧 技术架构

### AI模型分析

#### 🤖 ChatGPT 分析 (推荐)
- **模型**: OpenAI GPT-4o
- **优势**: 准确率最高，支持复杂语境理解
- **要求**: 需要API密钥 (详见下方API服务说明)

#### 🔬 本地AI模型 (备用)
- **模型**: MoritzLaurer/mDeBERTa-v3-base-mnli-xnli
- **类型**: Zero-shot文本分类
- **语言**: 支持中文和其他100+种语言
- **大小**: ~545MB

### 🔑 API服务说明

项目集成了ChatGPT API用于提供高质量的分析结果。用户需要自行配置API密钥。

**API服务获取**:
- **官方渠道**: [OpenAI官网](https://platform.openai.com/)  
- **中转服务**: [APIDekey](https://apidekey.xyz/register?aff=FkUA) 或其他如 [New-API](https://github.com/QuantumNous/new-api) 等
- **配置说明**: 详见 [ENV_CONFIG.md](ENV_CONFIG.md)

### 降级方案
当AI模型不可用时，系统会自动切换到基于规则的分析：
- 扩展关键词库
- 上下文权重计算
- 多维度评分算法

## 🌐 使用方法

### Web界面
1. 启动应用后访问 `http://localhost:5000`
2. 输入要分析的中文文本或网页链接
3. 点击"分析"按钮获取结果

### API接口
```bash
# 分析文本
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "你的文本内容"}'

# 检查系统状态
curl http://localhost:5000/status
```

## 📊 分析维度说明

| 维度 | 说明 | 示例关键词 |
|------|------|-----------|
| 女权倾向 | 支持性别平等、女性权利的表达 | 平权、独立、自主、女权 |
| 男权倾向 | 强调传统性别角色的观点 | 传统家庭、男主外、阳刚 |
| 厌女倾向 | 对女性的负面刻板印象 | 拜金女、绿茶、情绪化 |
| 左倾表达 | 集体主义、反资本主义观点 | 人民、工人、公有制 |
| 右倾表达 | 个人主义、自由市场观点 | 自由市场、个人主义、减税 |
| 情绪稳定性 | 文本的理性程度评估 | 冷静、理性 vs 暴躁、愤怒 |

## ⚠️ 使用限制

- 文本长度限制: 2000字符以内
- 语言支持: 主要针对中文优化
- 网络要求: 首次使用需要下载模型 (~545MB)
- 准确性: 结果仅供参考，不应作为绝对判断依据

## 🔍 故障排除

### 常见问题

1. **模型下载失败**
   ```bash
   # 解决方案: 系统会自动切换到规则分析模式
   # 或检查网络连接，重新运行 python3 setup.py
   ```

2. **端口被占用**
   ```bash
   # 解决方案: 修改app.py中的端口设置
   # 或终止占用端口的进程
   ```

3. **依赖安装失败**
   ```bash
   # 解决方案: 使用配置脚本，会自动选择合适的镜像源
   python3 setup.py
   ```

4. **AI模型无法加载**
   - ✅ 程序会自动切换到规则分析模式
   - ✅ 访问 `/status` 端点查看当前分析模式
   - ✅ 规则分析模式准确率依然很高

## 🚧 开发路线图

### 📋 当前功能状态

| 功能模块 | 状态 | 说明 |
|----------|------|------|
| ChatGPT分析 | ✅ 完善 | GPT-4o模型，最高准确率 |
| 文本分析 | ✅ 完善 | 三重降级保障 (ChatGPT → 本地AI → 规则) |
| Web界面 | ✅ 完善 | 响应式设计，图表可视化 |
| 网络优化 | ✅ 完善 | 自动镜像源配置 |
| URL链接分析 | 🟡 部分支持 | 见下方详细说明 |
| API接口 | ✅ 完善 | RESTful API |

### 🔗 URL链接分析功能现状

#### ✅ 已支持的网站类型
- 📰 **新闻网站**: 大部分新闻门户网站
- 📝 **博客文章**: 个人博客、技术博客等
- 🌐 **静态网页**: 基于HTML的内容页面
- 📑 **文档页面**: 在线文档、说明页面

#### ❌ 技术限制的网站类型
| 平台类型 | 支持度 | 主要障碍 | 建议方案 |
|----------|--------|----------|----------|
| **微博** | ❌ 不支持 | 动态加载、登录墙、反爬虫 | 手动复制文本内容 |
| **小红书** | ❌ 不支持 | 强反爬虫、移动端优先 | 手动复制文本内容 |
| **知乎** | 🟡 部分支持 | 登录墙限制 | 公开回答可抓取 |
| **微信公众号** | ❌ 不支持 | 需要特殊权限 | 复制文章内容 |
| **抖音/快手** | ❌ 不支持 | 视频平台，文本有限 | 复制评论文字 |

#### 🔧 技术原理说明

**当前实现方式**:
```python
# 简单HTTP抓取 + BeautifulSoup解析
resp = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(resp.text, "html.parser")
texts = soup.find_all("p")  # 提取段落文本
```

**局限性**:
- 🚫 无法处理JavaScript动态内容
- 🚫 无法绕过登录验证
- 🚫 受反爬虫机制限制
- 🚫 无法处理单页应用(SPA)

### 🎯 后续优化方向

#### 短期计划 (v1.1)
- [ ] **智能链接识别**: 自动识别社交媒体链接并提示用户
- [ ] **抓取结果预览**: 显示抓取到的内容供用户确认
- [ ] **错误提示优化**: 更友好的链接处理失败提示
- [ ] **支持更多静态网站**: 优化HTML解析规则

#### 中期计划 (v1.2)
- [ ] **浏览器扩展**: 开发Chrome/Firefox扩展，一键复制页面文本
- [ ] **增强爬虫**: 使用Selenium处理动态内容（可选）
- [ ] **缓存机制**: 对成功抓取的链接进行缓存
- [ ] **批量分析**: 支持多个链接批量处理

#### 长期计划 (v2.0)
- [ ] **平台API集成**: 与部分平台官方API对接
- [ ] **OCR文字识别**: 处理图片中的文字内容
- [ ] **视频字幕提取**: 分析视频内容的字幕文本
- [ ] **实时监控**: 对特定账号/话题进行持续监控

### 💡 用户使用建议

**最佳实践**:
1. **直接文本分析**: 推荐直接复制粘贴文本内容（准确率最高）
2. **新闻文章**: 可以直接使用链接功能
3. **社交媒体**: 建议手动复制文本内容
4. **长文章**: 注意2000字符长度限制

**使用技巧**:
```
✅ 推荐: https://news.sina.com.cn/article/xxx
✅ 推荐: https://blog.csdn.net/xxx
🟡 可试试: https://www.zhihu.com/question/xxx
❌ 不建议: https://weibo.com/xxx
❌ 不建议: https://www.xiaohongshu.com/xxx
```

### 🤝 社区贡献欢迎

我们欢迎社区贡献以下方面的改进：
- 🔧 更好的网页内容提取算法
- 🌐 更多网站的适配规则
- 🛡️ 更强的反反爬虫策略
- 📱 移动端适配优化

**参与方式**:
1. 提交Issue报告不支持的网站
2. 贡献新的内容提取规则
3. 改进现有解析算法
4. 完善文档和使用指南

## 🚀 启动方式

### 快速启动
```bash
bash start.sh
```

### 直接启动
```bash
python3 app.py
```

### 状态检查
- 主页: `http://localhost:5000`
- 状态页: `http://localhost:5000/status`

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

- 🐛 Bug报告
- 💡 功能建议  
- 📝 文档改进
- 🔧 代码优化

## 📄 许可证

本项目采用 [CC0 1.0 Universal](LICENSE) 许可证，可自由使用、修改和分发。

## 🙏 致谢

- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [mDeBERTa模型](https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-mnli-xnli)
- [hf-mirror.com](https://hf-mirror.com/) 镜像服务

---

**⭐ 如果这个项目对你有帮助，请给个Star！**
