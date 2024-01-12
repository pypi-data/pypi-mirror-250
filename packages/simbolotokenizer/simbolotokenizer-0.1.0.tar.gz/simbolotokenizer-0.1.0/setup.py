from setuptools import setup, find_packages

setup(
    name='simbolotokenizer',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.15.0',
        'keras>=2.15.0'
    ],
    description='Multilingual Partial Syllable Tokenization - A rule-based tokenization method designed to align with linguistic nuances while minimizing False Positive errors.',
    long_description=(
        "We would like to introduce Multilingual Partial Syllable Tokenization—a novel rule-based tokenization method "
        "that avoids breaking into complete syllables. Through experimentation, its utility has been uncovered in keyword "
        "detection, effectively minimizing False Positive errors and helping a lot in Burmese's rules-based+machine learning "
        "name recognition. Notably, this tokenization method is designed to align with the linguistic nuances of languages, "
        "but without requiring an exhaustive understanding of each specific language. Now it is integrated with a frequency-based "
        "approach to generate tokens."
    ),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
