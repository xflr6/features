# setup.py

from setuptools import setup

setup(
    name='features',
    version='0.5',
    author='Sebastian Bank',
    author_email='sebastian.bank@uni-leipzig.de',
    description='Feature set algebra for linguistics',
    keywords='lattice morphology phonology learning fca',
    license='MIT',
    url='http://github.com/xflr6/features',
    packages=['features'],
    package_data={
        'features': ['config.ini'],
    },
    install_requires=[
        'concepts>=0.7, <0.8',
        'fileconfig>=0.5, <0.6',
        'graphviz>=0.3, <0.4',
    ],
    platforms='any',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
