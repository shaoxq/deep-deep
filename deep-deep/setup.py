#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='deep-deep',
    version='0.0',
    url='https://github.com/TeamHG-Memex/deep-deep',
    description='Adaptive web crawler using Q-Learning',
    # long_description=open('README.rst').read(),
    author='Mikhail Korobov',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Framework :: Scrapy',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'psutil',
        'scrapy >= 1.3.2',
        'w3lib >= 1.17.0',
        'scikit-learn >= 0.18.1',
        'joblib',
        'numpy',
        'scrapy-cdr',
        'json-lines >= 0.3.1',
        'html-text >= 0.2.1',
        'proxy-middleware >= 0.2.0',
        'formasaurus[with_deps]',  # fixme: remove it
    ],
)
