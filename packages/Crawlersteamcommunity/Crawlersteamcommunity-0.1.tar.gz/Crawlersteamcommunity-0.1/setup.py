from setuptools import setup, find_packages

setup(
    name='Crawlersteamcommunity',
    version='0.1',
    packages=find_packages(),
    description='用于 steamcommunity.com 的简单网络爬虫',
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)