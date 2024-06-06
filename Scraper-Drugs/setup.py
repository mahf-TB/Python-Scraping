from setuptools import setup,find_packages

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().split('\n')
    
        
setup(
    name='drugs_data',
    version='1.0.0',
    install_requires=requirements,
    packages=find_packages(),
    entry_points = {
        'console_scripts':[
            'scrape = scraping.main:default',
            'scrape_api = scraping.api:main',       
            ]
    }
)