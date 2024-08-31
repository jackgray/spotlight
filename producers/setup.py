from setuptools import setup, find_packages

setup(
    name='spotlight_utils',  
    version='0.1.0',  
    description='Commonly used functions in spotlights data retrieval', 
    author='Jack Gray', 
    author_email='',  
    packages=find_packages(),  # Automatically find all packages and subpackages
    install_requires=[
        'pandas', 
        'clickhouse_connect',
        'backoff',
        'psutil'
        # 'apache-airflow'
    ],
    classifiers=[
        'Programming Language :: Python :: 3', 
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11', 
)
