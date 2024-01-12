import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="personalcolor",
    version="0.0.1",
    author="harune arakage",
    author_email="s2122002@stu.musashino-u.ac.jp",
    description="Shows your personal color",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harunearakage/personalcolor",
    project_urls={
        "Bug Tracker": "https://github.com/harunearakage/personalcolor",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['personalcolor'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'personalcolor = personalcolor:main'
        ]
    },
)
