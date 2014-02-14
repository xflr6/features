# setup.py

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='features',
    version='0.4.1',
    author='Sebastian Bank',
    author_email='sebastian.bank@uni-leipzig.de',
    description='Feature set algebra for linguistics',
    license='MIT',
    keywords='lattice morphology phonology learning fca',
    url='http://github.com/xflr6/features',
    packages=['features'],
    package_data = {
        'features': ['config.ini'],
    },
    install_requires=[
        'concepts==0.6.1',
        'fileconfig==0.4',
        'graphviz==0.2',
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
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
