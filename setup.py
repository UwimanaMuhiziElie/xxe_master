from setuptools import setup, find_packages

setup(
    name="XXE_Master",
    version="1.0.0",
    description="A powerful tool for detecting, and exploiting XML External Entity (XXE) vulnerabilities in web applications.",
    author="ElibitsNinja",
    author_email="muhizielie01@gmail.com",
    url="https://github.com/uwimanaMuhiziElie/xxe_master.git",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.20.0",
        "pyfiglet>=0.8.post1",
        "colorama>=0.4.4",
        "Flask>=2.0.0" 
    ],
    entry_points={
        "console_scripts": [
            "xxe_master=xmaster:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
