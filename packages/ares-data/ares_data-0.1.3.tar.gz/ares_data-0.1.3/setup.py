from setuptools import setup, find_packages

setup(
    name='ares_data',
    version='0.1.3',
    author='Jan Novopacký',
    author_email='jan.novopacky@gmail.com',
    description='`ares_data` je Python knihovna pro snadné získávání dat o společnostech z Českého obchodního rejstříku ARES.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Newpaw/ares_data',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25'  # Specifikuje minimální verzi requests
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
