from setuptools import setup

setup(
    name="places",
    version="0.1.2",
    author="Fabien Schwob",
    author_email="fabien@x-phuture.com",
    description = ("Django project to handle places"),
    license="BSD",
    url="https://github.com/jibaku/places",
    packages=[
        "places",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
