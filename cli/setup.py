from setuptools import setup, find_packages

setup(
    name="veterans-verify-cli",
    version="1.0.0",
    description="Command-line interface for Veterans Verification System",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/veterans-verify-system",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.0",
        "requests>=2.31.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "veterans-cli=veterans_cli.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
)
