from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xai-investment",
    version="0.1.0",
    author="Léo Lans, Wandrille Esnault, Martin Jezequel",
    author_email="team@xai-investment.com",
    description="IA Explicable pour Décisions d'Investissement",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/xai-investment",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "xgboost>=2.0.0",
        "lightgbm>=4.0.0",
        "shap>=0.42.0",
        "lime>=0.2.0",
        "alibi>=0.9.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "plotly>=5.17.0",
        "streamlit>=1.28.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.0",
        "yfinance>=0.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "jupyter>=1.0.0",
            "ipykernel>=6.0.0",
        ],
        "llm": [
            "openai>=1.0.0",
            "langchain>=0.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "xai-investment=app.app:main",
        ],
    },
)
