from setuptools import setup, find_packages

setup(
    name='lognet',
    version='3.0.1',
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=[
    ],
    author='Noloquideus',
    author_email='daniilmanukian@gmail.com',
    description='A simple logger with a convenient log message format.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=["lognet", "logging", "logger", "log"],
    url='https://github.com/Noloquideus/Lognet',
    license='MIT License',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
