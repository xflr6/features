# setup.py

import io
from setuptools import setup, find_packages

setup(
    name='features',
    version='0.6.dev0',
    author='Sebastian Bank',
    author_email='sebastian.bank@uni-leipzig.de',
    description='Feature set algebra for linguistics',
    keywords='lattice morphology phonology learning fca',
    license='MIT',
    url='https://github.com/xflr6/features',
    project_urls={
        'Documentation': 'https://features.readthedocs.io',
        'Changelog': 'https://features.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/xflr6/features/issues',
        'CI': 'https://travis-ci.org/xflr6/features',
        'Coverage': 'https://codecov.io/gh/xflr6/features',
    },
    packages=find_packages(),
    package_data={'features': ['config.ini']},
    zip_safe=False,
    platforms='any',
    python_requires='>=3.6',
    install_requires=[
        'concepts~=0.7',
        'fileconfig~=0.5',
        'graphviz~=0.7',
    ],
    extras_require={
        'dev': ['tox>=3', 'flake8', 'pep8-naming', 'wheel', 'twine'],
        'test': ['pytest>=4', 'pytest-cov'],
        'docs': ['sphinx>=1.8', 'sphinx-rtd-theme'],
    },
    long_description=io.open('README.rst', encoding='utf-8').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
