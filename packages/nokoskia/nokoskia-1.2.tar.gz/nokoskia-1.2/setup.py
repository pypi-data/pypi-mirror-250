from setuptools import setup, find_packages
import codecs
import os



VERSION = '1.2'
DESCRIPTION = 'simply fill the terminal with famous breaking bad dialogue'
LONG_DESCRIPTION = 'funny command line tool'

# Setting up
setup(
    name="nokoskia",
    version=VERSION,
    author="PranavSV",
    author_email="pranavsv2004@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'breakingbad', 'movie', 'fun', 'funny tools', 'command line tool'],
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: End Users/Desktop',
    'Programming Language :: Python :: 3',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
],
    entry_points={
        "console_scripts":[
                "knock = nokoskia:knock"
        ],
    },
)
