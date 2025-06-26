#!/usr/bin/env python3
# setup.py：一键配置脚本

import os
import sys
import subprocess
import platform

def print_banner():
    print("""
🎯 意识形态分析器 - 一键配置
================================
📍 自动配置镜像源  
🔧 智能检测环境  
📦 安装必要依赖
🚀 一键启动应用
""")

def setup_mirrors():
    """配置镜像源"""
    print("📦 配置镜像源...")
    
    # 检测网络环境
    is_china = False
    try:
        import urllib.request
        urllib.request.urlopen("https://www.google.com", timeout=5)
        print("🌐 检测到国际网络环境")
    except:
        print("🇨🇳 检测到中国网络环境，配置镜像源...")
        is_china = True
    
    if is_china:
        # 配置pip镜像
        pip_conf_dir = os.path.expanduser("~/.pip")
        pip_conf_file = os.path.join(pip_conf_dir, "pip.conf")
        
        os.makedirs(pip_conf_dir, exist_ok=True)
        
        pip_config = """[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
timeout = 60
retries = 3
"""
        
        with open(pip_conf_file, 'w', encoding='utf-8') as f:
            f.write(pip_config)
        
        # 创建环境配置文件
        env_file = ".env_china"
        env_settings = {
            'HF_ENDPOINT': 'https://hf-mirror.com',
            'HF_HUB_DISABLE_PROGRESS_BARS': '1',
            'HF_HUB_CACHE': './models_cache',
            'HF_HUB_TIMEOUT': '120',
        }
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write("# 中国网络环境配置\n")
            for key, value in env_settings.items():
                f.write(f"export {key}={value}\n")
        
        print(f"✅ 镜像源配置完成")
        return True
    
    return False

def install_dependencies():
    """安装依赖包"""
    print("📚 安装项目依赖...")
    
    try:
        # 安装依赖
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                     check=True)
        print("✅ 依赖安装成功")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️ 部分依赖安装失败，但程序仍可使用规则分析模式")
        return False

def create_startup_script():
    """确保启动脚本可执行"""
    if platform.system() != "Windows":
        try:
            os.chmod("start.sh", 0o755)
            print("✅ 启动脚本权限设置完成")
        except:
            pass

def main():
    print_banner()
    
    # 1. 配置镜像
    is_china = setup_mirrors()
    
    # 2. 安装依赖
    deps_ok = install_dependencies()
    
    # 3. 设置启动脚本
    create_startup_script()
    
    # 总结报告
    print("\n" + "="*50)
    print("🎉 配置完成！")
    print("="*50)
    print("📊 配置结果:")
    print(f"  🌐 网络环境: {'中国镜像源' if is_china else '国际网络'}")
    print(f"  📦 依赖安装: {'✅ 成功' if deps_ok else '⚠️ 部分失败'}")
    
    print("\n🚀 启动方式:")
    print("  方式1: bash start.sh")
    print("  方式2: python3 app.py")
    
    print("\n💡 使用说明:")
    if not deps_ok:
        print("  ⚠️ AI依赖安装失败，将使用规则分析模式")
    print("  🌐 访问地址: http://localhost:5000")
    print("  🔍 系统状态: http://localhost:5000/status")

if __name__ == "__main__":
    main() 