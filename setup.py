#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# 读取README文件
def read_long_description():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Inet API Client - 用于访问Sky Cloud平台API的Python客户端库"

setup(
    name="inet-api-client",
    version="1.2.5",
    author="Bobby Sheng",
    author_email="Bobby@sky-cloud.net",
    description="Inet API Client - 用于访问Sky Cloud平台API的Python客户端库",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/sky-cloud/inet-api-client",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.8.0",
        "pyjwt>=2.0.0",
        "pycryptodome>=3.15.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    keywords="inet-api sky-cloud api client network management vlan vpn",
    project_urls={
        "Bug Reports": "https://github.com/sky-cloud/inet-api-client/issues",
        "Source": "https://github.com/sky-cloud/inet-api-client",
        "Documentation": "https://github.com/sky-cloud/inet-api-client/blob/main/README.md",
    },
)
