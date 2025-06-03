#!/usr/bin/env python3
"""
LightRAG 知识库增强功能安装脚本
"""

import subprocess
import sys
import os

def install_package(package):
    """安装Python包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    print("🚀 Installing LightRAG Knowledge Base Enhancement...")
    print("=" * 50)
    
    # LightRAG相关依赖 - 使用正确的包名和简化的依赖
    packages = [
        "lightrag-hku",  # 正确的LightRAG包名
        "faiss-cpu==1.7.4",
        "pypdf==3.17.4",
        "docx2txt==0.8",
        "pandas==2.0.3",
        "numpy==1.24.3"
    ]
    
    failed_packages = []
    
    for package in packages:
        print(f"\n📦 Installing {package}...")
        if not install_package(package):
            failed_packages.append(package)
    
    print("\n" + "=" * 50)
    
    if not failed_packages:
        print("🎉 All packages installed successfully!")
        print("\n💡 Knowledge Base Features Available:")
        print("   - Smart requirement analysis with domain expertise")
        print("   - Contextual question generation")
        print("   - Best practices recommendations")
        print("   - Requirement completeness assessment")
        print("\n🚀 You can now run the application with: python run.py")
    else:
        print("⚠️ Some packages failed to install:")
        for package in failed_packages:
            print(f"   - {package}")
        print("\n🔧 You may need to install them manually or check your Python environment.")
        print("   The application will still work but with limited knowledge base features.")

if __name__ == "__main__":
    main() 