from setuptools import setup, find_packages

# Setup module
setup(
    # Module name
    name="terminalcolor",
    # Module version
    version="1.0.3",
    # Description
    description="Change the Python terminal text color.",
    # Long Description
    long_description=open('README.md').read(),
    # Author - Github username
    author="partcyborg",
    # Author email
    author_email="me@partcyb.org",
    # Project url
    url="https://github.com/partcyborg/TerminalColor",
    # Project packages
    packages=find_packages(),
    # Python requires
    python_requires=">=3.6",
    # Classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)
