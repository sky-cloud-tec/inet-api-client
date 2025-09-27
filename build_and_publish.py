#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建和发布脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd, check=True):
    """运行命令"""
    print(f"执行命令: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check)
    return result.returncode == 0


def clean_build():
    """清理构建文件"""
    print("清理构建文件...")
    
    dirs_to_clean = ['build', 'dist', 'inet_api_client.egg-info']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"删除目录: {dir_name}")


def build_package():
    """构建包"""
    print("开始构建包...")
    
    # 使用setuptools构建
    if not run_command("python setup.py sdist bdist_wheel"):
        print("❌ 构建失败")
        return False
    
    print("✅ 包构建成功")
    return True


def check_package():
    """检查包"""
    print("检查包...")
    
    # 检查包内容
    if not run_command("twine check dist/*"):
        print("❌ 包检查失败")
        return False
    
    print("✅ 包检查通过")
    return True


def install_local():
    """本地安装测试"""
    print("本地安装测试...")
    
    # 卸载现有版本
    run_command("pip uninstall inet-api-client -y", check=False)
    
    # 安装新版本
    if not run_command("pip install dist/*.whl"):
        print("❌ 本地安装失败")
        return False
    
    print("✅ 本地安装成功")
    return True


def test_import():
    """测试导入"""
    print("测试导入...")
    
    try:
        import inet_api_client
        print(f"✅ 导入成功，版本: {inet_api_client.__version__}")
        
        # 测试主要类
        from inet_api_client import ApiClient, SkyApiException
        print("✅ 主要类导入成功")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False


def publish_to_testpypi():
    """发布到测试PyPI"""
    print("发布到测试PyPI...")
    
    if not run_command("twine upload --repository testpypi dist/*"):
        print("❌ 发布到测试PyPI失败")
        return False
    
    print("✅ 发布到测试PyPI成功")
    return True


def publish_to_pypi():
    """发布到PyPI"""
    print("发布到PyPI...")
    
    if not run_command("twine upload dist/*"):
        print("❌ 发布到PyPI失败")
        return False
    
    print("✅ 发布到PyPI成功")
    return True


def main():
    """主函数"""
    print("Inet API Client 构建和发布工具")
    print("===============================")
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python build_and_publish.py clean    - 清理构建文件")
        print("  python build_and_publish.py build    - 构建包")
        print("  python build_and_publish.py check    - 检查包")
        print("  python build_and_publish.py install  - 本地安装测试")
        print("  python build_and_publish.py test     - 测试导入")
        print("  python build_and_publish.py testpypi - 发布到测试PyPI")
        print("  python build_and_publish.py pypi     - 发布到PyPI")
        print("  python build_and_publish.py all      - 执行完整流程")
        return
    
    action = sys.argv[1].lower()
    
    # 切换到脚本所在目录
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    if action == "clean":
        clean_build()
        
    elif action == "build":
        clean_build()
        build_package()
        
    elif action == "check":
        check_package()
        
    elif action == "install":
        install_local()
        
    elif action == "test":
        test_import()
        
    elif action == "testpypi":
        publish_to_testpypi()
        
    elif action == "pypi":
        publish_to_pypi()
        
    elif action == "all":
        print("执行完整构建流程...")
        
        # 1. 清理
        clean_build()
        
        # 2. 构建
        if not build_package():
            return
        
        # 3. 检查
        if not check_package():
            return
        
        # 4. 本地安装测试
        if not install_local():
            return
        
        # 5. 测试导入
        if not test_import():
            return
        
        print("\n✅ 完整构建流程成功完成！")
        print("\n后续步骤:")
        print("1. 发布到测试PyPI: python build_and_publish.py testpypi")
        print("2. 测试安装: pip install -i https://test.pypi.org/simple/ inet-api-client")
        print("3. 发布到正式PyPI: python build_and_publish.py pypi")
        
    else:
        print(f"未知操作: {action}")


if __name__ == "__main__":
    main()
