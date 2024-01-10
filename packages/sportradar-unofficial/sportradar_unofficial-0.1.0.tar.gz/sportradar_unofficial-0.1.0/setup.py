from setuptools import setup, find_packages

setup(
    name='sportradar_unofficial',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'urllib3',
        'pydantic',
        'requests',
        'pymongo',
        'setuptools>=58.1.0,<59.0.0',
        'coloredlogs>=15.0.1,<16.0.0'
    ],
    author='Gaurav Gurjar, John Bassie, John Bonnett',
    author_email='ggurjar333@gmail.com',
    description='An unofficial python package to access sportradar NFL APIs.',
    license='MIT',
    keywords='sport analysis, sport statistics, sport data analysis, scraping, data collection, data processing, '
             'MongoDB',
    url='http://github.com/ggurjar333/sportradar-unofficial'
)