from setuptools import setup, find_packages

setup(
    name='multilingual_partial_syllable_tokenization',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.15.0',
        'keras>=2.15.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
