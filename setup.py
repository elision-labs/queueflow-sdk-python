from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="queueflow",
    version="1.0.0",
    author="QueueFlow Team",
    author_email="team@queueflow.dev",
    description="Official Python SDK for QueueFlow distributed job queue",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/queueflow/queueflow-sdk-python",
    project_urls={
        "Bug Tracker": "https://github.com/queueflow/queueflow-sdk-python/issues",
        "Documentation": "https://docs.queueflow.dev/sdk/python",
        "Source Code": "https://github.com/queueflow/queueflow-sdk-python",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=[
        "httpx>=0.24.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
        ],
        "sync": [
            "requests>=2.28.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "queueflow=queueflow.cli:main",
        ],
    },
    package_data={
        "queueflow": ["py.typed"],
    },
    include_package_data=True,
)