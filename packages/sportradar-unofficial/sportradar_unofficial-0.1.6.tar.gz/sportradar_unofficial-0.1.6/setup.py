from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='sportradar_unofficial',
    version='0.1.6',
    packages=find_packages(),
    install_requires=[
        'urllib3',
        'pydantic',
        'requests',
        'pymongo',
        'coloredlogs>=15.0.1,<16.0.0'
    ],
    author='Gaurav Gurjar, John Bonnett, John Bassie',
    author_email='ggurjar333@gmail.com',
    description='An unofficial python package to access sportradar NFL APIs.',
    long_description=README,
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='sport analysis, sport statistics, sport data analysis, scraping, data collection, data processing, '
             'MongoDB',
    url='http://github.com/ggurjar333/sportradar-unofficial'
)