from setuptools import setup, find_packages

setup(
    name='coggle',
    version='0.1',
    description='数据挖掘和人工智能项目最佳实践',
    author='Yuzhong Liu',
    author_email='finlayliu@qq.com',
    packages = find_packages(),
    url="https://github.com/coggle-club/coggle",
    install_requires=[
        'numpy',
        'pandas',
        'jieba',
        'gensim',
        'emoji',
        'joblib',
        'scikit-learn'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)