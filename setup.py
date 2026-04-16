
from setuptools import setup, find_packages

setup(
    name="axaltyx",
    version="0.1.0",
    description="专业统计分析与数据可视化库",
    author="AxaltyX Team",
    packages=find_packages(),
    install_requires=[
        "numpy&gt;=1.24.0",
        "pandas&gt;=2.0.0",
        "scipy&gt;=1.10.0",
        "statsmodels&gt;=0.14.0",
        "scikit-learn&gt;=1.3.0",
        "matplotlib&gt;=3.7.0",
        "seaborn&gt;=0.12.0",
        "plotly&gt;=5.15.0",
        "lifelines&gt;=0.27.0",
        "pymc3&gt;=3.11.0",
        "nltk&gt;=3.8.0",
        "wordcloud&gt;=1.9.0",
    ],
    python_requires="&gt;=3.8",
)
