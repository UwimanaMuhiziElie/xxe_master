from setuptools import setup, find_packages

setup(
    name="XXE_Master",
    version="1.1.0", 
    description="A versatile tool for detecting and exploiting XML External Entity (XXE) vulnerabilities in web applications and APIs.",
    long_description=(
        "XXE_Master is a cutting-edge tool designed for detecting and exploiting "
        "XXE vulnerabilities in modern web applications and APIs. It includes a "
        "comprehensive payload repository, advanced obfuscation techniques for bypassing "
        "WAFs, and a built-in OOB server for data exfiltration."
    ),
    long_description_content_type="text/markdown",
    author="bl4ck0wl",
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
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Security",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    project_urls={
        "Documentation": "https://github.com/uwimanaMuhiziElie/xxe_master/blob/main/README.md",
        "Source": "https://github.com/uwimanaMuhiziElie/xxe_master",
        "Tracker": "https://github.com/uwimanaMuhiziElie/xxe_master/issues",
    },
)
