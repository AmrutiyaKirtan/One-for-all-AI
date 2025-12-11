"""
Setup script for AI Assistant
"""

from setuptools import setup, find_packages

setup(
    name="ai-assistant",
    version="1.0.0",
    description="Cross-platform AI assistant with voice recognition and TTS",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "speechrecognition>=3.10.0",
        "pyttsx3>=2.90",
        "pyaudio>=0.2.11",
        "openai>=1.3.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0"
    ],
    entry_points={
        'console_scripts': [
            'ai-assistant=main:main',
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)