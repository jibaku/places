from setuptools import find_packages, setup

setup(
    name="places",
    version="0.1.3",
    author="Fabien Schwob",
    author_email="fabien@x-phuture.com",
    description="Django project to handle places",
    license="BSD",
    url="https://github.com/jibaku/places",
    packages=find_packages(exclude=[]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
