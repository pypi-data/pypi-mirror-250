import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="muscletraining",
    version="0.0.3",
    author="niina awaya",
    author_email="s2122003@stu.musashino-u.ac.jp",
    description="Package to determine arm extension and contraction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/awayaniina/muscle-training",
    project_urls={
        "Bug Tracker": "https://github.com/awayaniina/muscle-training",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['muscletraining'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'muscletraining = muscletraining:main'
        ]
    },
)