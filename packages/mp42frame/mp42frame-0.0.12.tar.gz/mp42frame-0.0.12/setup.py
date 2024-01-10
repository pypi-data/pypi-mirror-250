import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mp42frame",
    version="0.0.12",
    author="Z.H.Ding",
    author_email="zh.py.2023@gmail.com",
    description="convert a video file or multiple video files in a directory into a series of image frames",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhdpy/mp42frame/",
    project_urls={
        "Bug Tracker": "https://github.com/zhdpy/mp42frame/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['mp42frame'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'mp42frame = mp42frame:main'
        ]
    },
)
