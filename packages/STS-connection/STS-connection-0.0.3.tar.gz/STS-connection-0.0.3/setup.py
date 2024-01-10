from setuptools import setup, find_packages

setup(
    name="STS-connection",
    version="0.0.3",
    keywords=["Serial", "Telnet", "SSH"],
    packages=find_packages(),
    author='Yutianlong',
    author_email='longshao863@gmail.com',
    description='This module allows you to easily perform serial, Telnet, and SSH connections in Python scripts, '
                'making the experience similar to using SecureCRT in Python scripts. ',
    readme='README.md',

    license='MIT License',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]

)
