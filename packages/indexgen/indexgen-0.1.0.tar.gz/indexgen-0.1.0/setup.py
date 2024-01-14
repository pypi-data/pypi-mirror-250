from setuptools import setup

setup(
    name="indexgen",
    version="0.1.0",
    packages=['cli'],
    install_requires=[
        "Click",
        "requests",
    ],
    entry_points="""
        [console_scripts]
        indexgen=cli.main:cli
    """,
)
