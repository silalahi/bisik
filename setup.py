from setuptools import setup, find_packages

setup(
    name="ai-pronunciation-trainer",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "flask>=3.0.0",
        "torch>=2.1.0",
        "openai-whisper>=20231117",
        "epitran>=1.24",
    ],
    python_requires=">=3.9",
)