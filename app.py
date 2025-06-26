# app.py：Flask 后端服务（优化版）
#更新python为3.9以上：brew install python@3.11
# 安装依赖（如果未安装）：pip install flask transformers beautifulsoup4 requests

import os
import sys
import json
from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup

# 加载.env文件
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ 已加载 .env 文件")
except ImportError:
    print("⚠️ python-dotenv 未安装，将尝试从系统环境变量读取配置")

app = Flask(__name__)

# 为中国用户配置镜像源
def setup_china_mirrors():
    """配置中国友好的镜像源"""
    print("🇨🇳 配置中国镜像源...")
    
    # 设置 Hugging Face 镜像
    os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
    
    # 设置代理选项（如果需要）
    os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'
    os.environ['HF_HUB_CACHE'] = './models_cache'
    
    # 设置请求超时和重试
    os.environ['HF_HUB_TIMEOUT'] = '60'
    
    print("✅ 镜像源配置完成")

def load_model_with_fallback():
    """带有降级方案的模型加载"""
    try:
        print("🔄 尝试加载 zero-shot 模型...")
        from transformers import pipeline
        
        # 尝试多个模型源
        model_options = [
            "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",  # 官方模型
            "MoritzLaurer/mDeBERTa-v3-base-mnli",        # 原始模型  
            "microsoft/deberta-v3-base",                  # 基础模型
        ]
        
        for model_name in model_options:
            try:
                print(f"📥 尝试下载模型: {model_name}")
                classifier = pipeline(
                    "zero-shot-classification", 
                    model=model_name,
                    device=-1,  # 使用CPU，避免GPU问题
                    trust_remote_code=True
                )
                print(f"✅ 成功加载模型: {model_name}")
                return classifier, "model"
            except Exception as e:
                print(f"❌ 模型 {model_name} 加载失败: {str(e)}")
                continue
        
        # 所有模型都失败，返回None
        return None, "failed"
        
    except ImportError:
        print("❌ transformers 库未安装")
        return None, "no_transformers"
    except Exception as e:
        print(f"❌ 模型加载失败: {str(e)}")
        return None, "failed"

def rule_based_analysis(text):
    """基于规则的意识形态分析（备用方案）"""
    print("🔧 使用规则分析方案...")
    
    # 扩展的关键词库
    advanced_keywords = {
        "女权倾向": {
            "positive": ["女权", "平权", "独立", "自主", "平等", "解放", "自由选择", "职场女性"],
            "negative": ["反对", "批评", "质疑"],
            "weight": 1.0
        },
        "男权倾向": {
            "positive": ["传统家庭", "男主外女主内", "领导力", "阳刚", "家庭责任", "保护"],
            "negative": ["反对传统", "质疑"],
            "weight": 1.0
        },
        "厌女倾向": {
            "positive": ["拜金女", "绿茶", "情绪化", "天生劣等", "智商不行", "只会花钱"],
            "negative": ["支持女性", "尊重"],
            "weight": 1.2
        },
        "左倾表达": {
            "positive": ["人民", "工人", "反资本", "公有制", "集体利益", "社会主义", "共产"],
            "negative": ["私有", "资本主义"],
            "weight": 1.0
        },
        "右倾表达": {
            "positive": ["自由市场", "私有制", "个人主义", "减税", "小政府", "企业家"],
            "negative": ["国有", "计划经济"],
            "weight": 1.0
        },
        "情绪稳定性": {
            "positive": ["冷静", "理性", "客观", "分析", "思考"],
            "negative": ["暴躁", "骂人", "愤怒", "冲动", "情绪化"],
            "weight": 0.8
        }
    }
    
    results = {}
    text_lower = text.lower()
    
    for label, config in advanced_keywords.items():
        # 计算正面词汇得分
        positive_score = sum(1 for word in config["positive"] if word in text_lower)
        # 计算负面词汇得分
        negative_score = sum(1 for word in config["negative"] if word in text_lower)
        
        # 找到匹配的关键词
        found_keywords = []
        for word in config["positive"] + config["negative"]:
            if word in text_lower:
                found_keywords.append(word)
        
        # 计算最终得分
        base_score = (positive_score - negative_score * 0.5) * config["weight"]
        # 归一化到0-100
        final_score = max(0, min(95, base_score * 15 + len(text_lower) * 0.01))
        
        results[label] = {
            "score": round(final_score, 2),
            "keywords": found_keywords[:5]  # 最多显示5个关键词
        }
    
    return results

# 初始化阶段
setup_china_mirrors()
classifier, model_status = load_model_with_fallback()

# 🎯 优化后的标签定义 - 使用详细描述减少歧义
DETAILED_LABELS = {
    "女权倾向": "支持女性权利、性别平等、女性独立自主和反对性别歧视的观点",
    "男权倾向": "强调传统性别角色、男性主导地位、传统家庭分工的观点", 
    "厌女倾向": "贬低、歧视、偏见、仇视或用刻板印象攻击女性的观点",
    "左倾表达": "支持集体主义、社会主义、反对资本主义或强调阶级斗争的观点",
    "右倾表达": "支持个人主义、自由市场、资本主义或强调个人责任的观点",
    "情绪稳定性": "表达冷静理性思考而非情绪化、愤怒或攻击性的程度"
}

# 简短标签（用于显示）
DISPLAY_LABELS = ["女权倾向", "男权倾向", "厌女倾向", "左倾表达", "右倾表达", "情绪稳定性"]

# 详细标签（传给AI模型）
AI_LABELS = list(DETAILED_LABELS.values())

# ChatGPT 配置 - 从环境变量读取
CHATGPT_API_BASE = os.getenv("CHATGPT_API_BASE", "https://apidekey.xyz")
CHATGPT_API_KEY = os.getenv("CHATGPT_API_KEY")
CHATGPT_MODEL = os.getenv("CHATGPT_MODEL", "gpt-4o")

MAX_TEXT_LENGTH = 2000

def chatgpt_analysis(text):
    """使用ChatGPT进行意识形态分析"""
    try:
        # 检查API密钥是否配置
        if not CHATGPT_API_KEY:
            print("⚠️ ChatGPT API密钥未配置，跳过ChatGPT分析")
            return None
        
        print("🚀 使用ChatGPT分析...")
        
        # 构建专门的prompt
        prompt = f"""你是一个专业的中文意识形态分析师。请分析以下文本的意识形态倾向，并按照以下6个维度评分（0-100分）：

1. 女权倾向：支持女性权利、性别平等、女性独立自主和反对性别歧视的程度
2. 男权倾向：强调传统性别角色、男性主导地位、传统家庭分工的程度  
3. 厌女倾向：贬低、歧视、偏见、仇视或用刻板印象攻击女性的程度
4. 左倾表达：支持集体主义、社会主义、反对资本主义或强调阶级斗争的程度
5. 右倾表达：支持个人主义、自由市场、资本主义或强调个人责任的程度
6. 情绪稳定性：表达冷静理性思考而非情绪化、愤怒或攻击性的程度

请严格按照以下JSON格式返回结果，不要添加任何其他内容：
{{
    "女权倾向": {{"score": 分数(0-100), "keywords": ["关键词1", "关键词2"], "explanation": "简短解释"}},
    "男权倾向": {{"score": 分数(0-100), "keywords": ["关键词1", "关键词2"], "explanation": "简短解释"}},
    "厌女倾向": {{"score": 分数(0-100), "keywords": ["关键词1", "关键词2"], "explanation": "简短解释"}},
    "左倾表达": {{"score": 分数(0-100), "keywords": ["关键词1", "关键词2"], "explanation": "简短解释"}},
    "右倾表达": {{"score": 分数(0-100), "keywords": ["关键词1", "关键词2"], "explanation": "简短解释"}},
    "情绪稳定性": {{"score": 分数(0-100), "keywords": ["关键词1", "关键词2"], "explanation": "简短解释"}}
}}

分析文本：{text}"""

        # 调用OpenAI API
        headers = {
            "Authorization": f"Bearer {CHATGPT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": CHATGPT_MODEL,
            "messages": [
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.1,  # 降低随机性，确保结果一致性
            "max_tokens": 1000
        }
        
        # 发送请求
        response = requests.post(
            f"{CHATGPT_API_BASE}/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ ChatGPT API请求失败: {response.status_code}")
            print(f"   响应内容: {response.text}")
            return None
        
        result = response.json()
        
        # 提取回复内容
        if 'choices' not in result or len(result['choices']) == 0:
            print("❌ ChatGPT返回格式错误")
            return None
        
        content = result['choices'][0]['message']['content'].strip()
        print(f"🤖 ChatGPT原始回复: {content[:200]}...")
        
        # 尝试解析JSON
        try:
            # 清理可能的markdown格式
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            analysis_result = json.loads(content)
            
            # 转换为标准格式
            formatted_result = {}
            for dimension in DISPLAY_LABELS:
                if dimension in analysis_result:
                    formatted_result[dimension] = {
                        "score": float(analysis_result[dimension].get("score", 0)),
                        "method": "ChatGPT分析",
                        "keywords": analysis_result[dimension].get("keywords", []),
                        "explanation": analysis_result[dimension].get("explanation", "")
                    }
                else:
                    # 如果某个维度缺失，给默认值
                    formatted_result[dimension] = {
                        "score": 0.0,
                        "method": "ChatGPT分析",
                        "keywords": [],
                        "explanation": "分析结果缺失"
                    }
            
            print("✅ ChatGPT分析完成")
            return formatted_result
            
        except json.JSONDecodeError as e:
            print(f"❌ ChatGPT返回JSON解析失败: {str(e)}")
            print(f"   原始内容: {content}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ ChatGPT请求超时")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ ChatGPT连接失败")
        return None
    except Exception as e:
        print(f"❌ ChatGPT分析失败: {str(e)}")
        return None

def extract_text_from_url(url):
    """从URL提取文本内容，支持多种网站类型"""
    
    # 检查不支持的网站类型
    unsupported_sites = {
        "weibo.com": "微博",
        "xiaohongshu.com": "小红书", 
        "xhs.life": "小红书",
        "douyin.com": "抖音",
        "kuaishou.com": "快手",
        "bilibili.com": "B站"
    }
    
    for site, name in unsupported_sites.items():
        if site in url:
            return f"[暂不支持{name}链接，请手动复制文本内容进行分析]"
    
    try:
        print(f"🔗 开始抓取链接: {url}")
        
        # 优化请求头，模拟真实浏览器
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        resp = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        
        if resp.status_code != 200:
            return f"[网页访问失败，状态码：{resp.status_code}。可能需要登录或该页面不存在]"
        
        # 改进编码检测
        if resp.encoding == 'ISO-8859-1':
            resp.encoding = resp.apparent_encoding
        
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 移除script和style标签
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script.decompose()
        
        # 多种内容提取策略
        content_parts = []
        
        # 1. 尝试提取文章主体（常见的文章容器）
        article_selectors = [
            "article", ".article", "#article",
            ".content", "#content", ".post-content",
            ".entry-content", ".article-content", 
            ".post-body", ".content-body",
            "[class*='content']", "[id*='content']"
        ]
        
        article_found = False
        for selector in article_selectors:
            article = soup.select_one(selector)
            if article:
                # 提取段落和标题
                for element in article.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div']):
                    text = element.get_text().strip()
                    if len(text) > 15:  # 过滤太短的文本
                        content_parts.append(text)
                article_found = True
                break
        
        # 2. 如果没找到文章容器，使用通用策略
        if not article_found:
            # 提取所有有意义的文本元素
            for element in soup.find_all(['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                text = element.get_text().strip()
                # 过滤条件：长度 > 15，不是纯数字，不是常见的无用文本
                if (len(text) > 15 and 
                    not text.isdigit() and 
                    not any(skip in text.lower() for skip in ['cookie', 'privacy', '隐私', '版权', 'copyright', '登录', '注册'])):
                    content_parts.append(text)
        
        # 3. 去重和排序
        content_parts = list(dict.fromkeys(content_parts))  # 去重但保持顺序
        
        # 4. 组合文本
        combined = " ".join(content_parts)
        
        # 5. 清理和限制长度
        if combined:
            # 基本清理
            combined = " ".join(combined.split())  # 清理多余空白
            combined = combined.replace('\n', ' ').replace('\r', ' ')
            
            print(f"✅ 抓取成功，文本长度: {len(combined)} 字符")
            return combined[:MAX_TEXT_LENGTH] if len(combined) > MAX_TEXT_LENGTH else combined
        else:
            return "[网页内容为空或无法提取文本。可能是动态加载内容，建议手动复制文本]"
            
    except requests.exceptions.Timeout:
        return "[网页访问超时，请检查网络连接或稍后重试]"
    except requests.exceptions.ConnectionError:
        return "[网络连接失败，请检查网址是否正确]"
    except Exception as e:
        print(f"❌ 抓取失败: {str(e)}")
        return f"[网页抓取失败：{str(e)}。建议手动复制文本内容]"

def analyze_text(text):
    """统一的文本分析接口 - 实现降级策略：ChatGPT → 本地AI → 规则分析"""
    if len(text) > MAX_TEXT_LENGTH:
        return {"error": "输入文本超出长度限制（2000 字符）"}
    
    if text.startswith("[") and text.endswith("]"):
        return {"error": text}
    
    # 方案1: 尝试ChatGPT分析
    try:
        chatgpt_result = chatgpt_analysis(text)
        if chatgpt_result is not None:
            return chatgpt_result
        else:
            print("⚠️ ChatGPT分析失败，降级到本地AI模型...")
    except Exception as e:
        print(f"⚠️ ChatGPT分析异常: {str(e)}，降级到本地AI模型...")
    
    # 方案2: 尝试本地AI模型分析
    try:
        if classifier and model_status == "model":
            print("🤖 使用本地AI模型分析...")
            result = classifier(text, AI_LABELS, multi_label=True)
            response = {}
            
            # 将AI结果映射回显示标签
            for i, (detailed_label, score) in enumerate(zip(result['labels'], result['scores'])):
                try:
                    label_index = AI_LABELS.index(detailed_label)
                    display_label = DISPLAY_LABELS[label_index]
                except ValueError:
                    # 如果找不到匹配项，尝试直接使用简短标签映射
                    label_mapping = {
                        "支持女性权利、性别平等、女性独立自主和反对性别歧视的观点": "女权倾向",
                        "强调传统性别角色、男性主导地位、传统家庭分工的观点": "男权倾向",
                        "贬低、歧视、偏见、仇视或用刻板印象攻击女性的观点": "厌女倾向",
                        "支持集体主义、社会主义、反对资本主义或强调阶级斗争的观点": "左倾表达",
                        "支持个人主义、自由市场、资本主义或强调个人责任的观点": "右倾表达",
                        "表达冷静理性思考而非情绪化、愤怒或攻击性的程度": "情绪稳定性"
                    }
                    display_label = label_mapping.get(detailed_label, f"未知标签_{i}")
                
                response[display_label] = {
                    "score": round(score * 100, 2),
                    "method": "本地AI模型",
                    "keywords": [],  # AI模型不需要显示关键词
                    "description": detailed_label  # 可选：显示详细描述
                }
            return response
        else:
            print("⚠️ 本地AI模型不可用，降级到规则分析...")
    except Exception as e:
        print(f"⚠️ 本地AI模型分析失败: {str(e)}，降级到规则分析...")
    
    # 方案3: 规则分析（最终备用方案）
    try:
        print("📏 使用规则分析（最终方案）...")
        result = rule_based_analysis(text)
        for label in result:
            result[label]["method"] = "规则分析"
        return result
    except Exception as e:
        print(f"❌ 所有分析方案都失败: {str(e)}")
        # 返回默认结果
        return {
            label: {
                "score": 0.0,
                "method": "分析失败",
                "keywords": [],
                "explanation": f"分析失败: {str(e)}"
            } for label in DISPLAY_LABELS
        }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/extract", methods=["POST"])
def extract():
    """只提取内容，不分析"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "请求数据为空"})
            
        input_url = data.get("url", "").strip()
        
        if not input_url:
            return jsonify({"error": "请输入要提取的URL"})
        
        text = extract_text_from_url(input_url)
        
        if text.startswith("[") and text.endswith("]"):
            return jsonify({"error": text})
        
        return jsonify({
            "success": True,
            "text": text,
            "length": len(text)
        })
        
    except Exception as e:
        print(f"❌ 提取请求失败: {str(e)}")
        return jsonify({"error": f"服务器内部错误: {str(e)}"})

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "请求数据为空"})
            
        input_text = data.get("text", "").strip()
        input_url = data.get("url", "").strip()
        
        # 优先使用URL，其次使用文本
        if input_url:
            text = extract_text_from_url(input_url)
        elif input_text:
            if input_text.startswith("http"):
                text = extract_text_from_url(input_text)
            else:
                text = input_text
        else:
            return jsonify({"error": "请输入要分析的文本或URL"})
        
        print(f"📝 分析文本: {text[:100]}..." if len(text) > 100 else f"📝 分析文本: {text}")
        result = analyze_text(text)
        print(f"✅ 分析结果: {result}")
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ 分析请求失败: {str(e)}")
        return jsonify({"error": f"服务器内部错误: {str(e)}"})

@app.route("/health")
def health():
    """健康检查端点 - 前端页面加载时调用"""
    return jsonify({
        "status": "ok",
        "model_loaded": classifier is not None,
        "analysis_engine": "AI模型" if classifier else "规则分析"
    })

@app.route("/status")
def status():
    """系统状态检查"""
    return jsonify({
        "model_status": model_status,
        "analysis_method": "AI模型" if classifier else "规则分析",
        "china_optimized": True,
        "mirror_endpoint": os.environ.get('HF_ENDPOINT', 'default')
    })

def find_available_port(start_port=5000, max_attempts=10):
    """查找可用端口"""
    import socket
    
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

if __name__ == "__main__":
    print("🚀 启动意识形态分析器...")
    print(f"📊 本地AI模型: {'已加载' if classifier else '未加载'}")
    print(f"🤖 ChatGPT分析: {'已配置' if CHATGPT_API_KEY else '未配置'}")
    
    # 显示分析方法优先级
    methods = []
    if CHATGPT_API_KEY:
        methods.append("ChatGPT")
    if classifier:
        methods.append("本地AI")
    methods.append("规则分析")
    print(f"📋 分析方法优先级: {' → '.join(methods)}")
    
    # 查找可用端口
    available_port = find_available_port(5000)
    
    if available_port is None:
        print("❌ 无法找到可用端口 (5000-5009)")
        print("💡 解决方案:")
        print("   1. 关闭其他占用端口的程序")
        print("   2. macOS用户: 系统偏好设置 -> 通用 -> 隔空投送与接力 -> 关闭'隔空播放接收器'")
        exit(1)
    
    if available_port != 5000:
        print(f"⚠️ 端口5000被占用，使用端口 {available_port}")
        print("💡 如果是macOS，可能是AirPlay占用了5000端口")
    
    print(f"🌐 访问: http://localhost:{available_port}")
    print(f"🔍 状态检查: http://localhost:{available_port}/status")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=available_port)
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        print("💡 请检查端口是否被占用或尝试以管理员权限运行")
